from pycoords.address import Address
from pycoords.address_mapper import dict_to_address

t_dictionaries = [
    {
        "name": "714",
        "address": "714 W. Girard Ave",
        "city": "Philadelphia",
        "state_code": "PA",
        "postal_code": "19123",
        "country_code": "US",
    },
    {
        "name": "1933",
        "address": "7900 Downing Ave",
        "city": "Bakersfield",
        "state_code": "CA",
        "postal_code": "93308",
        "country_code": "US",
    },
    {
        "name": "013 - Tilburg",
        "address": "Veemarktstraat 44, 5038 CV",
        "city": "Tilburg",
        "state_code": "",
        "postal_code": "",
        "country_code": "NL",
    },
    {
        "name": "04 Center",
        "address": "2701 S Lamar Blvd",
        "city": "Austin",
        "state_code": "TX",
        "postal_code": "78704",
        "country_code": "US",
    },
    {
        "name": "1 Hotel South Beach",
        "address": "2341 Collins Ave",
        "city": "Miami Beach",
        "state_code": "FL",
        "postal_code": "33139",
        "country_code": "US",
    },
]

t_addresses = [Address(**data) for data in t_dictionaries]


def test_address_mapper():
    addresses = dict_to_address(t_dictionaries)

    assert addresses[2].state_code == ""
    assert addresses[2].latitude == ""
    assert addresses[2].longitude == ""
    assert addresses == t_addresses


def test_address_str():
    assert str(t_addresses[0]) == "714, 714 W. Girard Ave, Philadelphia, PA, 19123, US"
    assert str(t_addresses[1]) == "1933, 7900 Downing Ave, Bakersfield, CA, 93308, US"
    assert (
        str(t_addresses[2]) == "013 - Tilburg, Veemarktstraat 44, 5038 CV, Tilburg, NL"
    )
    assert str(t_addresses[3]) == "04 Center, 2701 S Lamar Blvd, Austin, TX, 78704, US"
    assert (
        str(t_addresses[4])
        == "1 Hotel South Beach, 2341 Collins Ave, Miami Beach, FL, 33139, US"
    )
