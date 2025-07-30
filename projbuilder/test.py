#!python

"""
Test file
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

import test_utils


if __name__ == "__main__":
    test_utils.reset_session()
    new_spec = test_utils.create_spec()
    new_spec
