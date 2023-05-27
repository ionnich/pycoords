from pydantic import BaseModel, validator


class Address(BaseModel):
    """
    Address dataclass that corresponds to a venue address.

    :ivar str name: The name of the venue.
    :ivar str address: The address of the venue.
    :ivar str city: The city of the venue.
    :ivar str state_code: The state code of the venue.
    :ivar str country_code: The country code of the venue.
    :ivar str postal_code: The postal code of the venue.
    :ivar str phone: The phone number of the venue.
    :ivar str latitude: The latitude of the venue.
    :ivar str longitude: The longitude of the venue.
    """

    @validator("*")
    def none_to_empty(cls, _string: str) -> str:
        """
        Converts None values to empty strings.

        :param str _string: The string to convert.
        :return: The converted string.
        :rtype: str
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
        Builds a string of the address fit for geocoding fields.

        :return: A string representation of the address necessary for geocoding.
        :rtype: str
        """

        ignored_keys = ["phone", "name"]

        def ignore_fields(dictionary_item):
            key, value = dictionary_item
            return value != "" and key not in ignored_keys

        geocoding_fields = dict(filter(ignore_fields, self.dict().items()))
        accumulator = ", ".join(geocoding_fields.values())

        # remove trailing comma
        return accumulator.strip().rstrip(",")
