import pathlib


def get_project_dir() -> str:
    """
    This is used to ensure that we will use the absolute path and not a relative path
    :return: Path of the project directory as a string
    """
    return str(pathlib.Path(__file__).parent.parent.absolute())
