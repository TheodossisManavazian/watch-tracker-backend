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
    REFERENCE_NUMBERS = set()
    processed_listings = []
    flagged_listings = []
    not_in_db = []
    with engine.connect() as conn:
        with conn.begin():
            watches = watch_dao.get_watches_full_by_query(conn, {"query": "Rolex"})

        for watch in watches:
            REFERENCE_NUMBERS.add(watch["watch"]["reference_number"])

        for i, l in df.iterrows():
            pl = []
            fl = []

            listings = literal_eval(l["listing_data"])
            for listing in listings:
                lrn = listing["reference_number"].split(" ")[0].upper()
                if lrn in REFERENCE_NUMBERS:
                    listing["reference_number"] = lrn
                    pl.append(listing)
                elif "-" in lrn or lrn == "":
                    not_in_db.append(listing)
                    continue
                else:
                    with conn.begin():
                        aws = (
                            watch_dao.get_watches_full_by_like_reference_number(
                                conn, {"reference_number": lrn}
                            )
                            or []
                        )
                        flag = False
                        for aw in aws:
                            if listing["dial"].upper() == aw["watch"]["dial"].upper():
                                listing["reference_number"] = aw["watch"][
                                    "reference_number"
                                ]
                                pl.append(listing)
                                flag = True
                                break
                        if not flag:
                            fl.append(listing)

            print("\n" * 3, "-" * 30)
            print(fl)
            print(f"number listings: {len(listings)}")
            print(f"processed listings: {len(pl)}")
            print(f"flagged listings: {len(fl)}")
            print(f"not in db: {len(not_in_db)}")

            processed_listings.extend(pl)
            flagged_listings.extend(fl)

        if len(processed_listings) > 0:
            csv_utils.write_csv("processed_listings.csv", processed_listings)
            listings_service.upsert_processed_listings(conn, processed_listings)
        if len(flagged_listings) > 0:
            csv_utils.write_csv("flagged_listings.csv", flagged_listings)


if __name__ == "__main__":
    process()
