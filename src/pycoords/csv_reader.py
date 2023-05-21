import csv


def read_csv(file_name) -> list:
    """Reads a csv file and returns a dictionary of addresses.

    Args:
        file_name (str): The file name of the csv to be read.

    Returns:
        list: A list of dictionaries that store the attributes of addresses.
    """
    addresses = []

    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    except FileNotFoundError as e:
        raise e

    for row in data:
        addresses.append(
            {
                # TODO: @Aeinnor use dict.get()
                "name": row.get("name"),
                "address": row.get("address"),
                "city": row["city"],
                "state_code": row["state_code"],
                "postal_code": row["postal_code"],
                "country_code": row["country_code"],
            }
        )

    return addresses
