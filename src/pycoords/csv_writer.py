def write_csv(addresses: list, filename="geocoded_addresses.csv") -> int:
    # TODO: @Aeinnor implement this
    """Writes the data found in a list of addresses into a csv file.

    Args:
        addresses (list): A list of addresses.

    Returns:
        int: The number of addresses written to the csv file.

    """

    # TODO: Placeholder, delete when you implemenet
    print(filename)

    # TODO: Add counter for number of addresses that have None for lat and lon
    count = 0
    if not addresses:
        return count

    return count
