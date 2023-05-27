import os
from csv import DictWriter


def write_csv(addresses: list, filename="geocoded_addresses.csv") -> int:
    """
    Writes the data found in a list of addresses into a CSV file.

    :param list addresses: A list of addresses.
    :return: The number of addresses written to the CSV file.
    :rtype: int
    """
    filename = os.path.join(os.path.dirname(__file__), filename)
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
