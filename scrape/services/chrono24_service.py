from bs4 import BeautifulSoup
from typing import Union, List
from watch_service import engine
from watch_service.utils import csv_utils
from watch_service.services import watch_service
from watch_service.services import listings_service
from scrape.utils.webscraping_utils import extract_source

CHRONO24__BASE_URL = 'https://www.chrono24.com'
CHRONO24__LISTINGS_BASE_URL = "https://www.chrono24.com/search/index.htm?query="
CHRONO24__LISTINGS_URL_PARAMS = "&dosearch=true&searchexplain=false&watchTypes=U&pageSize=120&priceFrom=1"

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


def _load_waches() -> Union[List[dict], None]:
    with engine.connect() as conn:
        return watch_service.get_all_watches_full(conn)


# Chrono24 paramas are seperated by a '+'
def _load_params(watch: dict) -> List:
    params = []
    if watch["nickname"]:
        nn = "+".join(watch["nickname"].split(" "))
        params.append(nn)
    elif watch["dial"]:
        params.append(f'{watch["dial"]}+Dial')
    return params


def _format_url(brand: str, reference_number: str, query_list: List) -> dict:
    f_reference_number = reference_number.split("-")[0]
    query = f"{brand}+{f_reference_number}"
    for p in query_list:
        query += f"+{p}"

    return {
        "query": query,
        "url": CHRONO24__LISTINGS_BASE_URL + query + CHRONO24__LISTINGS_URL_PARAMS,
    }


def chrono24__collect_listings_from_all_pages(url: str, page_number: int, links: List) -> None:
    page_url = url + f"&showpage={page_number}"

    source = extract_source(page_url)
    soup = BeautifulSoup(source, features="html.parser")
    watches = soup.find("div", id="wt-watches")

    if not watches:
        return

    a = watches.find_all("a", class_="rcard")
    for i in range(len(a)):
        links.append(f'{CHRONO24__BASE_URL}/{a[i]["href"]}')

    chrono24__collect_listings_from_all_pages(url, page_number + 1, links)


def chrono_24__get_all_current_listings(
    brand: str, reference_number: str, params: List
) -> Union[List, None]:
    links = []
    f = _format_url(brand, reference_number, params)
    query, url = f["query"], f["url"]
    chrono24__collect_listings_from_all_pages(url, 1, links)

    return {"query": query, "links": links}


def chrono24__extract_data_from_listing(
    listing_url: str, data_to_extract: dict
) -> Union[List[dict], None]:
    source = extract_source(listing_url)
    soup = BeautifulSoup(source, features="html.parser")
    row = soup.find_all("td")

    payload = {"listing_url": listing_url}

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
    query_params: List,
    fields_to_extract: dict = CHRONO24__FIELD_NAMES,
) -> Union[List[dict], None]:
    all_listings = chrono_24__get_all_current_listings(brand, reference_number, query_params)
    query, links = all_listings["query"], all_listings["links"]

    res = {
        "reference_number": reference_number,
        "brand": brand,
        "query": query,
        "listing_data": {},
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


def get_insert_all_listings_for_each_reference_number():
    WATCHES = _load_waches()
    not_inserted = []

    with engine.connect() as conn:
        for watch in WATCHES:
            params = _load_params(watch)
            brand = watch["brand"]
            reference_number = watch["reference_number"]
            listings = chrono24__extract_data_from_all_listings(brand, reference_number, params)
            not_inserted.extend(listings_service.upsert_listing_from_chrono24_service(conn, listings))

    if len(not_inserted) > 0:
        csv_utils.write_csv("not_inserted.csv", not_inserted)
