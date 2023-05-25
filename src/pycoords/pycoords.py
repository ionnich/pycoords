import re
import sys
from os import chdir, getcwd, path
from time import perf_counter

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
    current_dir = path.abspath(getcwd())
    pycoords_dir = path.dirname(path.abspath(__file__))
    file_name = path.join(current_dir, file_name)
    _logger.debug("Locating file in: ...%s" % file_name[5:])
    _logger.debug("Locating dir in: ...%s" % pycoords_dir)
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

    current_dir = path.abspath(getcwd())
    source_csv = path.join(current_dir, source_csv)

    if engine := args.engine:
        _logger.info("Using %s as engine" % engine)

    if not file_exists(source_csv):
        _logger.error("%s is invalid -> exiting" % source_csv)
        sys.exit(1)

    start = perf_counter()
    csv_rows: list = read_csv(source_csv)
    total_rows = len(csv_rows)
    _logger.debug("Reading %d rows from %s" % (total_rows, source_csv))
    addresses: list = dict_to_address(csv_rows)
    total_addresses = len(addresses)
    _logger.debug(
        "Number of Address objects instantiated in memory %d" % total_addresses
    )

    parsed_addresses, total_parsed = geocode_addresses(
        addresses, engine=engine, parallel=args.parallel
    )
    _logger.info("Processed addresses: %d/%d" % (total_parsed, total_rows))

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
    end = perf_counter()
    _logger.info(
        "%d/%d addresses now have coordinates in %s"
        % (success_count, total_rows, output_filename)
    )
    _logger.debug("Finished in: %.2f seconds" % (end - start))


def run():
    # change working directory to current directory
    running_directory = getcwd()
    chdir(running_directory)
    _logger.debug("Pycoords is running in: %s" % running_directory)
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
