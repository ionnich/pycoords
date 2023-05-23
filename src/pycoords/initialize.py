import argparse


def parse_args(args: list) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = argparse.ArgumentParser(
        description="Gets the coordinates of venues via csv I/O"
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        help="file name of the input CSV",
        metavar="source_file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="geocoded.csv",
        help="file name of the output CSV",
        metavar="output_file",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const="DEBUG",
        required=False,
    )
    parser.add_argument(
        "-e",
        "--engine",
        type=str,
        help="geocoding engine used",
        metavar="engine",
        default="nominatim",
        required=False,
        choices=["nominatim", "google"],
    )
    parser.add_argument(
        "-p",
        "--parallel",
        dest="parallel",
        help="set parallel processing to True",
        action="store_const",
        default=False,
        const="parallel",
        required=False,
    )
    return parser.parse_args(args)
