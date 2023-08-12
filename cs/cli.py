from typing import TextIO

import click

from cs.db import DB
from cs.policy_reader import PolicyReader
from cs.utils import error_file_name


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--localpath",
    "-p",
    "data",
    default="data/data.csv",
    help="local file path for loading policy summaries",
    type=click.File(encoding="utf-8"),
)
@click.option(
    "--debug",
    is_flag=True,
    help="Debug setting, will run validation but not load to db",
    default=False,
)
def load(data: TextIO, debug: bool):
    """Loads and validates climate policy summaries"""
    click.echo(f"Validating document: {data.name}")

    pr = PolicyReader(data)
    pr.validate()

    if not pr.problem_rows.empty:
        error_out = error_file_name(original=data.name)
        pr.problem_rows.to_csv(error_out, index=False)
        click.echo(f"Found {len(pr.problem_rows)} issues, writing to: {error_out}")

    db = DB(debug=debug)
    db.df_to_table(pr.df)

    click.echo(f"Loaded {len(pr.df)} policies, from {data.name}")


def entrypoint():
    cli.add_command(load)
    cli()


if __name__ == "__main__":
    entrypoint()
