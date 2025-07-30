#!python

"""
File parser and session for holding metadata
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

from meta import MetaVars, Opts
import contexts as ctx
import context_utils as ctx_util
import re
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
        self.chain: image.PriorityChain = image.PriorityChain()
        self.template_file: ctx_util.PyFileTemplate = ctx_util.PyFileTemplate()
        self.opt: Opts = Opts()

    def line_parse(self, filename: str) -> image.PriorityChain:
        """
        Create chain of context objects ordered by context priority
        :param filename:
        """
        with open(filename, "r") as file:
            lines = file.readlines()
        context_proc: image.Procedure | None = None
        for index, line in enumerate(lines):
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
            # add cleaned string back into lines
        return self.chain

    def new_context(self, context_name: str) -> ctx.Context:
        """
        Returns corresponding contexts for string names
        :param context_name:
        :return:
        """
        if context_name == "opts":
            return ctx.OptContext(self.opt)
        elif context_name == "filestructure":
            return ctx.FSContext(self.opt.meta[MetaVars.Home_dir], self.template_file)
        elif context_name == "mldunders":
            return ctx.MLDundersContext(self.template_file)
        elif context_name == "install":
            return ctx.PipContext(self.opt.meta[MetaVars.Venv_nm], self.opt.meta[MetaVars.Home_dir])
        elif context_name == "git":
            return ctx.GitContext(self.opt.meta[MetaVars.Home_dir], self.opt)
        else:
            raise Exception("Unknown context")

    def process_all(self):
        """
        Process context procedures from chain
        """
        self.chain.process_by_priority()
