"""

"""

import contexts as ctx
import re
from meta import MetaVars
import image


def clean_line(line: str) -> str:
    """
    Clean text input
    Removes excess spaces
    :param line:
    :return:
    """
    return re.sub(r"\s+|\t", " ", line)


class Session:

    def __init__(self):
        self.meta: dict[MetaVars] = {}
        self.chain: image.PriorityChain = image.PriorityChain()

    def line_parse(self, filename: str):
        with open(filename, "r") as file:
            lines = file.readlines()
        context_proc: image.Procedure | None = None
        for line in lines:
            if line.isspace():
                continue
            line = clean_line(line.strip())
            if line[0] == "#":
                context_proc = image.Procedure(self.new_context(line[1:].lower()))
                self.chain.add(context_proc)
            else:
                if context_proc is None:
                    context_img = image.Procedure(self.new_context("filestructure"))
                    self.chain.add(context_img)
                context_proc.add_task(line)
                # curr_context.map(line.split())

    def new_context(self, context_name: str) -> ctx.Context:
        if context_name == "filestructure":
            return ctx.FSContext(self.meta[MetaVars.Home_dir])
        elif context_name == "docstring":
            return ctx.MLDundersContext()
        elif context_name == "install":
            if MetaVars.Venv_nm not in self.meta:
                self.meta[MetaVars.Venv_nm] = ".venv"
            return ctx.PipContext(self.meta[MetaVars.Venv_nm], self.meta[MetaVars.Home_dir])
        else:
            raise Exception("Unknown context")

    def process_all(self):
        self.chain.process_by_priority()
