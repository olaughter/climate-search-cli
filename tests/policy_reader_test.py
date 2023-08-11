from cs.policy_reader import PolicyReader


def test_validate():
    # Expect to pass validation
    fixture_path = "tests/fixtures/valid.csv"
    with open(fixture_path, "r") as f:
        pr = PolicyReader(f)
    pr.validate()
    assert len(pr.problem_rows) == 0, f"Found problems with valid file: {fixture_path}"

    # Expect to fail validation
    for problem_file in [
        "tests/fixtures/missing_titles.csv",
        "tests/fixtures/bad_policy_ids.csv",
        "tests/fixtures/bad_sectors.csv",
    ]:
        with open(problem_file, "r") as f:
            pr = PolicyReader(f)
        pr.validate()
        assert len(pr.df) < len(
            pr.problem_rows
        ), f"Expected problems with problem file: {problem_file}"


def test__policy_id_is_integer():
    fixture_path = "tests/fixtures/bad_policy_ids.csv"
    with open(fixture_path, "r") as f:
        pr = PolicyReader(f)
    result = pr._policy_id_is_integer(pr.df)

    expected_failures = 2
    assert (
        len(result) == expected_failures
    ), f"Unexpected amount of failures validating fixture file: {fixture_path}"


def test__policy_title_not_null():
    fixture_path = "tests/fixtures/missing_titles.csv"
    with open(fixture_path, "r") as f:
        pr = PolicyReader(f)
    result = pr._policy_title_not_null(pr.df)

    expected_failures = 2
    assert (
        len(result) == expected_failures
    ), f"Unexpected amount of failures validating fixture file: {fixture_path}"


def test__sectors_valid_array():
    fixture_path = "tests/fixtures/bad_sectors.csv"
    with open(fixture_path, "r") as f:
        pr = PolicyReader(f)
    result = pr._sectors_valid_array(pr.df)

    expected_failures = 2
    assert (
        len(result) == expected_failures
    ), f"Unexpected amount of failures validating fixture file: {fixture_path}"
