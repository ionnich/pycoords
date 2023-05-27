from time import sleep as std_sleep

import requests
from geopy import Nominatim
from geopy.exc import GeocoderQueryError, GeocoderTimedOut, GeocoderUnavailable
from requests_ip_rotator import ApiGateway

from pycoords.address import Address


def geocode_with_nominatim(address: Address, attempts=3) -> Address:
    """
    Geocodes an address using the Nominatim geocoder.

    :param Address address: The address to be geocoded.
    :return: A new address object with the lat and lon attributes populated.
    :rtype: Address
    """
    if attempts <= 0:
        return address

    geolocator = Nominatim(user_agent="pycoords")

    # copy address to an internal mutable object
    _address = address.copy()
    _address_str = str(_address)

    try:
        location = geolocator.geocode(_address_str)
    except (GeocoderTimedOut, GeocoderUnavailable):
        std_sleep(1)
        return geocode_with_nominatim(address, attempts=attempts - 1)
    except GeocoderQueryError:
        return address  # return address if geocoding is impossibe

    # pylint doesn't like the latitude and longitude attributes
    if not location:
        return _address
    if not location.latitude or not location.longitude:  # type: ignore
        return _address

    _address.latitude = location.latitude  # type: ignore
    _address.longitude = location.longitude  # type: ignore

    return _address


def geocode_with_google_maps(address: Address, api_key=None, attempts=3) -> Address:
    """
    Geocodes an address using the Google Maps API.
    The function recursively calls 3 times itself if the API returns an error.

    :param Address address: The address to be geocoded.
    :param str api_key: The Google Maps API key. (Optional)
    :return: A new address object with the lat and lon attributes populated.
    :rtype: Address
    """
    if attempts <= 0:
        return address

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": str(address), "key": api_key}
    _address = address.copy()

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("status") == "OK" and data.get("results"):
            result = data.get("results")[0]
            latitude = result.get("geometry").get("location").get("lat")
            longitude = result.get("geometry").get("location").get("lng")

            _address.latitude = latitude
            _address.longitude = longitude

    except (
        requests.RequestException,
        requests.ConnectionError,
        requests.HTTPError,
        requests.Timeout,
    ):
        return geocode_with_google_maps(address, attempts=attempts - 1)
    return _address


# NOTE: If you wanna use this, provide AWS credentials
def geocode_with_ip_rotation(address: Address) -> Address:
    """
    Geocodes an address using Nominatim with IP rotation.

    :param Address address: The address to be geocoded.
    :return: A new address object with the lat and lon attributes populated.
    :rtype: Address
    """
    url = "https://nominatim.openstreetmap.org/search"

    # Create gateway object and initialize in AWS
    gateway = ApiGateway(url)
    gateway.start()

    # Assign gateway to session
    session = requests.Session()
    session.mount(url, gateway)

    try:
        params = {"q": str(address), "format": "json", "limit": 1}

        response = session.get(url, params=params)
        response_json = response.json()

        if response.status_code == 200 and response_json:
            location = response_json[0]
            address.latitude = location["lat"]
            address.longitude = location["lon"]

    except (GeocoderTimedOut, GeocoderUnavailable):
        std_sleep(1)  # Delay if IP rotation rate is too high
        return geocode_with_ip_rotation(address)

    except GeocoderQueryError:
        return address  # Return the address if it can't be geocoded

    finally:
        # Shutdown the gateway
        gateway.shutdown()

    return address
