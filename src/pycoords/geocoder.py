from geopy import Nominatim

from pycoords.address import Address


def geocode_addresses(addresses: list) -> list:
    """Geocodes a list of addresses.

    Args:
        addresses (list): A list of addresses.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.
    """

    return [geocode(address) for address in addresses]


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

    if not location:
        return _address

    # pylint doesn't like the latitude and longitude attributes
    if location.latitude and location.longitude:  # type: ignore
        _address.latitude = location.latitude  # type: ignore
        _address.latitude = location.longitude  # type: ignore

    return _address
