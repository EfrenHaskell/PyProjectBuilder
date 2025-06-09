import argparse
import file_parser as fp

HELP_MESSAGES: dict[str, str] = {
    "-f": "The name of the file specifying the project structure.",
    "-h": "The directory where the project structure will be created, will use current directory by default",
}

if __name__ == "__main__":
    description = ""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--filename", required=True, help=HELP_MESSAGES["-f"])
    parser.add_argument("-h", "--homedir", help=HELP_MESSAGES["-h"])
