from csv import DictWriter


def write_csv(addresses: list, filename="geocoded_addresses.csv") -> int:
    # TODO: @Aeinnor implement this
    """Writes the data found in a list of addresses into a csv file.

    Args:
        addresses (list): A list of addresses.

    Returns:
        int: The number of addresses written to the csv file.

    """
    count = 0

    if not addresses:
        return count

    with open(filename, "w", newline="") as file:
        fieldnames = addresses[0].schema()["properties"].keys()

        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for address in addresses:
            if address.latitude != "" and address.longitude != "":
                count += 1

            writer.writerow(address.dict())

    return count
