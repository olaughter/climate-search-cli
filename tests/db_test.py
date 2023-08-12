import pandas as pd
from sqlalchemy import MetaData, select
from sqlalchemy.schema import Table

from cs.db import DB


def test_db_build_db_url():
    result = DB(debug=True).build_db_url("test")
    assert result == "sqlite:///test/database.db"


def test_db_df_to_table():
    db = DB(debug=True)
    df = pd.read_csv("tests/fixtures/valid.csv")
    db.df_to_table(df, "test")

    with db.engine.connect() as conn:
        test = Table("test", MetaData(), autoload_with=conn.engine)
        assert test.columns.keys() == [
            "policy_id",
            "policy_title",
            "sectors",
            "description_text",
        ]

        rows = conn.execute(select(test)).fetchall()
        assert len(rows) > 0


def test_query_policies():
    # Prepare table
    db = DB(debug=True)
    df = pd.read_csv("tests/fixtures/valid.csv")
    db.df_to_table(df, "policy")

    # Standard search
    rows = db.query_policies(keywords=["Forest"])
    assert len(rows) == 4

    # Is case insensitive
    rows = db.query_policies(keywords=["FOREST"])
    assert len(rows) == 4

    # Not present
    rows = db.query_policies(keywords=["SomethingNotInTheData"])
    assert len(rows) == 0

    # Multiple
    rows = db.query_policies(keywords=["Forest", "Economy"])
    assert len(rows) == 5
