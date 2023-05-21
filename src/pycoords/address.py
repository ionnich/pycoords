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
    def none_to_empty(cls, _string: str):
        """Converts None values to empty strings.

        Args:
            _string (str): The string to convert.

        Returns:
            str: The converted string.
        """

        _string = _string.strip()

        return _string or ""

    name: str
    address: str
    city: str
    state_code: str
    postal_code: str
    country_code: str
    latitude: str = ""
    longitude: str = ""

    def __str__(self):
        """
        Builds a string of address attributes for values that are not None.

        Returns:
            str: A string representation of the address.
        """

        accumulator = ""
        for attribute in self.__dict__:
            value = getattr(self, attribute)  # get value of attribute

            if value:
                accumulator += f"{value}, "

        # remove trailing comma and space
        return accumulator.strip().rstrip(",")
