#!usr/bin/env Python

"""
Context objects and utilities for context operations
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"


from pathlib import Path
from os import sep, path, chdir, remove, walk
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


def assignment_tokenizer(line):
    """
    Tokenize on assignment operator
    """
    tokens = []
    token = ""
    length = len(line)
    for index in range(length):
        char = line[index]
        if char == "=" or index == length - 1:
            if char != "=":
                token += char
            tokens.append(token.strip())
            token = ""
        else:
            token += char
    return tokens


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


class SubsectionMap:
    def __init__(self, funcmap: dict):
        self.internal = funcmap
        self.curr_subsection = ""

    def exec(self, params: list):
        if self.curr_subsection == "":
            raise Exception("No subsection set")
        if self.curr_subsection not in self.internal:
            return
        self.internal[self.curr_subsection](*params)

    def switch(self, subsection: str):
        self.curr_subsection = subsection


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

    def enter(self, dir_name: str):
        self.curr_relative += dir_name + sep

    def leave(self):
        index = self.curr_relative.rfind(sep, 0, len(self.curr_relative) - 2)
        if index > 0:
            self.curr_relative = self.curr_relative[:index + 1]
        else:
            self.curr_relative = sep

    def search(self):
        """
        Potential future functionality
        """
        pass

    def not_empty(self) -> bool:
        for root, _, files in walk(self.home):
            for file in files:
                file_path = path.join(root, file)
                if path.isfile(file_path) and file != "temp.md":
                    return True
        return False


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
        self.fs.enter(dir_name)

    def leave(self):
        self.fs.leave()

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
    def __init__(self, file_structure: FileStructure):
        self.fs: FileStructure = file_structure
        self.opts: list[str] = [self.fs.home, "", "", ""]
        self.git_bs = FileStructure("")
        self.most_recent_nest = ""
        self.sub_map = SubsectionMap({
            "opt": self.opt,
            "branches": self.branches,
            "readme": self.readme,
            "gitignore": self.gitignore,
        })
        self.ignore: list[str] = []
        self.readme_text: list[str] = []

    def __enter_dir(self):
        print(self.fs.home)
        print(self.opts[0])
        if self.opts[0] != self.fs.home:
            if self.opts[0] == "default":
                chdir(self.fs.make_path(""))
            else:
                chdir(self.fs.make_path(self.opts[0]))

    def init_repo(self):
        self.__enter_dir()
        subprocess.run(["git", "init"])
        with open("temp.md", "w") as file:
            file.write("Updates coming soon...")
        subprocess.run(["git", "add", "temp.md"])
        subprocess.run(["git", "commit", "-m", "Setup"])
        self.init_main_branch()

    def add_readme(self):
        with open("README.md", "w") as file:
            contents = "\n".join(self.readme_text)
            file.write(f"# {self.opts[1]}\n{contents}")

    def add_gitignore(self):
        with open(".gitignore", "w") as file:
            file.write("\n".join(self.ignore))

    def gitignore(self, line):
        self.ignore.append(line)

    def readme(self, line):
        self.readme_text.append(line)

    @staticmethod
    def init_main_branch():
        subprocess.check_call(["git", "branch", "-M", "main"])

    def add_origin(self):
        subprocess.check_call(["git", "remote", "add", "origin", self.opts[2]])

    def enter(self, nest_group: str):
        self.git_bs.enter(nest_group)

    def leave(self):
        self.git_bs.leave()

    def new_branch(self, name: str):
        subprocess.check_call(["git", "branch", name])
        self.most_recent_nest = name

    def push(self):
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Push project items"])
        if self.opts[3] == "":
            subprocess.run(["git", "push", "-u", "origin", "main"])
        else:
            subprocess.run(["git", "push", "origin", self.opts[3]])

    def opt(self, line):
        tokens = assignment_tokenizer(line)
        if len(tokens) > 1:
            var = tokens[0].lower()
            value = tokens[1]
            if var == "dir":
                self.opts[0] = value
                self.init_repo()
            elif var == "name":
                self.opts[1] = value
            elif var == "origin":
                self.opts[2] = value
                self.add_origin()
            elif var == "branch":
                self.opts[3] = value

    def branches(self, task: str):
        if task == "->":
            self.git_bs.enter(self.most_recent_nest)
        elif task == "<-":
            self.git_bs.leave()
        else:
            task_elements = task.split(" ")
            if len(task_elements) < 2:
                raise Exception("Missing required positional argument")
            name = task_elements[1]
            if task_elements[0] == "nest":
                self.most_recent_nest = name
            else:
                self.new_branch(self.git_bs.make_path(name))

    def map(self, line):
        if line[:2] == "//":
            self.sub_map.switch(line[2:].strip().lower())
        else:
            self.sub_map.exec([line])

    def exit_context(self):
        subprocess.run(["git", "reset"])
        if self.fs.not_empty():
            remove("temp.md")
        self.add_readme()
        self.add_gitignore()
        if self.opts[2] != "":
            self.push()


class MLDundersContext(Context):

    """
    Context for creating module-level dunders
    Certain dunders with default values will be added by default
    """
    def __init__(self, template):
        self.default: dict[str, str] = {}
        self.dunder_list = ["#!usr/bin/env Python", "\n\"\"\"\nDescription here...\n\"\"\"\n"]
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
    def __dunder_expression(dunder: str, value: str):
        return f"__{dunder}__ = \"{value}\""

    def map(self, line):
        tokens = assignment_tokenizer(line)
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

    def add_to_reqs(self, pip_spec: str):
        with open(self.fs.make_path("requirements.txt"), "a") as file:
            file.write(pip_spec + "\n")

    def init_venv(self):
        venv.EnvBuilder(with_pip=True).create(self.fs.make_path(self.env_name))

    def install(self):
        if sys.platform == "win32":
            venv_loc: str = path.join(self.fs.make_path(self.env_name), "Scripts", "pip.exe")
        else:
            venv_loc: str = path.join(self.fs.make_path(self.env_name), "bin", "pip")
        if not path.isfile(venv_loc):
            raise FileNotFoundError(f"Could not find pip at: {venv_loc}")

        result = subprocess.run([venv_loc, "install", "-r", self.fs.make_path("requirements.txt")])
        if result.returncode != 0:
            print("Failed to install packages from requirements.")
        else:
            print(f"Successfully installed all packages in {self.env_name}")

    def map(self, package_spec: str):
        self.add_to_reqs(package_spec)

    def exit_context(self):
        self.init_venv()
        self.install()
