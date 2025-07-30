from os import path
import re
from error import Err
import tokens as tk


class Opts:
    def __init__(self):
        self.home_dir = ""
        self.venv_name = ""
        self.num_contexts = 0
        self.execution_order = []
        self.show_dependence = False
        self.path = None

    def key_param_map(self, key, value):
        if key == "home_dir":
            self.home_dir = value
        if key == "venv_name":
            self.venv_name = value
        if key == "num_contexts":
            self.num_contexts = int(value)
        if key == "show_dependence":
            self.show_dependence = bool(value)

    def set_option(self, kv_string: str):
        key, value = re.split(r"\s*=\s*", kv_string)
        self.key_param_map(key, value)

    def load_options(self):
        options_file = "./conf/options.conf"
        if path.exists(options_file):
            with open(options_file, "r") as file:
                for line in file.readlines():
                    self.set_option(line)
        else:
            raise Exception("Could not locate options file")

    def load_exec_order(self):
        order_file = "./conf/exec_order.conf"
        if path.exists(order_file):
            with open(order_file, "r") as file:
                for line in file.readlines():
                    self.execution_order.append(line)
        else:
            raise Exception()

    def error_check(self):
        if len(self.execution_order) != self.num_contexts:
            raise Exception(Err.ContextOrderMismatch)

    def load_all(self):
        self.load_exec_order()
        self.load_options()
        self.error_check()


class ConfParser:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def load(self):
        with open(self.file_name, "r") as file:
            for line in file.readlines():
                if not line.isspace():
                    token_root = self.tokenize(line)

    @staticmethod
    def tokenize(line: str) -> tk.Token:
        root: tk.Token = tk.Root()
        curr: tk.Token = root
        literal = ""
        special = {
            "{": tk.LSquig,
            "}": tk.RSquig,
            "[": tk.LBrack,
            "]": tk.RBrack,
            "=": tk.AssignmentOp,
            ",": tk.Comma,
        }
        for char in line:
            if char.isspace():
                continue
            elif char in special:
                if literal != "":
                    curr = curr.append(tk.Literal(literal))
                    literal = ""
                curr = curr.append(special[char]())
            else:
                literal += char
        curr.append(tk.Literal(literal))
        return root


    def dump(self):
        pass

