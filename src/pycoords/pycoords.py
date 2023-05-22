import argparse
from loguru import logger as _logger
import sys
import os
import re

from pycoords import address_mapper, csv_reader, csv_writer, geocoder

# from pycoords.coordinates import geocode

__author__ = "Aaron Gumapac, Aeinnor Reyes"
__copyright__ = "Aaron Gumapac, Aeinnor Reyes"
__license__ = "MIT"

_logger.name = __name__


def is_csv(file_name):
    """_summary_

    Args:
        file_path (str): Path of the file to be validated.

    Returns:
        bool: True if the extension of the input is '.csv'. False otherwise.
    """
    csv_format = r"^.*\.csv$"
    return re.search(csv_format, file_name, re.IGNORECASE) is not None


def parse_args(args: list) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(
        description="Gets the coordinates of venues via csv I/O")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        help="File name of the input CSV",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="File name of the output CSV",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    # TODO: @Aeinnor Setup logger
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    _logger.level(loglevel)
    _logger.add(
        sys.stdout,
        format=Logformat,
        Level=Loglevel,
        colorize=True,
        backtrace=True,
    )


def main(args):
    # TODO: @Aeinnor fix docs
    """CLI program that takes a CSV file that stores venues as input and returns a new CSV file with the coordinates of the venues.

    Args:
      args (List[str]): Command line parameters as list of strings.
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    if not is_csv(args.source_csv):
        sys.exit("Input is not a CSV file")

    source_csv = args.source_csv

    try:
        unmapped_addresses: list = csv_reader.read_csv(source_csv)
        total_unmapped = len(unmapped_addresses)
    except FileNotFoundError:
        _logger.error("File not found: %s", source_csv)
        sys.exit(1)

    addresses: list = address_mapper.dict_to_address(unmapped_addresses)
    parsed_addresses: list = geocoder.geocode_addresses(addresses)

    # default filename
    output_filename = f"{source_csv}_geocoded.csv"
    if is_csv(args.output):
        output_filename = args.output
    else:
        _.logger.error(
            "File extension must be .csv, output file name will be set to default")

    success_count: int = csv_writer.write_csv(parsed_addresses, output_filename)
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
