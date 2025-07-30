#!python

"""
Image module provides Procedure and PriorityChain Objects
Used for representing context-task relation and priority grouping
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

import contexts
from typing import Any


class Procedure:
    """"
    A procedure consists of a context and task_list
    The task_list details the jobs to be executed when building a project
    Tasks can then be executed by context
    """

    def __init__(self, context):
        self.context = context
        self.task_list = []

    def __str__(self):
        return str(self.context) + "\n".join(self.task_list)

    def add_task(self, line: str):
        self.task_list.append(line)

    def process_tasks(self):
        for task in self.task_list:
            self.context.map(task)
        self.context.exit_context()


class PriorityChain:
    """
    A priority chain is a collection of procedures stored in priority order

    """

    def __init__(self):
        self.internal: dict[Any] = {
            contexts.OptContext: None,
            contexts.MLDundersContext: None,
            contexts.PipContext: None,
            contexts.FSContext: None,
            contexts.GitContext: None,
        }
        self.priority_order = [
            contexts.OptContext,
            contexts.MLDundersContext,
            contexts.PipContext,
            contexts.FSContext,
            contexts.GitContext,
        ]

    def __str__(self):
        return "\n".join([self.is_valid_procedure(context_type) for context_type in self.priority_order])

    def is_valid_procedure(self, context):
        procedure = self.internal[context]
        if procedure is not None:
            return procedure
        return ""

    def add(self, procedure: Procedure):
        """
        Add new procedure to chain
        :param procedure:
        :return:
        """
        self.internal[type(procedure.context)] = procedure

    def process_by_priority(self):
        """
        Process all tasks in priority order
        :return:
        """
        for context_type in self.priority_order:
            procedure = self.internal[context_type]
            if procedure is not None:
                procedure.process_tasks()
