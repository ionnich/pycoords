from pycoords.address import Address
from pycoords.geocoder import geocode_addresses

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
]


def test_geocoder():
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="pycoords_test")

    test_queries = [
        "714 W. Girard Ave, Philadelphia, PA 19123",
        "7900 Downing Ave, Bakersfield, CA 93308",
        "Veemarktstraat 44, 5038 CV, Tilburg, NL",
    ]

    test_locations = [geolocator.geocode(query) for query in test_queries]
    mapped_addresses = geocode_addresses(t_dataset)

    for i, address in enumerate(mapped_addresses):
        assert address.latitude == test_locations[i].latitude  # type: ignore
        assert address.longitude == test_locations[i].longitude  # type: ignore
