import pytest
import requests

from pycoords.address import Address
from pycoords.geocoder import geocode_addresses, get_api_key

# TODO: verify that tests are running

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

test_queries = [
    "714 W. Girard Ave, Philadelphia, PA 19123",
    "7900 Downing Ave, Bakersfield, CA 93308",
    "Veemarktstraat 44, 5038 CV, Tilburg, NL",
    "714 W. Girard Ave, Philadelphia, PA 19123",
    "7900 Downing Ave, Bakersfield, CA 93308",
    "Veemarktstraat 44, 5038 CV, Tilburg, NL",
]


def google_maps_api(query: str, api_key: str):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": query, "key": api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK" and data["results"]:
        result = data["results"][0]
        latitude = result["geometry"]["location"]["lat"]
        longitude = result["geometry"]["location"]["lng"]

        return latitude, longitude


def test_geocoder():
    from geopy.geocoders import Nominatim

    # NOTE: provide your own API key for testing
    test_api_key = get_api_key()

    geolocator = Nominatim(user_agent="pycoords_test")

    nominatim = geolocator.geocode

    def google(query):
        return google_maps_api(query, test_api_key)

    with pytest.raises(SystemExit):
        geocode_addresses(t_dataset, engine="invalid")

    engine = "nominatim"
    nominatim_set = [nominatim(query) for query in test_queries]
    mapped_addresses, _ = geocode_addresses(t_dataset, engine=engine, parallel=True)
    for i, address in enumerate(mapped_addresses):
        assert address.latitude == nominatim_set[i][0]  # type: ignore
        assert address.longitude == nominatim_set[i][1]  # type: ignore

    engine = "google"
    google_set = [google(query) for query in test_queries]
    for i, address in enumerate(mapped_addresses):
        assert address.latitude == google_set[i].latitude  # type: ignore
        assert address.longitude == google_set[i].longitude  # type: ignore
