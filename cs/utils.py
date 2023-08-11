import os


def error_file_name(original: str) -> str:
    """Build an file name for an error file based on the original path"""
    base_path, extension = os.path.splitext(original)
    return "".join([base_path, "_errors", extension])
