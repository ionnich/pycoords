import os

import pytest

from pycoords.csv_reader import read_csv


@pytest.fixture
def sample_csv():
    csv_file = os.path.join(os.path.dirname(__file__), "sample.csv")
    return csv_file


def test_read_csv(sample_csv):
    expected_data = [
        {
            "name": "714",
            "address": "714 W. Girard Ave",
            "city": "Philadelphia",
            "state_code": "PA",
            "country_code": "US",
            "postal_code": "19123",
            "phone": "8668488499",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "1933",
            "address": "7900 Downing Ave",
            "city": "Bakersfield",
            "state_code": "CA",
            "country_code": "US",
            "postal_code": "93308",
            "phone": "(661) 829-5377",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "013 - Tilburg",
            "address": "Veemarktstraat 44, 5038 CV",
            "city": "Tilburg",
            "state_code": "",
            "country_code": "NL",
            "postal_code": "",
            "phone": "",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "04 Center",
            "address": "2701 S Lamar Blvd",
            "city": "Austin",
            "state_code": "TX",
            "country_code": "US",
            "postal_code": "78704",
            "phone": "(512) 333-0404",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "1 Hotel South Beach",
            "address": "2341 Collins Ave",
            "city": "Miami Beach",
            "state_code": "FL",
            "country_code": "US",
            "postal_code": "33139",
            "phone": "3056041000",
            "latitude": None,
            "longitude": None,
        },
    ]

    result = read_csv(sample_csv)
    assert result == expected_data
