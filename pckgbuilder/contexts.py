#!usr/bin/env Python

"""
Context objects and utilities for context operations
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"


from pathlib import Path
from os import sep, path, chdir
import venv
import sys
import subprocess
import datetime


def clean_dir(dirpath: str) -> str:
    """
    Adds a path separator to the end of the path if not already present
    :param dirpath:
    :return:
    """
    if dirpath[-1] != sep:
        return dirpath + sep
    return dirpath


def handle_existing_file(filename: str) -> str:
    """
    Checks if a file already exists and if so adds new identifier character
    :param filename:
    :return:
    """
    id_counter: int = 0
    temp = filename
    while True:
        if not path.exists(temp):
            return temp
        extension_idx: int = filename.rfind(".")
        temp = f"{filename[:extension_idx]}.{id_counter}{filename[extension_idx:]}"
        id_counter += 1


class PyFileTemplate:

    """
    Provides functionality and object representing a python file template
    Used for adding default text to files
    """
    def __init__(self):
        self.default_text_data = []

    @staticmethod
    def check_extension(file_nm: str):
        """
        Returns the extension of a given file
        :param file_nm:
        :return:
        """
        index = file_nm.rfind(".")
        return file_nm[index + 1:]

    def apply(self, file_nm: str):
        """
        Create new file with default content
        :param file_nm:
        """
        contents: str = ""
        if self.check_extension(file_nm) == "py":
            contents = "\n".join(self.default_text_data) + "\n"
        with open(file_nm, "w") as file:
            file.write(contents)

    def append(self, items: list[str]):
        """
        Adds new items to default text
        :param items:
        """
        self.default_text_data.extend(items)


class FileStructure:

    """
    Object representation of file structure
    At present, only represents home dir and the cwd
    Future implementations might require a more robust implementation
     - Could later create full tree for file structure
    """

    def __init__(self, home_dir: str):
        self.home = home_dir
        self.curr_relative = sep

    def make_path(self, name: str):
        """
        Build path for new file/dir
        :param name:
        """
        return self.home + self.curr_relative + name

    def search(self):
        """
        Potential future functionality
        """
        pass


class Context:

    """
    Base class for Context
    Lists functionality to be included in context objects
    """
    def map(self, line):
        """
        Defines mapping between string commands and context procedures
        :param line:
        """
        pass

    def exit_context(self):
        """
        Defines end of context procedure
        """
        pass


class FSContext(Context):

    """
    Context for file structure creation
    """

    def __init__(self, file_structure: FileStructure, template: PyFileTemplate):
        self.fs: FileStructure = file_structure
        self.temp_dir = self.fs.home
        self.dir_idx = 0
        self.file_idx = 0
        self.template = template

    def add_file(self, filename: str):
        filename = handle_existing_file(self.fs.make_path(filename))
        self.template.apply(filename)
        print(f"Successfully created file: {filename}")

    def create_dir(self, dir_name: str):
        dir_name = self.fs.make_path(dir_name)
        Path(dir_name).mkdir(exist_ok=True)
        print(f"Successfully created directory: {dir_name}")

    def enter(self, dir_name: str):
        self.fs.curr_relative += dir_name + sep

    def leave(self):
        index = self.fs.curr_relative.rfind(sep, 0, len(self.fs.curr_relative)-2)
        if index > 0:
            self.fs.curr_relative = self.fs.curr_relative[:index+1]
        else:
            self.fs.curr_relative = sep

    def map(self, line: str):
        elements: list[str] = line.split()
        command: str = elements[0].lower()
        if command == "dir":
            if len(elements) > 1:
                new_dir: str = elements[1]
            else:
                new_dir: str = f"dir{self.dir_idx}"
                self.dir_idx += 1
            self.create_dir(new_dir)
            self.temp_dir = new_dir
        elif command == "->":
            self.enter(self.temp_dir)
        elif command == "<-":
            self.leave()
        elif command == "file":
            if len(elements) > 1:
                new_file: str = elements[1]
            else:
                new_file: str = f"file{self.file_idx}.txt"
                self.file_idx += 1
            self.add_file(new_file)


class GitContext(Context):

    """
    Context for git initialization
     - Still in development
    """
    def __init__(self, file_structure: FileStructure, git_dir: str):
        self.git_dir = git_dir
        self.fs: FileStructure = file_structure

    def __enter_dir(self):
        chdir(self.fs.make_path(self.git_dir))

    def new_repo(self, remote_repo: str, repo_name: str):
        self.__enter_dir()
        subprocess.check_call(["git", "init"])
        subprocess.check_call(["git", "branch", "-M", "main"])
        subprocess.check_call(["git", "remote", "add", "origin", remote_repo])
        with open("README.md", "w") as file:
            file.write(f"# {repo_name}")

    def clone_repo(self, remote_repo: str):
        self.__enter_dir()
        subprocess.check_call(["git", "clone", remote_repo])

    def enter(self):
        pass

    def leave(self):
        pass


class MLDundersContext(Context):

    """
    Context for creating module-level dunders
    Certain dunders with default values will be added by default
    """
    def __init__(self, template):
        self.default: dict[str, str] = {}
        self.dunder_list = ["#!usr/bin/env Python"]
        date_time = datetime.datetime.now()
        date_str = f"{date_time.month}/{date_time.day}/{date_time.year}"
        self.dunders: dict[str, str] = {
            "all": "",
            "annotations": "",
            "author": "",
            "credits": "",
            "date": date_str,
            "status": "development",
            "version": 0.1,
        }
        self.template: PyFileTemplate = template

    @staticmethod
    def __custom_tokenize(line):
        """
        Tokenize on =
        """
        tokens = []
        token = ""
        length = len(line)
        for index in range(length):
            char = line[index]
            if char == "=" or index == length - 1:
                tokens.append(token.strip())
                token = ""
            else:
                token += char
        return tokens

    @staticmethod
    def __dunder_expression(dunder: str, value: str):
        return f"__{dunder}__ = \"{value}\""

    def map(self, line):
        tokens = self.__custom_tokenize(line)
        if len(tokens) < 2:
            raise Exception("All Module-level dunders must be of form key=value")
        dunder = tokens[0]
        value = tokens[1]
        if dunder == "date":
            if value != "default":
                self.dunders["date"] = value
        elif dunder in self.dunders:
            self.dunders[dunder] = value
        else:
            self.dunder_list.append(self.__dunder_expression(dunder, value))

    def exit_context(self):
        for dunder, value in self.dunders.items():
            if value != "":
                self.dunder_list.append(self.__dunder_expression(dunder, value))
        self.template.append(self.dunder_list)


class PipContext(Context):

    """
    Context for pip installation and requirements file creation
    Requirements will match those listed in .pyspec file
    """
    def __init__(self, env_name: str, file_structure: FileStructure):
        self.env_name = env_name
        self.fs = file_structure

    def init_venv(self):
        venv.EnvBuilder(with_pip=True).create(self.env_name)

    def activate(self):
        """
        Venv activation
        - Yet to be tested, should work in theory
        """
        venv_loc = self.fs.make_path(self.env_name)
        if sys.platform == "win32":
            activate_script = path.join(venv_loc, "Scripts", "activate.bat")
        else:
            activate_script = path.join(venv_loc, "bin", "activate")
        with open(activate_script) as file:
            exec(file.read(), {'__file__': activate_script})

    def add_to_reqs(self, pip_spec: str):
        with open(self.fs.make_path("requirements.txt"), "a") as file:
            file.write(pip_spec + "\n")

    def install(self):
        try:
            venv_loc = self.fs.make_path("requirements.txt")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", venv_loc])
            print(f"Successfully installed all dependencies from {venv_loc}")
        except subprocess.CalledProcessError as e:
            print(f"Installation failed: {e}")

    def map(self, package_spec: str):
        self.add_to_reqs(package_spec)

    def exit_context(self):
        self.activate()
        self.install()
