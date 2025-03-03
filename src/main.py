#!/usr/bin/env python3
"""
Main Python script to make font
"""

import sys
import logging
from argparse import ArgumentParser
from log import StreamToLogger
from factory.generator import Generator
from factory.patcher import Patcher

DEBUG_FILE = "debug.log"


def parse_args():
    """Parse arguments from command line"""
    parser = ArgumentParser()
    parser.add_argument(
        "base_font_file",
        type=str,
        metavar="PATH",
        help="The TTF or OTF font to add ligatures to.",
    )
    parser.add_argument(
        "ligature_font_file",
        type=str,
        metavar="PATH",
        help="The OTF font to copy ligatures from.",
    )
    parser.add_argument(
        "--name",
        "-n",
        type=str,
        default="",
        help="Name of the generated font. Completely replaces the original.",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        type=str,
        default="",
        help="String to prefix the name of the generated font with.",
    )
    parser.add_argument(
        "--suffix",
        "-s",
        type=str,
        default="",
        help="String to suffix the name of the generated font with.",
    )
    parser.add_argument(
        "--directory",
        "-D",
        help="The directory to save the ligaturized font in."
        " The actual filename will be automatically generated"
        " based on the --suffix and the --prefix and"
        " --output-name flags.",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Enable debug outputs.",
    )
    return parser.parse_args()


def main(
    base_font_file, ligature_font_file, name, prefix, suffix, directory, debug, **kwargs
):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    handler = logging.FileHandler(DEBUG_FILE, "w", "utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    stdout_logger = logging.getLogger("STDOUT")
    stdout_logger.setLevel(level)
    stdout_logger.addHandler(handler)
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    if debug:
        stderr_logger = logging.getLogger("STDERR")
        stderr_logger.setLevel(level)
        stderr_logger.addHandler(handler)
        sl = StreamToLogger(stderr_logger, logging.ERROR)
        sys.stderr = sl

    patcher = Patcher(base_font_file, ligature_font_file)
    patcher.patch()
    generator = Generator(patcher.base_font)
    generator.update_font_metadata(prefix, name, suffix)
    generator.generate(directory)


if __name__ == "__main__":
    main(**vars(parse_args()))
