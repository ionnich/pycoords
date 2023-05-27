import argparse


def parse_args(args: list) -> argparse.Namespace:
    """
    Parse command line parameters.

    :param List[str] args: Command line parameters as list of strings (for example, ["--help"]).
    :return: Command line parameters namespace.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Gets the coordinates of venues via csv I/O"
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        help="File name of the input CSV",
        metavar="source_file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="geocoded.csv",
        help="File name of the output CSV",
        metavar="output_file",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="Set loglevel to DEBUG",
        action="store_const",
        const="DEBUG",
        required=False,
    )
    parser.add_argument(
        "-e",
        "--engine",
        type=str,
        help="Choose a geocoding engine to be used (nominatim, google)",
        metavar="engine",
        default="nominatim",
        required=False,
        choices=["nominatim", "google"],
    )
    parser.add_argument(
        "-p",
        "--parallel",
        dest="parallel",
        help="Set parallel processing to True",
        action="store_const",
        default=False,
        const="parallel",
        required=False,
    )
    return parser.parse_args(args)
