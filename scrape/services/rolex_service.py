import sys
import os

root_path = "/".join(os.path.dirname(__file__).split("/")[:-2])
sys.path.append(root_path)

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from typing import Union, List
from watch_service import engine
from watch_service.utils import csv_utils
from scrape.utils import webscraping_utils
from watch_service.services import watch_service, listings_service
from time import sleep
import pandas as pd

ROLEX_BASE_URL = "https://www.rolex.com"

MODEL_CASE_MAPPINGS = {
    "Model case": "case_model_case",
    "Oyster architecture": "case_oyster_architecture",
    "Diameter": "case_diameter",
    "Material": "case_material",
    "Bezel": "case_bezel",
    "Winding crown": "case_winding_crown",
    "Crystal": "case_crystal",
    "Water resistance": "case_water_resistance",
}

MOVEMENT_MAPPINGS = {
    "Movement": "movement_movement",
    "Calibre": "movement_caliber",
    "Precision": "movement_precision",
    "Functions": "movement_functions",
    "Oscillator": "movement_oscillator",
    "Winding": "movement_winding",
    "Power reserve": "movement_power_reserve",
}

BRACELET_MAPPINGS = {
    "Bracelet": "bracelet_bracelet",
    "Material": "bracelet_material",
    "Clasp": "bracelet_clasp",
}

DIAL_MAPPINGS = {"Dial": "dial_dial", "Details": "dial_details"}

SECTIONS = [
    ["case", MODEL_CASE_MAPPINGS],
    ["movement", MOVEMENT_MAPPINGS],
    ["bracelet", BRACELET_MAPPINGS],
    ["dial", DIAL_MAPPINGS],
]


def rolex__extract_all_data(dr, url: str, reference_number: str) -> dict | None:
    data = {}
    dr.get(url)

    sleep(2.3)
    source = dr.page_source
    soup = BeautifulSoup(source, "html.parser")
    main = soup.find("main")
    if not main:
        return None

    try:
        price = main.find("span", "price").text
        image_link = main.find_all("img", "css-fmei9v e1jb8e190")[1]["srcset"]
        sections = main.find_all("div", "css-1vfgbko e1yf0wve4")
        list_items = []

        data["reference_number"] = reference_number
        data["retail_price"] = float(price.strip()[1:].replace(",", ""))
        data["image_url"] = image_link.split(" ")[-2]
        data["watch_url"] = url

        for section in sections:
            list_items.append(section.find_all("li"))

        i = 0
        for list_item in list_items:
            name, mappings = SECTIONS[i]
            data[name] = {}
            for d in list_item:
                header = d.find("h5").text
                para = d.find("p").text
                if header in mappings.keys():
                    data[name][mappings[header]] = para
                else:
                    data[name][header] = para
            i += 1

    except Exception as e:
        return {"reference_number": reference_number, "exception": e}

    return data


def extract_model_links(url: str) -> List[str]:
    links = []
    dr = webdriver.Chrome()
    dr.get(url)
    sleep(5)
    try:
        view_more = dr.find_element(By.XPATH, '//button[contains(text(), "View more")]')
        while view_more:
            view_more.click()
            sleep(5)
            view_more = dr.find_element(
                By.XPATH, '//button[contains(text(), "View more")]'
            )
    except Exception as e:
        print(e)

    source = dr.page_source
    soup = BeautifulSoup(source, "html.parser")
    ml = soup.find("div", "css-oj0oop eyz9ve28")

    uls = ml.find_all("li", "css-zjik7 eyz9ve25")
    for ul in uls:
        a = ul.find("a")
        links.append(a["href"])
    return links


def gather_links(url: str):
    model_numbers = extract_model_links(url)
    data = []
    for i in model_numbers:
        data.append({"link": i})

    csv_utils.write_csv("rolex_links.csv", data, "a")


def scrape(from_index: int):
    dr = webdriver.Chrome()
    rolex = []
    excpetions = []
    model_numbers = pd.read_csv("rolex_links.csv")
    for i, url in model_numbers.iloc[from_index:].iterrows():
        print("scraping index", i, "of", len(model_numbers), "", url)
        u = ROLEX_BASE_URL + url["link"]
        rn = u.split("/")[-1][1:]
        data = rolex__extract_all_data(dr, u, rn)
        if "exception" in data.keys():
            excpetions.append(data)
        else:
            rolex.append(data)

    csv_utils.write_csv("rolex.csv", rolex, "a")
    if len(excpetions) > 0:
        csv_utils.write_csv("exceptions.csv", excpetions, "a")
