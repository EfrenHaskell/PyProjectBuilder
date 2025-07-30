#!usr/bin/env Python

"""
Image module provides Procedure and PriorityChain Objects
Used for representing context -- task relation and priority grouping
"""

__author__ = "Efren"
__date__ = "6/10/2025"
__status__ = "development"
__version__ = "0.1"

import contexts


class Procedure:
    """"
    A procedure consists of a context and task_list
    The task_list details the jobs to be executed when building a project
    Tasks can then be executed by context
    """

    def __init__(self, context):
        self.context = context
        self.task_list = []

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
        self.internal: list[list[Procedure]] = [[], [], [], []]

    def add(self, procedure: Procedure):
        """
        Add new procedure to chain
        :param procedure:
        :return:
        """
        self.internal[self.__priority_of(procedure.context)].append(procedure)

    def process_by_priority(self):
        """
        Process all tasks in priority order
        :return:
        """
        for priority_group in self.internal:
            for image in priority_group:
                image.process_tasks()

    @staticmethod
    def __priority_of(context):
        """
        Return priority of context
        :param context:
        :return:
        """
        if isinstance(context, contexts.MLDundersContext):
            return 0
        if isinstance(context, contexts.PipContext):
            return 1
        if isinstance(context, contexts.FSContext):
            return 2
        if isinstance(context, contexts.GitContext):
            return 3
