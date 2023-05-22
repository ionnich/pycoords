from time import sleep as std_sleep
from typing import Callable

from geopy import Nominatim
from geopy.exc import GeocoderQueryError, GeocoderTimedOut, GeocoderUnavailable

from pycoords.address import Address


def geocode_addresses(addresses: list) -> list:
    """Geocodes a list of addresses.

    Args:
        addresses (list): A list of addresses.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.
    """
    if isinstance(addresses, Address):
        addresses = [addresses]

    return [geocode(address) for address in addresses]


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
def geocode(address: Address) -> Address:
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
