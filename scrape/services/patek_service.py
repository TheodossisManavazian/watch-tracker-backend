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
from time import sleep
import pandas as pd

PATEK_BASE_URL = "https://www.patek.com"
collections = "https://www.patek.com/en/collection/all-models"


class ExceptionReviewWebDetails(Exception):
    pass


class EceptionCaptcha(Exception):
    pass


def patek__extract_all_data(dr, url: str, reference_number: str) -> dict | None:
    data = {}
    dr.get(url)
    sleep(2)
    try:
        cookies = dr.find_element(By.XPATH, '//a[contains(@class, "lightbrown")]')
        if cookies:
            cookies.click()
    except:
        pass

    toggle_button = dr.find_element(By.XPATH, '//a[contains(@class, "toggle_button")]')
    toggle_button.click()

    source = dr.page_source
    soup = BeautifulSoup(source, "html.parser")

    hidden_article = soup.find("div", "hidden_article")
    price = hidden_article.find("span", {"id": "product_price"}).text
    price = price.split(" ")[0]
    price = float(price.replace("'", ""))

    image = soup.find("div", "face_img")
    image_link = image.find("img", "lazyload")
    if image_link:
        image_link = image_link["data-src"]
    else:
        image_link = image.find("img", "lazyloaded")
        if image_link:
            image_link = image_link["data-src"]
        else:
            image_link = ""

    data["reference_number"] = reference_number
    data["retail_price"] = price
    data["image_url"] = image_link
    data["watch_url"] = url

    article_data = soup.find_all("div", "article_flexbox_right_content")

    for article in article_data:
        header = article.find("div", "article_flexbox_right_content_title").text
        info = article.find("div", "article_flexbox_right_content_text").text

        if header == "Dial":
            section = "dial"
            data[section] = {}
            info = info.split(",")
            dial_color = info[0]
            dial_details = ""
            if len(info) > 1:
                dial_details = "".join(info[1:])
            data[section]["dial_color"] = dial_color.strip()
            data[section]["dial_details"] = dial_details.strip()

        if header == "Case":
            section = "case"
            data[section] = {}

            ix1 = info.find(".")
            case_material = info[0:ix1]
            info = info[ix1 + 1 :]
            ix1 = info.find(":")
            ix2 = info.find("mm.")
            if ix1 > 0 and ix1 < ix2:
                case_diameter = info[ix1 + 1 : ix2 + 2]
            else:
                case_diameter = info[: ix2 + 2]

            info = info[ix2 + 3 :]
            ix = info.find("Water-resistant")
            info = info[ix:]
            ix = info.find(".")
            case_water_resistance = " ".join(info[: ix + 1].split(" ")[-2:])
            case_details = info[ix1 + 1 :].replace("\n", " ")

            data[section]["case_material"] = case_material.strip()
            data[section]["case_diameter"] = case_diameter.strip()
            data[section]["case_water_resistance"] = case_water_resistance.strip()
            data[section]["case_details"] = case_details.strip()

        if header == "Strap":
            section = "bracelet"
            data[section] = {}
            info = info.split(".")

            bracelet_first = info[0].split(",")
            bracelet_material, bracelet_color, bracelet_details = "", "", ""

            if len(bracelet_first) > 1:
                bracelet_material = bracelet_first[0]
                bracelet_color = bracelet_first[-1]

            if len(info) > 1:
                bracelet_details = "".join(info[1:]).strip()

            data[section]["bracelet_material"] = bracelet_material.strip()
            data[section]["bracelet_color"] = bracelet_color.strip()
            data[section]["bracelet_details"] = bracelet_details.strip()

        if header == "Bracelet":
            section = "bracelet"
            data[section] = {}
            info = info.split(".")

            bracelet_material, bracelet_color, bracelet_details = "", "", ""

            if len(info) > 1:
                bracelet_details = "".join(info[1:]).strip()

            bracelet_material = info[0]
            bracelet_color = info[0]

            data[section]["bracelet_material"] = bracelet_material.strip()
            data[section]["bracelet_color"] = bracelet_material.strip()
            data[section]["bracelet_details"] = bracelet_details.strip()

    caliber_content = soup.find("div", "caliber_content")
    caliber_number = caliber_content.find("span", "reference").text.strip()
    section = "caliber"
    data[section] = {}
    data[section]["caliber_caliber"] = caliber_number


def extract_model_links(url: str) -> List[str]:
    links = []
    dr = webdriver.Chrome()
    dr.get(url)
    sleep(5)

    source = dr.page_source
    soup = BeautifulSoup(source, "html.parser")
    articles = soup.find_all("div", "article filtered")
    for article in articles:
        a = article.find("a")
        links.append(a["href"])
    return links


def gather_links(url: str):
    model_numbers = extract_model_links(url)
    data = []
    for i in model_numbers:
        data.append({"link": i})

    csv_utils.write_csv("patek_links.csv", data, "a")


def scrape(from_index: int):
    dr = webdriver.Chrome()
    watches = []
    excpetions = []
    model_numbers = pd.read_csv("patek_links.csv")
    for i, url in model_numbers.iloc[from_index:].iterrows():
        print("scraping index", i, "of", len(model_numbers), "", url)
        u = PATEK_BASE_URL + url["link"]
        rn = u.split("/")[-1]
        rn = rn.split("-")
        if len(rn) == 3:
            rn = f"{rn[0]}/{rn[1]}-{rn[2]}"
        else:
            rn = f"{rn[0]}-{rn[1]}"

        data = patek__extract_all_data(dr, u, rn)
        print(data)
        if "exception" in data.keys():
            excpetions.append(data)
            break
        else:
            watches.append(data)

    if len(watches) > 0:
        csv_utils.write_csv("patek.csv", watches, "a")
    if len(excpetions) > 0:
        csv_utils.write_csv("exceptions.csv", excpetions, "a")
