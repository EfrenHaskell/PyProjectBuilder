from os import path


def check_dependencies():
    dirs: list[str] = [
        "./conf",
        "./scripts"
    ]
    config_files: list[str] = [
        "context"
    ]
    for dir_nm in dirs:
        if not path.exists(dir_nm) or not path.isdir(dir_nm):
            raise Exception(f"Missing dir {dir_nm}")

    for cfg in config_files:
        if not path.exists(f"./config/{cfg}.cfg"):
            raise Exception(f"Missing config file {cfg}.cfg")

