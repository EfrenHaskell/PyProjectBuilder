from pathlib import Path
from os import path
import sys
from load import Opts


class PathObj:
    def __init__(self, sep: str, home_path: str = "."):
        """
        PathObj maintains current working directory, path sep and generic indexes
        """

        self.cwd: str = self.__clean(home_path)
        self.sep = sep
        self.generic_dir_postfix = -1
        self.generic_file_postfix = -1

    def append(self, dir_name: str):
        """
        Append cleaned dir to cwd
        :param dir_name:
        """

        self.cwd += self.__clean(dir_name)

    def __clean(self, name: str) -> str:
        """
        Removes extraneous path separators
        :param name:
        :return:
        """

        if len(name) > len(self.sep):
            if name[:len(self.sep)] == self.sep:
                name = name[len(self.sep):]
            if name[-len(self.sep):] == self.sep:
                name = name[:-len(self.sep)]
        return name

    def trunc(self):
        """
        Remove last directory from path
        """

        last_sep_index = self.cwd.rfind(self.sep)
        if last_sep_index != -1:
            self.cwd = self.cwd[:last_sep_index]

    def file_path(self, file_name: str) -> str:
        """
        Return full file path
        :param file_name:
        :return:
        """

        return self.cwd + self.sep + self.__clean(file_name)

    def new_generic_dir(self):
        self.generic_dir_postfix += 1
        return self.generic_dir_postfix

    def new_generic_file(self):
        self.generic_file_postfix += 1
        return self.generic_file_postfix


class Obj:

    def __init__(self):
        self.children: list[Obj] = []

    """
    Base class for procedure objects
    """
    def enter(self, obj: "Obj"):
        self.children.append(obj)

    def exit(self):
        pass

    def __execute_children(self, options: Opts):
        """
        Internal executor for children objects
        """
        for child in self.children:
            child.exec(options)

    def exec(self, options: Opts):
        pass


class BlobObj(Obj):
    def __init__(self, short_text: str = ""):
        super().__init__()
        self.short_text = short_text

    def enter(self, obj: Obj):
        raise Exception()

    def exec(self, options: Opts):
        return self.short_text


class FileTemplate:
    def __init__(self, file_type: str):
        self.contents = []
        self.my_type = file_type
        self.prog_langs = {
            "python",
            "cpp"
        }

    def append(self, child_obj: "FileObj"):
        """
        Adds new items to default text
        :param child_obj:
        """
        if self.my_type == "md":
            file_type = child_obj.template.my_type
            if file_type in self.prog_langs:
                content = "\n".join(["```", file_type, child_obj, "```"])
            else:
                content = str(child_obj)
            self.contents.append(content)

    def __str__(self):
        return "\n".join(self.contents)


class PyFileTemplate(FileTemplate):
    def __init__(self):
        self.exec_str = self.get_exec_str()
        self.ml_doc_str = []
        self.ml_dunders = []
        self.imports = []
        super().__init__("python")

    def append(self, child_obj: "FileObj"):
        file_type = child_obj.template.my_type
        if file_type == "txt":
            self.ml_doc_str.append(str(child_obj.template))

    @staticmethod
    def get_exec_str():
        return "#!python" if sys.platform == "win32" else "#!usr/bin/env python3"

    def __str__(self):
        header = self.exec_str + "\n".join(self.ml_doc_str) + "\n".join(self.ml_dunders) + "\n".join(self.imports)
        return header + super().__str__()


class FileObj(Obj):
    def __init__(self, name: str):
        super().__init__()
        self.name: str = name
        self.template: FileTemplate = self.get_file_template()

    def get_file_template(self) -> FileTemplate:
        extension = self.__check_extension(self.name)
        if extension == "py":
            return PyFileTemplate()
        else:
            return FileTemplate(extension)

    def __str__(self):
        return str(self.template)

    @staticmethod
    def __check_extension(file_nm: str):
        """
        Returns the extension of a given file
        :param file_nm:
        :return:
        """
        return file_nm[file_nm.rfind(".") + 1:]

    def apply(self, file_nm: str):
        """
        Create file
        :param file_nm:
        """
        if not path.exists(file_nm):
            with open(file_nm, "w") as file:
                file.write(str(self.template) + "\n")
            print(f"Successfully created file: {file_nm}")

    def __execute_children(self, options: Opts):
        for child in self.children:
            child.exec(options)
            self.template.append(child)

    def exec(self, options: Opts):
        self.__execute_children(options)
        self.apply(options.path.file_path(self.name))


class DirObj(Obj):

    def __init__(self, name: str):
        super().__init__()
        self.name: str = name

    def append(self, procedure):
        self.children.append(procedure)

    def exec(self, options: Opts):
        dir_path: str = options.path.file_path(self.name)
        if not path.exists(dir_path):
            Path(dir_path).mkdir()
            print(f"Successfully created directory: {dir_path}")
        options.path.append(self.name)
        self.__execute_children(options)
        options.path.trunc()


class PipObj(Obj):
    def __init__(self, package_name: str):
        super().__init__()
        self.package_name = package_name

    def enter(self, obj: Obj):
        pass

    def exec(self, options: Opts):
        with open(options.path.file_path("requirements.txt"), "a") as file:
            file.write(self.package_name + "\n")


class OptObj(Obj):
    def __init__(self, kv_string):
        super().__init__()
        self.key_val = kv_string

    def exec(self, options: Opts):
        options.set_option(self.key_val)
