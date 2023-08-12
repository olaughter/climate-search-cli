import os

import pandas as pd
from sqlalchemy import create_engine

from cs.schema import Schema


class DB:
    POLICY = "policy"
    SECTOR = "sector"

    def __init__(self, debug: bool = False):
        if debug:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            db_path = self.build_db_url()
            self.engine = create_engine(db_path, echo=False)

    def build_db_url(self) -> str:
        """Creates the database url string"""
        db_path = os.path.join("data", "database.db")
        db_url = f"sqlite:///{db_path}"
        return db_url

    def to_database(self, df):
        """Loads tables to database

        Based on their pandas table transformed in Schema
        """
        schema = Schema()

        policy = schema.policy(df)
        sector = schema.sector(df)

        self.df_to_table(df=policy, table_name=self.POLICY)
        self.df_to_table(df=sector, table_name=self.SECTOR)

    def df_to_table(self, df: pd.DataFrame, table_name: str):
        """Load an individual pandas dataframe to the database"""
        with self.engine.connect() as conn:
            df.to_sql(
                table_name,
                conn,
                index=False,
                if_exists="replace",
            )
