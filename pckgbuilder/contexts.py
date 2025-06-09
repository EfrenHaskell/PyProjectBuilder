"""

"""
from pathlib import Path
from os import sep, path, chdir
import venv
import sys
import subprocess
import datetime


def clean_dir(dirpath: str) -> str:
    if dirpath[-1] != sep:
        return dirpath + sep
    return dirpath


def handle_existing_file(filename: str) -> str:
    id_counter: int = 0
    temp = filename
    while True:
        if not path.exists(temp):
            return temp
        extension_idx: int = filename.rfind(".")
        temp = f"{filename[:extension_idx]}.{id_counter}{filename[extension_idx:]}"
        id_counter += 1


class Context:
    def map(self, line):
        pass


class MLDundersContext(Context):

    def __init__(self):
        self.default: dict[str, str] = {}
        self.dunder_list = ["#!usr/bin/env Python"]

    @staticmethod
    def __custom_tokenize(line):
        tokens = []
        token = ""
        for char in line:
            if char == " " or char == "=":
                tokens.append(token)
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
        expression = self.__dunder_expression(dunder, value)
        if dunder == "date":
            if value == "default":
                date_time = datetime.datetime.now()
                date_str = f"{date_time.month}/{date_time.day}/{date_time.year}"
                self.dunder_list.append(self.__dunder_expression(dunder, date_str))
            else:
                self.dunder_list.append(expression)
        else:
            self.dunder_list.append(expression)


class FileStructure:

    def __init__(self, home_dir: str):
        self.home = home_dir
        self.curr_relative = ""

    def make_path(self, name: str):
        return self.home + self.curr_relative + name

    def search(self):
        pass


class FSContext(Context):

    def __init__(self, file_structure: FileStructure):
        self.fs: FileStructure = file_structure
        self.temp_dir = self.fs.home
        self.dir_idx = 0
        self.file_idx = 0

    def add_file(self, filename: str, contents: list[str]):
        filename = handle_existing_file(self.fs.make_path(filename))
        with open(filename, "w") as file:
            file.write("\n".join(contents))
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
            self.fs.curr_relative = ""

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
            self.add_file(new_file, [])


class GitContext(Context):

    def __init__(self, file_structure: FileStructure, git_dir: str):
        self.git_dir = git_dir
        self.fs: FileStructure = file_structure

    def __enter_dir(self):
        chdir(self.fs.make_path(self.git_dir))

    def new_repo(self, remote_repo: str):
        self.__enter_dir()
        subprocess.check_call(["git", "init"])
        subprocess.check_call(["git", "branch", "-M", "main"])
        subprocess.check_call(["git", "remote", "add", "origin", remote_repo])

    def clone_repo(self, remote_repo: str):
        self.__enter_dir()
        subprocess.check_call(["git", "clone", remote_repo])

    def enter(self):
        pass

    def leave(self):
        pass


class PipContext(Context):

    def __init__(self, env_name: str, file_structure: FileStructure):
        self.env_name = env_name
        self.fs = file_structure

    def init_venv(self):
        venv.EnvBuilder(with_pip=True).create(self.env_name)

    def activate(self):
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
