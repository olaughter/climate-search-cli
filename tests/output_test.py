import pickle

from cs.output import build_policy_sequence, build_sumamry_stats


def test_build_policy_sequence():
    with open("tests/fixtures/rows", "rb") as f:
        rows = pickle.load(f)

    result = build_policy_sequence(rows)

    assert type(result) == list
    assert len(result) == len(rows)
    for row in result:
        assert type(row) == dict
        for field in ["policyTitle", "policyId", "sectors", "descriptionText"]:
            assert field in row.keys()

        assert type(row["sectors"]) == list


def test_build_sumamry_stats():
    with open("tests/fixtures/rows", "rb") as f:
        rows = pickle.load(f)

    result = build_sumamry_stats(rows)
