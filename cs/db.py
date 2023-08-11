import os

import pandas as pd
from sqlalchemy import create_engine


class DB:
    def __init__(self, debug: bool = False):
        if debug:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            db_path = self.build_db_url()
            self.engine = create_engine(db_path, echo=False)

    def build_db_url(self):
        db_path = os.path.join("data", "database.db")
        db_url = f"sqlite:///{db_path}"
        return db_url

    def df_to_table(self, df: pd.DataFrame, table_name: str):
        with self.engine.connect() as conn:
            df.to_sql(
                table_name,
                conn,
                index=False,
                if_exists="replace",
            )
