import sys
import os

root_path = "/".join(os.path.dirname(__file__).split("/")[:-2])
sys.path.append(root_path)

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from watch_service.utils import csv_utils
from scrape.utils import webscraping_utils
import pandas as pd
from ast import literal_eval

BASE_URL = "https://www.watchbase.com/"


def _map_caliber_info(payload):
    return {
        "movement": payload["movement"],
        "caliber": payload["caliber"],
        "brand": payload["brand"],
        "power_reserve": payload["power_reserve"],
        "qty_jewels": payload["qty_jewels"],
    }


def _format_url(caliber, brand):
    b = "-".join(brand.split(" ")).lower()
    if brand == "Patek Phillipe":
        c = "-".join(("-".join(caliber.split(" ")).split("/"))).lower()
    elif brand == "Rolex":
        c = caliber
    elif brand == "Audemars Piguet":
        c = f"ap-{caliber}"
    return BASE_URL + f"{b}/caliber/{c}"


def scrape_caliber_info(caliber, brand):
    data = {"caliber": caliber, "brand": brand}
    url = _format_url(caliber, brand)

    source = webscraping_utils.extract_source(url)

    soup = BeautifulSoup(source, "html.parser")
    caliber_detail = soup.find("div", {"id": "caliber-detail"})
    if not caliber_detail:
        data["exception"] = "true"
        return data

    rows = caliber_detail.find_all("tr")
    for row in rows:
        h = row.find("th").text
        d = row.find("td")
        if "Movement" in h:
            data["movement"] = d.text
        elif "Reserve" in h:
            data["power_reserve"] = d.text
        elif "Jewels" in h:
            data["qty_jewels"] = d.text
        elif "Frequency" in h:
            data["frequency"] = d.text

    return data


if __name__ == "__main__":
    patek = pd.read_csv("patek.csv")
    rolex = pd.read_csv("rolex.csv")
    ap = pd.read_csv("ap.csv")

    calibers = {}
    calibers["Patek Phillipe"] = set()
    calibers["Rolex"] = set()
    calibers["Audemars Piguet"] = set()

    for i, watch in patek.iterrows():
        caliber = literal_eval(watch["caliber"])["caliber_caliber"]
        calibers["Patek Phillipe"].add(caliber)

    for i, watch in ap.iterrows():
        caliber = literal_eval(watch["caliber"])["caliber_caliber"]
        calibers["Audemars Piguet"].add(caliber.lower())

    for i, watch in rolex.iterrows():
        caliber = literal_eval(watch["movement"])["movement_caliber"]
        calibers["Rolex"].add(caliber.lower())

    c = []
    exceptions = []
    for key, val in calibers.items():
        for caliber in val:
            cal = caliber
            if key == "Rolex":
                cal = caliber.split(",")[0].strip()
            data = scrape_caliber_info(cal, key)
            if "exception" in data.keys():
                exceptions.append(data)
            else:
                c.append(data)

    csv_utils.write_csv("caliber_info.csv", c)
    csv_utils.write_csv("exceptions.csv", exceptions)
