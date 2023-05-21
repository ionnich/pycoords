from typing import Optional

from pydantic import BaseModel, validator


class Address(BaseModel):
    # TODO: Address object must be 1 to 1 to the csv object aside from the coordinates
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

    @validator("*")
    def nullify_empty_strings(cls, _string: str):
        """Replaces empty strings with None

        Args:
            v (str): The value of the field.

        Returns:
            str | None: The value of the field or None.
        """
        _string = _string.strip()
        return None if not _string else _string

    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state_code: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]

    def __str__(self):
        """
        Builds a string of address attributes for values that are not None.

        Returns:
            str: A string representation of the address.
        """

        accumulator = ""
        for attribute in self.__dict__:
            value = getattr(self, attribute)  # get value of attribute

            if value is not None:
                accumulator += f"{value}, "

        # remove trailing comma and space
        return accumulator.strip().rstrip(",")
