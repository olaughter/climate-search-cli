from typing import TextIO

import pandas as pd


class PolicyReader:
    """For processing policy data into a valid dataframe

    Reads a TextIO object into a pandas dataframe, and performs validations on it

    variables:
        problem_rows: the records with issues
        df: the full dataframe
    """

    def __init__(self, data: TextIO) -> None:
        col_names = [
            "policy_id",
            "policy_title",
            "sectors",
            "description_text",
        ]
        self.df = pd.read_csv(
            data,
            usecols=col_names,
            dtype="string",
            keep_default_na=False,
            encoding="utf8",
        )

        self.problem_rows = pd.DataFrame(columns=col_names)

    def validate(self) -> None:
        """Loops over a series of checks

        If any checks return bad rows it will store them in problem_rows
        for later investigation.
        """
        for validation in [
            self._policy_id_is_integer,
            self._policy_title_not_null,
            self._sectors_valid_array,
        ]:
            problems = validation(self.df)
            self.df = self.df.drop(problems.index)
            self.problem_rows = pd.concat([self.problem_rows, problems])

    def _policy_id_is_integer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validation. Returns rows where policy id is not an integer"""
        return df[~df.policy_id.str.isdigit()]

    def _policy_title_not_null(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validation. Returns rows where policy title is missing"""
        return df[df.policy_title == ""]

    def _sectors_valid_array(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validation. Returns rows where secotr array has an empty item"""
        return df[
            df.apply(
                lambda row: all([len(s) == 0 for s in row.sectors.split(";")]), axis=1
            )
        ]
