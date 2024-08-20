import csv
from typing import List


def write_csv(filename: str, data: List[dict]):
    keys = data[0].keys()
    with open(f"{filename}", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
