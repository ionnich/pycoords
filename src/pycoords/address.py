from pydantic import BaseModel, validator


class Address(BaseModel):
    """Address dataclass that corresponds to a venue address.

    Attributes:
        name (str): The name of the venue.
        address (str): The address of the venue.
        city (str): The city of the venue.
        state_code (str): The state code of the venue.
        country_code (str): The country code of the venue.
        postal_code (str): The postal code of the venue.
        phone (str): The phone number of the venue.
        latitude (str): The latitude of the venue.
        longitude (str): The longitude of the venue.
    """

    @validator("*")
    def none_to_empty(cls, _string: str):
        """Converts None values to empty strings.

        Args:
            _string (str): The string to convert.

        Returns:
            str: The converted string.
        """

        try:
            _string = _string.strip()
        except AttributeError:
            pass

        return _string or ""

    name: str | None
    address: str | None
    city: str | None
    state_code: str | None
    country_code: str | None
    postal_code: str | None
    phone: str | None
    latitude: str | None = ""
    longitude: str | None = ""

    def __str__(self):
        """
        Builds a string of the address fit for geocoding fields

        Returns:
            str: A string representation of the address necessary for geocoding.
        """

        ignored_keys = ["phone", "name"]

        def ignore_fields(dictionary_item):
            key, value = dictionary_item
            return value != "" and key not in ignored_keys

        geocoding_fields = dict(filter(ignore_fields, self.dict().items()))
        accumulator = ", ".join(geocoding_fields.values())

        # remove trailing comma
        return accumulator.strip().rstrip(",")
