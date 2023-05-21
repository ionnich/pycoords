"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = pycoords.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""
import argparse
import logging
import sys

from pycoords import __version__, address_mapper, csv_reader, csv_writer

# from pycoords.coordinates import geocode

__author__ = "Aaron Gumapac, Aeinnor Reyes"
__copyright__ = "Aaron Gumapac, Aeinnor Reyes"
__license__ = "MIT"

_logger = logging.getLogger(__name__)
# NOTE: if you wanna use loguru instead of logging, you can do this:
# from loguru import logger as _logger
# set the name:
# _logger.name = __name__


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from pycoords.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    # TODO: @Aeinnor finish parse args
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"pycoords {__version__}",
    )
    parser.add_argument(dest="n", help="n-th Fibonacci number", type=int, metavar="INT")
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
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

    # NOTE: if you wanna use loguru instead of logging:
    # # set the level:
    # _logger.level(loglevel)
    # # set the format:
    # _logger.add(
    #     sys.stdout,
    #     format=logformat,
    #     level=loglevel,
    #     colorize=True,
    #     backtrace=True
    # )


def main(args):
    # TODO: @Aeinnor fix docs
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    # TODO: @Aeinnor change this according to argparse
    source_csv = args.source_csv

    try:
        unmapped_addresses: list = csv_reader.read_csv(source_csv)
        total_unmapped = len(unmapped_addresses)
    except FileNotFoundError:
        _logger.error("File not found: %s", source_csv)
        sys.exit(1)

    addresses: list = address_mapper.dict_to_address(unmapped_addresses)
    # TODO: @Aeinnor change this according to argparse

    # default filename
    output_filename = f"{source_csv}_geocoded.csv"
    if args.output:
        output_filename = args.output

    success_count: int = csv_writer.write_csv(addresses, output_filename)
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
