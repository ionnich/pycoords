from os import environ

from dotenv import load_dotenv

from pycoords.address import Address
from pycoords.backends import geocode_with_google_maps, geocode_with_nominatim


def get_api_key() -> str | None:
    # TODO: @Aeinnor get api key from environmental variables
    load_dotenv()

    if api_key := environ.get("GOOGLE_MAPS_API_KEY"):
        return api_key
    else:
        api_key = input("Enter your Google Maps API key: ")

        # create .env file
        with open(".env", "w") as f:
            f.write(f"GOOGLE_MAPS_API_KEY={api_key}")

    return api_key


def geocode_addresses(addresses: list, engine="nominatim", api_key=None) -> list:
    """Geocodes a list of addresses.

    Args:
        addresses (list): A list of addresses.
        engine (str, optional): The geocoding engine to use. Defaults to "nominatim".

    Returns:
        list: A list of addresses with the lat and lon attributes populated.

    Raises:
        ValueError: If the engine is not supported.
    """
    engines = {
        "nominatim": geocode_with_nominatim,
        "google": geocode_with_google_maps,
    }

    backend = engines.get(engine)

    if not backend:
        raise SystemExit("Engine %s not supported", backend)

    if engine == "google":
        if not api_key:
            api_key = get_api_key()

        def backend(address):
            return geocode_with_google_maps(address, api_key)

        backend = backend

    if isinstance(addresses, Address):
        addresses = [addresses]

    return [backend(address) for address in addresses]
