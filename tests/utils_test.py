import pytest

from cs.utils import error_file_name


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
