from pycoords.address import Address


def dict_to_address(dictionaries: list | dict) -> list:
    """
    Converts a list of dictionaries to a list of addresses.

    :param list dictionaries: A list of dictionaries that stores the venue details.
    :return: A list of Address objects.
    :rtype: list
    """

    if isinstance(dictionaries, dict):  # if only one dictionary is passed
        dictionaries = [dictionaries]

    return [Address(**row) for row in dictionaries]
