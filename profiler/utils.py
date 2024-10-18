# Standard imports
import glob
import shutil
import yaml
from pathlib import Path

# Related third party imports

# Local application/library specific imports


def open_yaml(file_path):
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)
    return content


def open_txt(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def glob_files(path, extension):
    return glob.glob(f"{path}/*.{extension}")


def remove_dir(path):
    """
    Remove a directory and its contents.

    Args:
        path (str): The path to the directory to remove

    Returns:
        None

    Example:
        remove_dir("output/")
    """
    if Path(path).exists() and Path(path).is_dir():
        shutil.rmtree(path)
    Path(path).mkdir(parents=True, exist_ok=True)
