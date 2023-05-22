import csv
import os

from pycoords.address import Address
from pycoords.csv_writer import write_csv

# TODO @Aeinnor Implement this
t_dataset = [
    Address(
        name="714",
        address="714 W. Girard Ave",
        city="Philadelphia",
        state_code="PA",
        country_code="US",
        postal_code="19123",
        phone="8668488499",
    ),
    Address(
        name="1933",
        address="7900 Downing Ave",
        city="Bakersfield",
        state_code="CA",
        country_code="US",
        postal_code="93308",
        phone="(661) 829-5377",
    ),
    Address(
        name="013 - Tilburg",
        address="Veemarktstraat 44, 5038 CV",
        city="Tilburg",
        state_code="",
        country_code="NL",
        postal_code="",
        phone="",
    ),
    Address(
        name="04 Center",
        address="2701 S Lamar Blvd",
        city="Austin",
        state_code="TX",
        country_code="US",
        postal_code="78704",
        phone="(512) 333-0404",
    ),
    Address(
        name="1 Hotel South Beach",
        address="2341 Collins Ave",
        city="MIami Beach",
        state_code="FL",
        country_code="US",
        postal_code="33139",
        phone="3056041000",
    ),
]


def test_csv_writer():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(test_dir, "write_sample.csv")

    geocoded = write_csv(t_dataset, csv_file_path)

    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    assert geocoded == 0
    assert len(data) == 5
    assert data == [address.dict() for address in t_dataset]
