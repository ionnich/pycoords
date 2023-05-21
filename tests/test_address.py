from pycoords.address import Address
from pycoords.address_mapper import dict_to_address

t_dictionaries = [
    {
        "name": "714",
        "address": "714 W. Girard Ave",
        "city": "Philadelphia",
        "state_code": "PA",
        "country_code": "US",
        "postal_code": "19123",
        "phone": "8668488499",
    },
    {
        "name": "1933",
        "address": "7900 Downing Ave",
        "city": "Bakersfield",
        "state_code": "CA",
        "country_code": "US",
        "postal_code": "93308",
        "phone": "(661) 829-5377",
    },
    {
        "name": "013 - Tilburg",
        "address": "Veemarktstraat 44, 5038 CV",
        "city": "Tilburg",
        "state_code": "",
        "country_code": "NL",
        "postal_code": "",
        "phone": "",
    },
    {
        "name": "04 Center",
        "address": "2701 S Lamar Blvd",
        "city": "Austin",
        "state_code": "TX",
        "country_code": "US",
        "postal_code": "78704",
        "phone": "(512) 333-0404",
    },
    {
        "name": "1 Hotel South Beach",
        "address": "2341 Collins Ave",
        "city": "Miami Beach",
        "state_code": "FL",
        "country_code": "US",
        "postal_code": "33139",
        "phone": "3056041000",
    },
]

t_addresses = [Address(**data) for data in t_dictionaries]


def test_address_mapper():
    addresses = dict_to_address(t_dictionaries)

    assert addresses[2].state_code == ""
    assert addresses[2].latitude == ""
    assert addresses[2].longitude == ""
    assert addresses == t_addresses

    for i, t_dict in enumerate(t_dictionaries):
        address = addresses[i].dict()
        address_dict = {key: value for key, value in address.items() if value != ""}
        t_dict = {key: value for key, value in t_dict.items() if value != ""}

        assert address_dict == t_dict


def test_nonetypes():
    none_dict = {
        "name": None,
        "address": None,
        "city": None,
        "state_code": None,
        "country_code": None,
        "postal_code": None,
        "phone": None,
    }
    address = Address(**none_dict)

    assert address.name == ""
    assert address.address == ""
    assert address.city == ""
    assert address.state_code == ""
    assert address.postal_code == ""
    assert address.country_code == ""
    assert address.latitude == ""
    assert address.longitude == ""


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
