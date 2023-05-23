from time import sleep as std_sleep
from typing import Callable

import requests
from geopy import Nominatim
from geopy.exc import GeocoderQueryError, GeocoderTimedOut, GeocoderUnavailable
from requests_ip_rotator import ApiGateway

from pycoords.address import Address


def geocode_with_retry(max_attempts: int = 3, delay: int = 1) -> Callable:
    """
    A decorator that retries geocode if it fails.

    Args:
        max_attempts (int): The max attempts to geocode an address. Defaults to 3
        delay (int): The number of seconds to wait between attempts. Defaults to 1.

    Returns:
        function: geocode function with retry logic.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (GeocoderTimedOut, GeocoderUnavailable):
                    std_sleep(delay)
                    attempts += 1
                    continue
                except GeocoderQueryError:
                    return args[0]  # return the address if it can't be geocoded

        return wrapper

    return decorator


@geocode_with_retry()
def geocode_with_nominatim(address: Address) -> Address:
    """
    Geocodes an address using the Nominatim geocoder.

    Args:
        address (Address): The address to be geocoded.

    Returns:
        Address: A new address object with the lat and lon attributes populated.
    """

    geolocator = Nominatim(user_agent="pycoords")

    # copy address to an internal mutable object
    _address = address.copy()
    _address_str = str(_address)

    location = geolocator.geocode(_address_str)

    # pylint doesn't like the latitude and longitude attributes
    if location.latitude and location.longitude:  # type: ignore
        _address.latitude = location.latitude  # type: ignore
        _address.longitude = location.longitude  # type: ignore

    return _address


def geocode_with_google_maps(address: Address, api_key=None) -> Address:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {"address": str(address), "key": api_key}

    # TODO: @Aeinnor catch invalid api key and timeouts
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK" and data["results"]:
        result = data["results"][0]
        latitude = result["geometry"]["location"]["lat"]
        longitude = result["geometry"]["location"]["lng"]

        address.latitude = latitude
        address.longitude = longitude

    return address


# NOTE: If you wanna use this, provide AWS credentials
def geocode_with_ip_rotation(address: Address) -> Address:
    """
    Geocodes an address using Nominatim with IP rotation.

    Args:
        address (Address): The address to be geocoded.

    Returns:
        Address: A new address object with the lat and lon attributes populated.
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
