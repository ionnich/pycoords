from concurrent.futures import ThreadPoolExecutor
from os import cpu_count, getenv

from dotenv import load_dotenv

from pycoords.address import Address
from pycoords.backends import geocode_with_google_maps, geocode_with_nominatim


def get_api_key() -> str | None:
    load_dotenv()

    if api_key := getenv("GOOGLE_MAPS_API_KEY"):
        return api_key
    else:
        api_key = input("Enter your Google Maps API key: ")

        # create .env file
        with open(".env", "w") as f:
            f.write(f"GOOGLE_MAPS_API_KEY={api_key}")

    return api_key


def parallel_processing(addresses: list, backend) -> list:
    workers = cpu_count()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(backend, addresses)

    return list(results)


def geocode_addresses(
    addresses: list, engine="nominatim", api_key=None, parallel=True
) -> list:
    """Geocodes a list of addresses.

    Args:
        addresses (list): A list of addresses.
        engine (str, optional): The geocoding engine to use. Defaults to "nominatim".
        api_key (str, optional): The Google Maps API key. Defaults to None.
        parallel (bool, optional): Whether to use parallel processing. Defaults to True.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.

    Raises:
        ValueError: If the engine is not supported.
    """
    engines = {
        "nominatim": geocode_with_nominatim,
        "google": geocode_with_google_maps,
    }

    if isinstance(addresses, Address):
        addresses = [addresses]

    if engine not in engines:
        raise SystemExit("Engine %s not supported" % engine)

    backend = engines[engine]

    if engine == "google":
        if not api_key:
            api_key = get_api_key()

        def backend(address):
            return geocode_with_google_maps(address, api_key)

        backend = backend
    else:
        # NOTE: Support for other engines is to come
        parallel = False

    if parallel:
        return parallel_processing(addresses, backend)

    return [backend(address) for address in addresses]
