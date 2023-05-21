import os
import pytest
from pycoords.csv_reader import read_csv


@pytest.fixture
def sample_csv():
    csv_file = os.path.join(os.path.dirname(__file__), "sample.csv")
    return csv_file


def test_read_csv(sample_csv):
    expected_data = [
        {"name": "714", "address": "714 W. Girard Ave", "city": "Philadelphia",
            "state_code": "PA", "postal_code": "19123", "country_code": "US"},
        {"name": "1933", "address": "7900 Downing Ave", "city": "Bakersfield",
            "state_code": "CA", "postal_code": "93308", "country_code": "US"},
        {"name": "013 - Tilburg", "address": "Veemarktstraat 44, 5038 CV",
            "city": "Tilburg", "state_code": "", "postal_code": "", "country_code": "NL"},
        {"name": "04 Center", "address": "2701 S Lamar Blvd", "city": "Austin",
            "state_code": "TX", "postal_code": "78704", "country_code": "US"},
        {"name": "1 Hotel South Beach", "address": "2341 Collins Ave", "city": "Miami Beach",
            "state_code": "FL", "postal_code": "33139", "country_code": "US"}
    ]

    result = read_csv(sample_csv)
    assert result == expected_data
