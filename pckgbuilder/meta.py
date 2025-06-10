#!usr/bin/env Python

"""
Misc code
 - Potential updates:
    - Have metadata builder from conf files
    - Could provide better customization capabilities for Custom Contexts
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

from enum import Enum, auto


class MetaVars(Enum):
    Home_dir = auto()
    Venv_nm = auto()

