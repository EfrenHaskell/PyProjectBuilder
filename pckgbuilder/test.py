import test_utils

if __name__ == "__main__":
    new_session = test_utils.create_session()
    new_session.line_parse("sample.pyspec")
    test_utils.end_session()
