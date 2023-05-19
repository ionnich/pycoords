from typing import Any, Dict

from pydantic import BaseModel


def address_from_string(s: str):
    address_dict: Dict[str, Any] = {
        "name": None,
        "address": None,
        "city": None,
        "state_code": None,
        "postal_code": None,
        "country_code": None,
        "latitude": None,
        "longitude": None,
    }

    substrings = s.split(",")

    for i, entry in enumerate(substrings):
        if entry:
            key = list(address_dict.keys())[i]  # get the ith key from address_dict
            address_dict[key] = entry.strip()

    return Address(**address_dict)


class Address(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    country_code: str | None = None
    latitude: str | None = None
    longitude: str | None = None

    def add_name(self, name: str):
        self.name = name
        return self

    def add_address(self, address: str):
        self.address = address
        return self

    def add_city(self, city: str):
        self.city = city
        return self

    def add_state_code(self, state_code: str):
        self.state_code = state_code
        return self

    def add_postal_code(self, postal_code: str):
        self.postal_code = postal_code
        return self

    def add_country_code(self, country_code: str):
        self.country_code = country_code
        return self

    def add_latitude(self, latitude: str):
        self.latitude = latitude
        return self

    def add_longitude(self, longitude: str):
        self.longitude = longitude
        return self

    def __str__(self):
        pass

    # TODO: @aein return the right f string
    # return f""
