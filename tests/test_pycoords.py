import csv
import os

from pycoords.pycoords import is_csv, main

test_dir = os.path.dirname(os.path.abspath(__file__))
default_test_path = os.path.join(test_dir, "default_geocoded.csv")


def csv_reader(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    return data


def test_is_csv():
    assert is_csv("sample.csv") is True
    assert is_csv("text.txt") is False


def test_main():
    input_sample = os.path.join(test_dir, "sample.csv")

    # testing default behavior (only required fields provided)
    arguments = ["-s", input_sample]
    main(arguments)

    csv_file_path = os.path.join(test_dir, "sample_geocoded.csv")

    test_default_file = csv_reader(csv_file_path)
    default_test_data = csv_reader(default_test_path)

    assert test_default_file == default_test_data
