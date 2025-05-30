import argparse

HELP_MESSAGES: dict[str, str] = {
    "-f": "The name of the file specifying the project structure.",
}

if __name__ == "__main__":
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--filename", required=True, help=HELP_MESSAGES["-f"])
