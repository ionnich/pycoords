from concurrent.futures import ThreadPoolExecutor
from os import cpu_count, getenv

from alive_progress import alive_bar as pbar
from alive_progress import alive_it as auto_bar
from dotenv import load_dotenv

from pycoords.address import Address
from pycoords.backends import geocode_with_google_maps, geocode_with_nominatim


def get_api_key() -> str:
    """
    Gets the Google Maps API key from the .env file or prompts the user to enter it.

    Returns:
        str : The Google Maps API key.
    """
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
    """
    Geocodes a list of addresses in parallel.

    Args:
        addresses (list): A list of addresses.
        backend (function): The geocoding backend to use.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.
    """
    workers = cpu_count()
    pbar_title = f"Concurrently processing with {workers} cores"
    bar_style = "filling"
    spinner_style = "notes"
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(backend, address) for address in addresses]
        results = list()
        with pbar(
            len(addresses), bar=bar_style, spinner=spinner_style, title=pbar_title
        ) as progress:
            for future, _ in zip(futures, addresses):
                progress()
                results.append(future.result())

    return results


def single_threaded_processing(addresses: list, backend) -> list:
    """
    Geocodes a list of addresses in a single thread.

    Args:
        addresses (list): A list of addresses.
        backend (function): The geocoding backend to use.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.
    """

    addresses = auto_bar(addresses, bar="filling")  # type: ignore
    return [backend(address) for address in addresses]


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

    if engine not in engines:
        raise SystemExit("Engine %s not supported" % engine)

    if isinstance(addresses, Address):
        addresses = [addresses]

    _queue = [address.copy() for address in addresses]

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
        return parallel_processing(_queue, backend)

    return single_threaded_processing(_queue, backend)
