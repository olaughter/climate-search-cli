import pytest

from cs.utils import error_file_name, get_data_dir


@pytest.mark.parametrize(
    "start,want",
    (
        ["path/to/file.csv", "path/to/file_errors.csv"],
        ["path.csv", "path_errors.csv"],
    ),
)
def test_error_file_name(start, want):
    got = error_file_name(start)
    assert got == want


def test_get_data_dir():
    result = get_data_dir()
    assert result.endswith("data")
