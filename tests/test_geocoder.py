import pytest
import requests

from pycoords.address import Address
from pycoords.geocoder import geocode_addresses, get_api_key

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


def test_geocoder(monkeypatch):
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="pycoords_test")

    # NOTE: provide your own API key for testing
    test_api_key = get_api_key()

    nominatim = geolocator.geocode

    def google(query):
        return google_maps_api(query, test_api_key)

    # NOTE: change respective backends for desired tests
    backend = google
    engine = "google"

    test_locations = [backend(query) for query in test_queries]
    mapped_addresses = geocode_addresses(t_dataset, engine=engine, parallel=True)

    with pytest.raises(SystemExit):
        geocode_addresses(t_dataset, engine="invalid")

    if engine == "google" and backend == google:
        for i, address in enumerate(mapped_addresses):
            assert address.latitude == test_locations[i][0]
            assert address.longitude == test_locations[i][1]

    elif engine == "nominatim" and backend == nominatim:
        for i, address in enumerate(mapped_addresses):
            assert address.latitude == test_locations[i].latitude  # type: ignore
            assert address.longitude == test_locations[i].longitude  # type: ignore
