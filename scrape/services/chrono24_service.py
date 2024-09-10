import sys
import os

root_path = "/".join(os.path.dirname(__file__).split("/")[:-2])
sys.path.append(root_path)

from bs4 import BeautifulSoup
from typing import Union, List
from watch_service import engine
from scrape.utils import webscraping_utils
from watch_service.utils import csv_utils
from watch_service.services import listings_service, watch_service
import time

CHRONO24__BASE_URL = "https://www.chrono24.com"
CHRONO24__LISTINGS_BASE_URL = "https://www.chrono24.com/search/index.htm?query="
CHRONO24__LISTINGS_URL_PARAMS = (
    "&dosearch=true&searchexplain=false&watchTypes=U&pageSize=120&priceFrom=1"
)

features = [
    "brand",
    "model",
    "reference_number",
    "year",
    "condition",
    "location",
    "listing_price",
    "accessories",
    "listing",
]

CHRONO24__FIELD_NAMES = {
    "Brand": "brand",
    "Dial": "dial",
    "Model": "model",
    "Reference number": "reference_number",
    "Year of production": "year",
    "Condition": "condition",
    "Location": "location",
    "Price": "price",
    "Scope of delivery": "accessories",
    "Listing code": "listing_code",
}


def _generate_query(brand: str, reference_number: str) -> dict:
    if brand == "Rolex":
        f_reference_number = reference_number.split("-")[0]
    else:
        f_reference_number = reference_number.split("/")

        if len(f_reference_number) > 1:
            f_reference_number = f"%2F".join(f_reference_number)
        else:
            f_reference_number = f_reference_number[0]

    query = f"{brand}+{f_reference_number}"

    return {
        "query": query,
        "url": CHRONO24__LISTINGS_BASE_URL + query + CHRONO24__LISTINGS_URL_PARAMS,
    }


def chrono24__collect_listings_from_all_pages(
    url: str, page_number: int, links: List
) -> None:
    page_url = url + f"&showpage={page_number}"

    source = webscraping_utils.extract_source(page_url)
    soup = BeautifulSoup(source, features="html.parser")
    watches = soup.find("div", id="wt-watches")

    if not watches:
        return

    a = watches.find_all("a", class_="rcard")
    for i in range(len(a)):
        links.append(f'{CHRONO24__BASE_URL}/{a[i]["href"]}')

    chrono24__collect_listings_from_all_pages(url, page_number + 1, links)


def chrono_24__get_all_current_listings(
    brand: str, reference_number: str
) -> Union[List, None]:
    links = []
    f = _generate_query(brand, reference_number)
    query, url = f["query"], f["url"]

    if query in queries:
        return
    queries.add(query)

    print(f"using query {query}")
    chrono24__collect_listings_from_all_pages(url, 1, links)
    return {"query": query, "links": links}


def chrono24__extract_data_from_listing(
    listing_url: str,
    data_to_extract: dict,
) -> Union[List[dict], None]:

    source = webscraping_utils.extract_source(listing_url)
    soup = BeautifulSoup(source, features="html.parser")
    main = soup.find("main", {"id": "main-content"})
    container = main.find("div", "container")
    row = main.find_all("td")
    payload = {"listing_url": listing_url}

    if container:
        title = container.find("span", "d-block")
        if title:
            payload["title"] = " ".join(title.text.split())

    image_url = main.find("div", "watch-image-carousel-image")
    if image_url:
        if image_url.has_attr("style"):
            payload["image_url"] = image_url["style"].replace(
                "background-image: url('", ""
            )[:-3]

    for i, val in data_to_extract.items():
        payload[val] = ""

    voided_keywords = set()

    for i in range(len(row)):
        if row[i].text in data_to_extract.keys() and row[i].text not in voided_keywords:
            feature = row[i].text
            data = row[i + 1].text.strip()
            data = data.split("\n")[0]
            payload[CHRONO24__FIELD_NAMES[feature]] = data

    return payload


def chrono24__extract_data_from_all_listings(
    brand: str,
    reference_number: str,
    fields_to_extract: dict = CHRONO24__FIELD_NAMES,
) -> Union[List[dict], None]:

    all_listings = chrono_24__get_all_current_listings(brand, reference_number)
    if not all_listings:
        return

    query, links = all_listings["query"], all_listings["links"]

    res = {
        "reference_number": reference_number,
        "brand": brand,
        "query": query,
        "listing_data": [],
    }

    if len(all_listings) < 1:
        return res

    data = []
    for link in links:
        d = chrono24__extract_data_from_listing(link, fields_to_extract)
        if d is not None:
            data.append(d)

    res["listing_data"] = data
    return res


def insert_all_listings_for_each_reference_number():
    exceptions = []
    lgs = []
    with engine.connect() as conn:
        WATCHES = watch_service.get_watches_full_by_query(conn, "Audemars Piguet")

    with engine.connect() as conn:
        for w in WATCHES:
            watch = w["watch"]
            print(f"grabbing listings for {watch.reference_number}...")
            try:
                listings = chrono24__extract_data_from_all_listings(
                    watch.brand, watch.reference_number
                )
            except:
                exceptions.append(dict(watch))
            if listings:
                lgs.append(listings)

    if len(lgs) > 0:
        csv_utils.write_csv("current_listings_ap.csv", lgs)
    if len(exceptions) > 0:
        csv_utils.write_csv("exceptions.csv", exceptions)


queries = set()
if __name__ == "__main__":
    start_time = time.time()
    insert_all_listings_for_each_reference_number()
    print("--- %s seconds ---" % (time.time() - start_time))
