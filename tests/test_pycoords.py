# from csv import DictReader, DictWriter
# import pytest
# from pycoords.coordinates import geocode
# from pycoords.pycoords import fib, main

__author__ = "Aaron Gumapac, Aeinnor Reyes"
__copyright__ = "Aaron Gumapac, Aeinnor Reyes"
__license__ = "MIT"

test_rows = [
    "Maddison Square Garden, 123 Main St, Anytown, CA, 12345, USA, 38.1234, -121.1234",
    "Maddison Square Garden, 123 Main St, Anytown, CA, 12345, USA",
    "Maddison Square Garden, 123 Main St, Anytown, CA, 12345",
    "Maddison Square Garden, 123 Main St, Anytown, CA",
    "Maddison Square Garden, 123 Main St",
    "Maddison Square Garden",
]

# create test csv file containing test_rows
with open("test.csv", "w") as f:
    fieldnames = [
        "name",
        "address",
        "city",
        "state_code",
        "postal_code",
        "country_code",
        "latitude",
        "longitude",
    ]
    f.write(",".join(fieldnames) + "\n")
    for row in test_rows:
        f.write(row + "\n")


# def test_address_from_string():
#     with open("test.csv", "r") as f:
#         reader = DictReader(f)
#         for row in reader:
#             address = Address()
#             address.add_name(row["name"]).add_address(row["address"]).add_city(
#                 row["city"]
#             ).add_state_code(row["state_code"]).add_postal_code(
#                 row["postal_code"]
#             ).add_country_code(
#                 row["country_code"]
#             ).add_latitude(
#                 row.get("latitude")
#             ).add_longitude(
#                 row["longitude"]
#             )
