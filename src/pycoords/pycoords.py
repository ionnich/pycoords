import argparse
import re
import sys
from os import path

from loguru import logger as _logger

from pycoords.initialize import parse_args
from pycoords.address_mapper import dict_to_address
from pycoords.csv_reader import read_csv
from pycoords.csv_writer import write_csv
from pycoords.geocoder import geocode_addresses

__author__ = "Aaron Gumapac, Aeinnor Reyes"
__copyright__ = "Aaron Gumapac, Aeinnor Reyes"
__license__ = "MIT"

_logger.name = __name__  # type: ignore


def is_csv(file_name):
    """Checks if a file name ends with '.csv'

    Args:
        file_path (str): Path of the file to be validated.

    Returns:
        bool: True if the extension of the input is '.csv'. False otherwise.
    """
    csv_format = r"^.*\.csv$"
    return re.search(csv_format, file_name, re.IGNORECASE) is not None


def file_exists(file_name):
    return path.isfile(file_name) is not None


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    _logger.level("INFO")

    if loglevel:
        _logger.level(loglevel)


def main(args):
    """CLI program that takes a CSV file that stores venues as input
    and returns a new CSV file with the coordinates of the venues.

    Args:
      args (List[str]): Command line parameters as list of strings.
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    
    if not is_csv(args.source):
        _logger.error("Input is not a CSV file -> exiting")
        sys.exit(1)

    source_csv = args.source
    
    if engine := args.engine:
        _logger.info("Using %s as geocoding engine", engine)
    else:
        engine = "nominatim"

    if not file_exists(source_csv):
        _logger.error("%s is invalid", source_csv)

    unmapped_addresses: list = read_csv(source_csv)
    total_unmapped = len(unmapped_addresses)
    addresses: list = dict_to_address(unmapped_addresses)

    try:
        parsed_addresses: list = geocode_addresses(addresses, engine=engine)
    except ValueError as e:
        _logger.error(e)
        sys.exit()

    output_filename = f"{source_csv}_geocoded.csv"
    if is_csv(args.output):
        output_filename = args.output
    else:
        _logger.warning("File extension must be .csv -> using %s", output_filename)

    success_count: int = write_csv(parsed_addresses, output_filename)

    _logger.info(
        "Successfully geocoded %d/%d addresses to %s",
        success_count,
        total_unmapped,
        output_filename,
    )


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function iss used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # NOTE:
    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #     python -m pycoords.skeleton 42
    #
    run()
