import os

import pandas as pd
from sqlalchemy import create_engine

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
