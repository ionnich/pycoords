from pydantic import BaseModel


class Address(BaseModel):
    """Address dataclass that corresponds to a venue address.

    Attributes:
        name (str | None): The name of the venue.
        address (str | None): The address of the venue.
        city (str | None): The city of the venue.
        state_code (str | None): The state code of the venue.
        postal_code (str | None): The postal code of the venue.
        country_code (str | None): The country code of the venue.
        latitude (str | None): The latitude of the venue.
        longitude (str | None): The longitude of the venue.
    """
    name: str | None = None
    address: str | None = None
    city: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    country_code: str | None = None
    latitude: str | None = None
    longitude: str | None = None

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state_code}, {self.postal_code}, {self.country_code}"


def dictionaries_to_addresses(dictionaries: list) -> list:
    """Converts a list of dictionaries to a list of addresses

    Args:
        dictionaries (list): A list of dictionaries that stores the venue details.

    Returns:
        list: A list of Address objects.
    """
    addresses = [Address(**row) for row in dictionaries]

    return addresses
