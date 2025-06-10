#!usr/bin/env Python

"""
Test utils
Creates and resets session and initializes test folder for testing functionality
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

import shutil
import file_parser as fp
from pathlib import Path
from os import sep, path, remove
from meta import MetaVars
from contexts import FileStructure
from image import PriorityChain


def reset_session():
    """
    Remove redundant files and directories
    """
    shutil.rmtree(f".{sep}test")
    if path.exists(f".{sep}requirements.txt"):
        remove(f".{sep}requirements.txt")


def create_session() -> fp.Session:
    """
    Create test directory and set meta vars
    """
    Path(f".{sep}test").mkdir(exist_ok=True)
    new_session = fp.Session()
    new_session.meta[MetaVars.Home_dir] = FileStructure(f".{sep}test")
    return new_session


def print_chain(chain: PriorityChain):
    """
    Print string representation of priority chain
    """
    for priority_group in chain.internal:
        for image in priority_group:
            print(image.context)
            print("\n - ".join(image.task_list))
