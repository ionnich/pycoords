import csv
import os


def read_csv(file_name) -> list:
    """Reads a csv file and returns a dictionary of addresses.

    Args:
        file_name (str): The file name of the csv to be read.

    Returns:
        list: A list of dictionaries that store the attributes of addresses.
    """
    file_name = os.path.join(os.path.dirname(__file__), file_name)
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
                "name": row.get("name"),
                "address": row.get("address"),
                "city": row.get("city"),
                "state_code": row.get("state_code"),
                "country_code": row.get("country_code"),
                "postal_code": row.get("postal_code"),
                "phone": row.get("phone"),
                "latitude": row.get("latitude"),
                "longitude": row.get("longitude"),
            }
        )

    return addresses
