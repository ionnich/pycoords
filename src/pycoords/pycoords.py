import re
import sys
from os import path

from loguru import logger as _logger

from pycoords.address_mapper import dict_to_address
from pycoords.csv_reader import read_csv
from pycoords.csv_writer import write_csv
from pycoords.geocoder import geocode_addresses
from pycoords.initialize import parse_args

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
    """Checks if a file exists in current directory"""
    file_name = path.join(path.dirname(__file__), file_name)
    return path.exists(file_name)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    _logger.remove()
    level = "DEBUG" if loglevel else "INFO"
    if loglevel:
        _logger.add("pycoords.log", level="DEBUG")

    _logger.add(sys.stderr, level=level)


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
        _logger.info("Using %s as geocoding engine" % engine)

    if not file_exists(source_csv):
        _logger.error("%s is invalid -> exiting" % source_csv)
        sys.exit(1)

    unmapped_addresses: list = read_csv(source_csv)
    addresses: list = dict_to_address(unmapped_addresses)
    unparsed_addresses = [
        address
        for address in addresses
        if not address.latitude or not address.longitude
    ]

    total_rows = len(unmapped_addresses)
    total_unmapped = len(unparsed_addresses)
    _logger.debug("Addresses in %s : %d" % (source_csv, total_rows))
    _logger.debug("Addresses to be geocoded: %d" % total_unmapped)

    parsed_addresses: list = geocode_addresses(
        addresses, engine=engine, parallel=args.parallel
    )

    _logger.debug("Processed addresses: %d" % len(parsed_addresses))

    output_filename = source_csv.rstrip(".csv") + "_geocoded.csv"
    DEFAUlT_OUTPUT = "geocoded.csv"
    if is_csv(args.output):
        output_filename = (
            args.output if args.output != DEFAUlT_OUTPUT else output_filename
        )
    else:
        _logger.warning(
            "Output file extension must be .csv -> using %s" % output_filename
        )

    success_count: int = write_csv(parsed_addresses, output_filename)

    _logger.info(
        "Successfully geocoded %d/%d addresses to %s"
        % (success_count, total_unmapped, output_filename)
    )
    _logger.info("Altered %d/%d addresses" % (success_count, total_rows))


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    # NOTE:
    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #     python -m pycoords.skeleton 42
    #
    run()
