import os

import pandas as pd
from sqlalchemy import MetaData, create_engine, or_, select
from sqlalchemy.schema import Table

POLICY_TABLE = "policy"


class DB:
    def __init__(self, debug: bool = False, dbdir: str = "data"):
        if debug:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            db_path = self.build_db_url(dbdir)
            self.engine = create_engine(db_path, echo=False)

    def build_db_url(self, dbdir) -> str:
        """Creates the database url string"""
        db_path = os.path.join(dbdir, "database.db")
        db_url = f"sqlite:///{db_path}"
        return db_url

    def df_to_table(self, df: pd.DataFrame, table_name: str = POLICY_TABLE):
        """Load an individual pandas dataframe to the database"""
        with self.engine.connect() as conn:
            df.to_sql(
                table_name,
                conn,
                index=False,
                if_exists="replace",
            )

    def query_policies(self, keywords):
        """Keyword search for matching policies

        Builds sql that will return rows with any keyword in either title or description
        """
        with self.engine.connect() as conn:
            policy = Table(POLICY_TABLE, MetaData(), autoload_with=conn.engine)

            query = select(policy).where(
                or_(
                    *[policy.c.policy_title.contains(k) for k in keywords],
                    *[policy.c.description_text.contains(k) for k in keywords],
                )
            )
            rows = conn.execute(query).fetchall()
            return rows
