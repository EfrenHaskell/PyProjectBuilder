#!python

"""
Utilities for context operations
"""

__author__ = "Efren"
__date__ = "6/30/2025"
__status__ = "development"
__version__ = "0.1"


from os import sep, path, walk


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

    def __init__(self, home_dir: str, path_sep: str = sep):
        self.home = home_dir
        if self.home == "" or self.home[-1] == path_sep:
            self.curr_relative = ""
        else:
            self.curr_relative = path_sep
        self.path_sep = path_sep

    def make_path(self, name: str):
        """
        Build path for new file/dir
        :param name:
        """
        return self.home + self.curr_relative + name

    def enter(self, dir_name: str):
        self.curr_relative += dir_name + self.path_sep

    def leave(self):
        index = self.curr_relative.rfind(self.path_sep, 0, len(self.curr_relative) - 2)
        if index > 0:
            self.curr_relative = self.curr_relative[:index + 1]
        else:
            if self.home == "" or self.home[-1] == self.path_sep:
                self.curr_relative = ""
            else:
                self.curr_relative = self.path_sep

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


def assignment_tokenizer(line) -> list[str]:
    """
    Tokenize on assignment operator
    :param line:
    :return:
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
