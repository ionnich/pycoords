from concurrent.futures import ThreadPoolExecutor
from os import cpu_count, getenv
from pathlib import Path

from alive_progress import alive_bar as pbar
from alive_progress import alive_it as auto_bar
from dotenv import load_dotenv

from pycoords.address import Address
from pycoords.backends import geocode_with_google_maps, geocode_with_nominatim


def get_api_key() -> str:
    """
    Gets the Google Maps API key from the .env file or prompts the user to enter it.

    :return: The Google Maps API key.
    :rtype: str
    """
    load_dotenv(dotenv_path=Path(".env"))

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

    :param list addresses: A list of addresses.
    :param Callable backend: The geocoding backend to use.
    :return: A list of addresses with the lat and lon attributes populated.
    :rtype: list
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

    :param list addresses: A list of addresses.
    :param Callable backend: The geocoding backend to use.
    :return: A list of addresses with the lat and lon attributes populated.
    :rtype: list
    """
    addresses = auto_bar(addresses, bar="filling")  # type: ignore
    return [backend(address) for address in addresses]


def remove_geocoded(addresses: list) -> tuple:
    """
    Removes addresses that have already been geocoded.

    :param list addresses: A list of addresses.
    :return: A tuple containing a list of unparsed addresses and their indices.
    :rtype: tuple
    """
    unparsed_addresses = list()
    indices = list()

    for index, address in enumerate(addresses):
        if not address.latitude and not address.longitude:
            unparsed_addresses.append(address)
            indices.append(index)

    return unparsed_addresses, indices


def get_position_in(addresses: list, address: Address) -> int:
    """
    Gets the position of an address in a list of addresses.

    :param list addresses: A list of addresses.
    :param Address address: The address to find.
    :return: The position of the address in the list of addresses.
    :rtype: int
    """
    print("getting index")
    return addresses.index(address)


def generate_coordinates(
    addresses: list, engine="nominatim", api_key=None, parallel=True
) -> list:
    """
    Wrapper for geocoding functions.

    :param list addresses: A list of addresses.
    :param str engine: The geocoding engine to use. (Optional, defaults to "nominatim")
    :param str api_key: The Google Maps API key. (Optional, defaults to None)
    :param bool parallel: Whether to use parallel processing. (Optional, defaults to True)
    :return: A list of addresses with the lat and lon attributes populated.
    :rtype: list
    :raises SystemExit: If the engine is not supported.
    """
    engines = {
        "nominatim": geocode_with_nominatim,
        "google": geocode_with_google_maps,
    }

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

    return single_threaded_processing(addresses, backend)


def geocode_addresses(
    addresses: list, engine="nominatim", api_key=None, parallel=True
) -> tuple:
    """
    Geocodes a list of addresses.

    :param list addresses: A list of addresses.
    :param str engine: The geocoding engine to use. (Optional, defaults to "nominatim")
    :param str api_key: The Google Maps API key. (Optional, defaults to None)
    :param bool parallel: Whether to use parallel processing. (Optional, defaults to True)
    :return: A tuple containing a list of addresses and a count of geocoded addresses.
    :rtype: tuple
    :raises ValueError: If the engine is not supported.
    """
    if isinstance(addresses, Address):
        addresses = [addresses]

    _queue = list(addresses)

    _unparsed_queue, _unparsed_indices = remove_geocoded(_queue)
    _unparsed_queue = generate_coordinates(_unparsed_queue, engine, api_key, parallel)

    success_counter = 0
    for item in _unparsed_queue:
        if item.latitude and item.longitude:
            success_counter += 1

    # Combine the parsed and unparsed addresses while preserving the order
    for index in _unparsed_indices:
        _queue[index] = _unparsed_queue.pop(0)

    return (_queue, success_counter)
