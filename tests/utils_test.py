import pytest

from cs.utils import error_file_name, get_data_dir


@pytest.mark.parametrize(
    "start,want,errdir",
    (
        ["path/to/file.csv", "path/to/file_errors.csv", None],
        ["path.csv", "path_errors.csv", None],
        ["path/to/file.csv", "otherpath/file_errors.csv", "otherpath/"],
    ),
)
def test_error_file_name(start, want, errdir):
    got = error_file_name(start, errdir)
    assert got == want


def test_get_data_dir():
    result = get_data_dir()
    assert result.endswith("data")
