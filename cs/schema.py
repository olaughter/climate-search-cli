import pandas as pd


class Schema:
    def policy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates a dataframe for policy information, ready for loading"""
        policy = df.copy(deep=True)
        policy = df[["policy_id", "policy_title", "description_text"]]
        policy = policy.astype(
            {
                "policy_id": "int64",
                "policy_title": "string",
                "description_text": "string",
            }
        )
        return policy

    def sector(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates a dataframe for sector information, ready for loading"""
        sector = df.copy(deep=True)
        sector["sector"] = sector["sectors"].str.split(";")  # Splits sectors into array
        sector = sector.explode("sector")  # Creates row for each sector
        sector = sector[["policy_id", "sector"]]  # Define Columns
        return sector
