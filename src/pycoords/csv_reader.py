import csv


def read_csv(file_name):
    """Reads the data found in a csv file, converts them into addresses and stores them in a list.

    Args:
        file_name (str): The file name of the csv to be read.

    Returns:
        list: A list of dictionaries that store the attributes of addresses.
    """
    addresses = []

    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    for row in data:
        addresses.append(
            {"name": row["name"], "address": row["address"], "city": row["city"], "state_code": row["state_code"], "postal_code": row["postal_code"], "country_code": row["country_code"]})

    return addresses
