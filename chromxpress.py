#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Mathias Buff"
__version__ = "0.1.0"
__license__ = "MIT"

import struct

import argparse
import logzero
from logzero import logger


def main(args):
    """ Main entry point of the app """
    
    if args.output:
        destination_path = args.output
    else:
        destination_path = args.path.replace(".tsv", ".crcd")

    # logger verbosity setup
    logzero.loglevel(max(0, (30 - args.verbose*10)))
    if args.quiet:
        logzero.loglevel(100)

    logger.debug(f"Reading from input file: {args.path}")

    data = []
    with open(args.path, "r") as file:
        data = [
            [
                float(point.replace("\n", ""))
                for point in line.split("\t")
            ]
                for line in file.readlines()
                ]
    
    points_count = len(data)
    time_end = data[-1][0]
    frequency = 1 / (time_end * 60 / (points_count - 1))

    logger.info(f"Registered data. " +
                f"Length: {time_end} min. " +
                f"Frequency: {frequency} Hz."
                )
    logger.debug(f"Writing to output file: {destination_path}")

    with open(destination_path, "bw") as file:
        file.write(int(time_end).to_bytes(4))
        file.write(points_count.to_bytes(4))
        for datum in data:
            file.write(struct.pack('!f', datum[1]))
    
    logger.debug("Finished writing.")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("path", help="Input file path")

    # Optional argument flag which defaults to False
    parser.add_argument("-q", "--quiet", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-o", "--output", action="store", dest="output")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc.)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)