import pathlib

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent

DIRECTORY_DOWNLOADS = DIRECTORY_OF_THIS_FILE / "downloads"
assert DIRECTORY_DOWNLOADS.is_dir()
