from concurrent.futures import ThreadPoolExecutor
from os import cpu_count, getcwd, getenv, path

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
    # change directory to current directory
    running_directory = getcwd()
    # load environment variables from .env file
    load_dotenv(dotenv_path=path.join(running_directory, ".env"))

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


def remove_geocoded(addresses: list) -> tuple:
    """
    Removes addresses that have already been geocoded.

    Args:
        addresses (list): A list of addresses.

    Returns:
        tuple: a list of unparsed addresses and their indices
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

    Args:
        addresses (list): A list of addresses.
        address (Address): The address to find.

    Returns:
        int: The position of the address in the list of addresses.
    """
    print("getting index")
    return addresses.index(address)


def generate_coordinates(
    addresses: list, engine="nominatim", api_key=None, parallel=True
) -> list:
    """
    Wrapper for geocoding functions.

    Args:
        addresses (list): A list of addresses.
        engine (str, optional): The geocoding engine to use. Defaults to "nominatim".
        api_key (str, optional): The Google Maps API key. Defaults to None.
        parallel (bool, optional): Whether to use parallel processing. Defaults to True.

    Returns:
        list: A list of addresses with the lat and lon attributes populated.
    Raises:
        SystemExit: If the engine is not supported.
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
    """Geocodes a list of addresses.

    Args:
        addresses (list): A list of addresses.
        engine (str, optional): The geocoding engine to use. Defaults to "nominatim".
        api_key (str, optional): The Google Maps API key. Defaults to None.
        parallel (bool, optional): Whether to use parallel processing. Defaults to True.

    Returns:
        tuple: A tuple containing a list of addresses and a count of geocoded addresses

    Raises:
        ValueError: If the engine is not supported.
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
