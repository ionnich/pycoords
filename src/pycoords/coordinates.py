from geopy import Nominatim

from pycoords.address import Address


def geocode(address: Address) -> Address:
    """Initialize coordinates from address."""

    # copy address to an internal mutable object
    _address = address.copy()

    geolocator = Nominatim(user_agent="pycoords")

    # _address_str = str(_address)

    location = geolocator.geocode(_address)

    if not location:
        return _address

    _address.latitude = location.latitude  # type: ignore
    _address.longitude = location.longitude  # type: ignore

    return _address
