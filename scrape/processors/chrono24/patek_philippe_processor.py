import sys
import os


root_path = "/".join(os.path.dirname(__file__).split("/")[:-3])
sys.path.append(root_path)

from ast import literal_eval
from watch_service import engine
from watch_service.daos import watch_dao, listings_dao
from watch_service.services import listings_service
import pandas as pd
from watch_service.utils import csv_utils

path = ""


def process():
    df = pd.read_csv(path)
    with engine.connect() as conn:

        for i, l in df.iterrows():
            listings = literal_eval(l["listing_data"])
            rf = l["reference_number"]
            for listing in listings:
                listing["reference_number"] = rf
                listings_service.upsert_processed_listing(conn, listing)


if __name__ == "__main__":
    process()
