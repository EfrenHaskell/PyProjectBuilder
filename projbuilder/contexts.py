#!python

"""
Context objects and utilities for context operations
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"


from pathlib import Path
import re
from os import chdir, remove
import venv
import sys
import subprocess
import datetime
# from meta import Opts, MetaVars
import objects as obj
from typing import Any


class Context:
    """
    Base class for Context
    Lists functionality to be included in context objects
    """
    def __init__(self, opts):
        self.children: list[obj.Obj] = []
        self.opts = opts

    def exec(self):
        for child in self.children:
            child.exec(self.opts)
        self.exit_context()

    def exit_context(self):
        """
        Defines end of context procedure
        """
        pass

    @staticmethod
    def extended_tokenize(line):
        return re.split(r"(\s+)", line)


class FSContext(Context):
    """
    Context for file structure creation
    """

    def __init__(self, new_path: obj.PathObj, opts=None):
        super().__init__(opts)
        self.path = new_path


class PipContext(Context):
    pass


class OptContext(Context):
    pass


# class GitContext(Context):
#
#     """
#     Context for git initializationZ
#     """
#     def __init__(self, new_path: obj.PathObj, generics=None):
#         self.path = new_path
#         self.branch_maker: obj.PathObj = obj.PathObj("/", "")
#         self.enter_context()
#
#     def enter_context(self):
#         pass
#
#     def __enter_dir(self):
#         if self.opt.meta[MetaVars.Git_dir] != self.fs.home:
#             if self.opt.meta[MetaVars.Git_dir] == "default":
#                 chdir(self.fs.make_path(""))
#             else:
#                 chdir(self.fs.make_path(self.opt.meta[MetaVars.Git_dir]))
#
#     def init_repo(self):
#         self.__enter_dir()
#         subprocess.run(["git", "init"])
#         with open("temp.md", "w") as file:
#             file.write("Updates coming soon...")
#         subprocess.run(["git", "add", "temp.md"])
#         subprocess.run(["git", "commit", "-m", "Setup"])
#         self.init_main_branch()
#
#     def add_readme(self):
#         with open("README.md", "w") as file:
#             contents = "\n".join(self.readme_text)
#             file.write(f"# {self.opt.meta[MetaVars.Git_name]}\n{contents}")
#
#     def add_gitignore(self):
#         with open(".gitignore", "w") as file:
#             file.write("\n".join(self.ignore))
#
#     def gitignore(self, line):
#         self.ignore.append(line)
#
#     def readme(self, line):
#         self.readme_text.append(line)
#
#     @staticmethod
#     def init_main_branch():
#         subprocess.check_call(["git", "branch", "-M", "main"])
#
#     def add_origin(self):
#         subprocess.check_call(["git", "remote", "add", "origin", self.opt.meta[MetaVars.Git_origin]])
#
#     def enter(self, nest_group: str):
#         self.git_bs.enter(nest_group)
#
#     def leave(self):
#         self.git_bs.leave()
#
#     def new_branch(self, name: str):
#         subprocess.check_call(["git", "branch", name])
#         self.most_recent_nest = name
#
#     def push(self):
#         subprocess.run(["git", "add", "."])
#         subprocess.run(["git", "commit", "-m", "Push project items"])
#         if self.opt.meta[MetaVars.Git_branch] == "":
#             subprocess.run(["git", "push", "-u", "origin", "main"])
#         else:
#             subprocess.run(["git", "push", "origin", self.opt.meta[MetaVars.Git_branch]])
#
#     def branches(self, task: str):
#         if task == "->":
#             self.git_bs.enter(self.most_recent_nest)
#         elif task == "<-":
#             self.git_bs.leave()
#         else:
#             task_elements = task.split(" ")
#             if len(task_elements) < 2:
#                 raise Exception("Missing required positional argument")
#             name = task_elements[1]
#             if task_elements[0] == "nest":
#                 self.most_recent_nest = name
#             elif task_elements[0] == "branch":
#                 self.new_branch(self.git_bs.make_path(name))
#
#     def map(self, line):
#         if line[:2] == "//":
#             self.sub_map.switch(line[2:].strip().lower())
#         else:
#             self.sub_map.exec([line])
#
#     def exit_context(self):
#         subprocess.run(["git", "reset"])
#         if self.fs.not_empty():
#             remove("temp.md")
#         self.add_readme()
#         self.add_gitignore()
#         if self.opt.meta[MetaVars.Git_origin] != "":
#             self.push()
#
#
# class MLDundersContext(Context):
#
#     """
#     Context for creating module-level dunders
#     Certain dunders with default values will be added by default
#     """
#     def __init__(self, template):
#         self.default: dict[str, str] = {}
#
#         self.dunder_list = [python_loc, "\n\"\"\"\nDescription here...\n\"\"\"\n"]
#         date_time = datetime.datetime.now()
#         date_str = f"{date_time.month}/{date_time.day}/{date_time.year}"
#         self.dunders: dict[str, str] = {
#             "all": "",
#             "annotations": "",
#             "author": "",
#             "credits": "",
#             "date": date_str,
#             "status": "development",
#             "version": 0.1,
#         }
#         self.template: PyFileTemplate = template
#
#     def __str__(self):
#         return "mldunders"
#
#     @staticmethod
#     def __dunder_expression(dunder: str, value: str):
#         return f"__{dunder}__ = \"{value}\""
#
#     def map(self, line):
#         tokens = assignment_tokenizer(line)
#         if len(tokens) < 2:
#             raise Exception("All Module-level dunders must be of form key=value")
#         dunder = tokens[0]
#         value = tokens[1]
#         if dunder == "date":
#             if value != "default":
#                 self.dunders["date"] = value
#         elif dunder in self.dunders and value != "default":
#             self.dunders[dunder] = value
#         else:
#             self.dunder_list.append(self.__dunder_expression(dunder, value))
#
#     def exit_context(self):
#         for dunder, value in self.dunders.items():
#             if value != "":
#                 self.dunder_list.append(self.__dunder_expression(dunder, value))
#         self.template.append(self.dunder_list)
#
#
# class OptContext(Context):
#
#     def __init__(self, opt: Opts):
#         self.opt: Opts = opt
#
#     def __str__(self):
#         return "opts"
#
#     def map(self, line):
#         tokens = assignment_tokenizer(line)
#         if len(tokens) < 2:
#             raise Exception("Missing necessary argument in assignment operation")
#         var = self.opt.map_metavar(tokens[0])
#         assign_val = tokens[1]
#         if assign_val == "default":
#             return
#         if var == MetaVars.Home_dir:
#             assign_val = FileStructure(assign_val)
#         self.opt.meta[var] = assign_val
#
#
# class PipContext(Context):
#
#     """
#     Context for pip installation and requirements file creation
#     Requirements will match those listed in .pyspec file
#     """
#     def __init__(self, env_name: str, new_path: obj.PathObj):
#         self.env_name = env_name
#         self.path = new_path
#
#     def __str__(self):
#         return "install"
#
#     def add_to_reqs(self, pip_spec: str):
#         with open(self.fs.make_path("requirements.txt"), "a") as file:
#             file.write(pip_spec + "\n")
#
#     def init_venv(self):
#         venv.EnvBuilder(with_pip=True).create(self.fs.make_path(self.env_name))
#
#     def install(self):
#         if sys.platform == "win32":
#             venv_loc: str = path.join(self.fs.make_path(self.env_name), "Scripts", "pip.exe")
#         else:
#             venv_loc: str = path.join(self.fs.make_path(self.env_name), "bin", "pip")
#         if not path.isfile(venv_loc):
#             raise FileNotFoundError(f"Could not find pip at: {venv_loc}")
#
#         result = subprocess.run([venv_loc, "install", "-r", self.fs.make_path("requirements.txt")])
#         if result.returncode != 0:
#             print("Failed to install packages from requirements.")
#         else:
#             print(f"Successfully installed all packages in {self.env_name}")
#
#     def map(self, package_spec: str):
#         self.add_to_reqs(package_spec)
#
#     def exit_context(self):
#         self.init_venv()
#         self.install()
