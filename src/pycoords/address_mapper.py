from pycoords.address import Address


def dict_to_address(dictionaries: list | dict) -> list:
    """Converts a list of dictionaries to a list of addresses

    Args:
        dictionaries (list): A list of dictionaries that stores the venue details.

    Returns:
        list: A list of Address objects.
    """

    if isinstance(dictionaries, dict):  # if only one dictionary is passed
        dictionaries = [dictionaries]

    return [Address(**row) for row in dictionaries]
