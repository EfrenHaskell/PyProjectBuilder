#!python

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
from os import sep
import context_utils as ctx_utils


class MetaVars(Enum):
    Home_dir = auto()
    Venv_nm = auto()
    Git_dir = auto()
    Git_name = auto()
    Git_origin = auto()
    Git_branch = auto()


class Opts:

    def __init__(self):
        self.meta = {
            MetaVars.Home_dir: ctx_utils.FileStructure("."),
            MetaVars.Venv_nm: f".{sep}venv",
            MetaVars.Git_dir: "default",
            MetaVars.Git_name: "",
            MetaVars.Git_origin: "",
            MetaVars.Git_branch: "main",
        }

    @staticmethod
    def map_metavar(meta_string: str):
        if meta_string == "home_dir":
            return MetaVars.Home_dir
        elif meta_string == "venv_name":
            return MetaVars.Venv_nm
        elif meta_string == "git_dir":
            return MetaVars.Git_dir
        elif meta_string == "git_name":
            return MetaVars.Git_name
        elif meta_string == "git_origin":
            return MetaVars.Git_origin
        elif meta_string == "git_branch":
            return MetaVars.Git_branch
        else:
            raise Exception(f"No such option {meta_string}")
