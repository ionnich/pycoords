import os
from csv import DictWriter

from loguru import logger


def write_csv(
    addresses: list, filename="geocoded_addresses.csv", logger=logger.debug
) -> int:
    """Writes the data found in a list of addresses into a csv file.

    Args:
        addresses (list): A list of addresses.

    Returns:
        int: The number of addresses written to the csv file.

    """
    filename = os.path.join(os.path.dirname(__file__), filename)
    count = 0

    if not addresses:
        return count

    with open(filename, "w", newline="") as file:
        fieldnames = addresses[0].schema()["properties"].keys()
        # first_address = addresses[0]
        # if first_address:
        #     fieldnames = first_address.schema()["properties"].keys()
        # else:
        #     logger("Addresses cannot be geocoded, please check your connection")
        #     raise SystemExit()

        writer = DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for address in addresses:
            if address.latitude != "" and address.longitude != "":
                count += 1

            writer.writerow(address.dict())

    return count
