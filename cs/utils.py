import os


def error_file_name(original: str, errdir: str) -> str:
    """Build an file name for an error file based on the original path"""
    base_path, extension = os.path.splitext(original)
    if errdir:
        file = os.path.split(base_path)[-1]
        base_path = os.path.join(errdir, file)
    return "".join([base_path, "_errors", extension])


def get_data_dir() -> str:
    """Returns the data directory as an absolute path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    return data_dir
