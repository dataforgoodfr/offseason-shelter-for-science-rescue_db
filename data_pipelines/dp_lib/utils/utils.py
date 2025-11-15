import os


def _get_data_directory() -> str:
    """Returns the path of the data directory from the data_pipelines library"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = os.path.basename(dir_path)

    # We go up in the directory level until
    # we are at the root of the library
    while dir_name != "data_pipelines":
        dir_path = os.path.dirname(dir_path)
        dir_name = os.path.basename(dir_path)

    return os.path.join(dir_path, "data")

DATA_DIR = _get_data_directory()
