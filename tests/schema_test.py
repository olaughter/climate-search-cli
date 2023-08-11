import pandas as pd

from cs.schema import Schema


def test_schema_policy():
    fixture_path = "tests/fixtures/valid.csv"
    df = pd.read_csv(fixture_path)

    policy_table = Schema().policy(df)

    assert policy_table.columns.tolist() == [
        "policy_id",
        "policy_title",
        "description_text",
    ]
    assert policy_table.policy_id.dtype == "int64"
    assert not policy_table.policy_id.isna().any()
    assert len(policy_table) == len(df)


def test_schema_sector():
    fixture_path = "tests/fixtures/valid.csv"
    df = pd.read_csv(fixture_path)

    sector_table = Schema().sector(df)

    assert sector_table.columns.tolist() == ["policy_id", "sector"]
    assert not sector_table.policy_id.isna().any()
    assert not sector_table.sector.isna().any()
    assert len(sector_table) > len(df)
