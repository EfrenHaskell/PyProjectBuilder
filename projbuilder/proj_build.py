#!python

"""
CLI for package builder tool. Defines basic command line args and runs a build session.
"""

__author__ = "Efren"
__date__ = "6/13/2025"
__status__ = "development"
__version__ = "0.1"

import argparse
import file_parser as fp
from os import path
from pathlib import Path
from image import PriorityChain

HELP_MESSAGES: dict[str, str] = {
    "-f": "pyspec file name",
    "-u": "update project structure from pyspec file",
    "-w": "supress warnings when updating",
}


def handle_dir_not_exist(dir_name):
    """
    Check if specified dir_name exists and truly is a directory
    Creates directory if not
    Ensures project will be built in an existing home directory
    :param dir_name:
    """
    if not path.exists(dir_name) or not path.isdir(dir_name):
        Path(dir_name).mkdir(exist_ok=True)


def register_args(arg_parser):
    """
    :param arg_parser:
    """
    arg_parser.add_argument("-f", "--filename", required=True, type=str, help=HELP_MESSAGES["-f"])
    arg_parser.add_argument("-u", "--update", action="store_true", help=HELP_MESSAGES["-u"])
    arg_parser.add_argument("-w", "--warnings", action="store_true", help=HELP_MESSAGES["-w"])


def get_history():
    hist_path = ".data/spec.hist"
    if path.exists(hist_path):
        with open(hist_path, "r") as hist:
            return hist.readlines()
    return []


def compare(hist: list[str], spec: PriorityChain):



def save_history(spec_contents: str):
    with open(".data/spec.hist", "w") as file:
        file.write(spec_contents)


if __name__ == "__main__":
    description = ""
    parser = argparse.ArgumentParser(description=description)
    register_args(parser)
    args = parser.parse_args()
    new_session = fp.Session()
    chain = new_session.line_parse(args.filename)
    if not path.exists(".data"):
        Path(".data").mkdir()
    if args.update:
        history = get_history()
        compare(history, chain)
    else:
        new_session.process_all()
    save_history(str(chain))
