#!python

"""
Test utils
Creates and resets session and initializes test folder for testing functionality
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

import shutil
from pathlib import Path
from os import sep, path, remove
import spec


def reset_session():
    """
    Remove redundant files and directories
    """
    if path.exists(f".{sep}test") and path.isdir(f".{sep}test"):
        shutil.rmtree(f".{sep}test")
    if path.exists(f".{sep}requirements.txt"):
        remove(f".{sep}requirements.txt")


def create_spec() -> spec.Spec:
    """
    Create test directory and set meta vars
    """
    Path(f".{sep}test").mkdir(exist_ok=True)
    return spec.Spec()
