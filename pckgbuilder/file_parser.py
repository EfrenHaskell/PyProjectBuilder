#!usr/bin/env Python

"""
File parser and session for holding metadata
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

from meta import MetaVars
import contexts as ctx
import re
import image
from os import sep


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
        self.template_file: ctx.PyFileTemplate = ctx.PyFileTemplate()

    def line_parse(self, filename: str):
        """
        Create chain of context objects ordered by context priority
        :param filename:
        """
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
        """
        Returns corresponding contexts for string names
        :param context_name:
        :return:
        """
        if context_name == "filestructure":
            return ctx.FSContext(self.meta[MetaVars.Home_dir], self.template_file)
        elif context_name == "mldunders":
            return ctx.MLDundersContext(self.template_file)
        elif context_name == "install":
            if MetaVars.Venv_nm not in self.meta:
                self.meta[MetaVars.Venv_nm] = f".{sep}venv"
            return ctx.PipContext(self.meta[MetaVars.Venv_nm], self.meta[MetaVars.Home_dir])
        elif context_name == "git":
            return ctx.GitContext(self.meta[MetaVars.Home_dir])
        else:
            raise Exception("Unknown context")

    def process_all(self):
        """
        Process context procedures from chain
        """
        self.chain.process_by_priority()
