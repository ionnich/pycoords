from pycoords.address import dictionaries_to_addresses, Address

t_dictionaries = [
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

t_addresses = [Address(**data) for data in t_dictionaries]


def test_dictionaries_to_addresses():
    addresses = dictionaries_to_addresses(t_dictionaries)

    assert addresses[2].state_code is None
    assert addresses[2].latitude is None
    assert addresses[2].longitude is None
    assert addresses == t_addresses
