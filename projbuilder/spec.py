import re
import contexts as ctx
import objects as obj
import load
from os import path
import productions as parse_util
from error import Err


class Funcmap:
    def __init__(self, funcs):
        self.internal_map = funcs
        self.curr_func_group = ""

    def exec(self, params):
        self.internal_map[self.curr_func_group](*params)

    def switch(self, func_group) -> int:
        if func_group not in self.internal_map:
            return 1
        self.curr_func_group = func_group
        return 0


class Spec:
    def __init__(self):
        self.options = load.Opts()
        self.options.load_all()
        self.options.path = obj.PathObj(path.sep, self.options.home_dir)
        self.context_tree: list[ctx.Context] = [None] * self.options.num_contexts

    @staticmethod
    def __clean(line: str):
        """
        Clean line of extraneous end spaces and normalize casing
        :param line:
        :return:
        """
        return line.strip().lower()

    @staticmethod
    def prefix_handle(line: str, prefix: str) -> (bool, str):
        """
        Check if value is prefix of line and remove prefix if so
        :param line:
        :param prefix:
        :return:
        """
        return True, line[len(prefix):] if line[:len(prefix)] == prefix else False, line

    @staticmethod
    def extended_split(line):
        """
        Split on white space, removing any extraneous spaces as well
        :param line:
        """
        return re.split(r"(\s+)", line)

    def str_to_production(self, first: str) -> obj.Obj:
        """
        Convert string tokens to objects
        """
        if first == "dir":
            parse_util.DirProduction()
        elif first == "file":
            if len(tokens) == 1:
                return obj.FileObj(self.options.path.new_generic_file())
            elif len(tokens) == 2:
                return obj.FileObj(tokens[1])
            else:
                raise Exception(Err.TokenLength, "file")
        elif first == "readme":
            if len(tokens) > 1:
                raise Exception(Err.TokenLength, "README")
            return obj.FileObj("README.md")
        elif first == "gitignore":
            if len(tokens) > 1:
                raise Exception(Err.TokenLength, ".gitignore")
            return obj.FileObj(".gitignore")
        elif first == "blob":
            return obj.BlobObj(" ".join(tokens[1:]))
        else:
            curr_context = self.context_tree[-1]
            if type(curr_context) == ctx.PipContext:
                return obj.PipObj(string)
            elif type(curr_context) == ctx.OptContext:
                return obj.OptObj(string)
            else:
                return obj.FileObj(first)

    @staticmethod
    def __tokenize(line: str):
        return re.split(r"\s+", line)

    def context_map(self, context_name: str) -> ctx.Context:
        if context_name == "filestructure":
            return ctx.FSContext(self.options.path)
        # elif context_name == "pip":
        #     return ctx.PipContext(self.options.venv_name, self.path)

    def section_parse(self, lines: list[str]):
        nest_layers: list[ctx.Context | obj.Obj] = []
        last_obj: obj.Obj | None = None
        for line in lines:
            line = self.__clean(line)
            if line.isspace():
                continue
            is_context, line = self.prefix_handle(line, "#")
            if is_context:
                curr_context = self.context_map(self.__clean(line))
                context_order = self.options.execution_order.index(curr_context)
                self.context_tree[context_order] = curr_context
                if len(nest_layers) > 1:
                    raise Exception(Err.NestError)
                elif len(nest_layers) == 1:
                    nest_layers[0] = curr_context
                else:
                    nest_layers.append(curr_context)
            elif len(self.context_tree) == 0:
                raise Exception(Err.ContextSpec)
            elif line == "->":
                if last_obj is None:
                    raise Exception(Err.EnterError)
                else:
                    nest_layers.append(last_obj)
            elif line == "<-":
                last_obj = None
                nest_layers.pop(-1)
            else:
                tokens = self.__tokenize(line)
                new_obj: obj.Obj = self.str_to_production(tokens[0])
                nest_layers[-1].children.append(new_obj)
                last_obj = new_obj

    def exec(self):
        for context in self.context_tree:
            context.exec()


class Default(Spec):
    def __init__(self):
        super().__init__()
