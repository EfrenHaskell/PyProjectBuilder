import shutil
import file_parser as fp
from pathlib import Path
from os import sep, path, remove
from meta import MetaVars
from contexts import FileStructure
from image import PriorityChain


def end_session():
    shutil.rmtree(f".{sep}test")
    if path.exists(f".{sep}requirements.txt"):
        remove(f".{sep}requirements.txt")


def create_session() -> fp.Session:
    Path("./test").mkdir(exist_ok=True)
    new_session = fp.Session()
    new_session.meta[MetaVars.Home_dir] = FileStructure("./test")
    return new_session


def print_chain(chain: PriorityChain):
    for priority_group in chain.internal:
        for image in priority_group:
            print(image.context)
            print("\n - ".join(image.task_list))
