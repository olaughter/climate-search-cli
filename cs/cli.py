import os
from typing import TextIO

import click

from cs.db import DB
from cs.output import build_output
from cs.policy_reader import PolicyReader
from cs.utils import error_file_name, get_data_dir

DATA_DIR = get_data_dir()


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--localpath",
    "-p",
    "data",
    default=os.path.join(DATA_DIR, "data.csv"),
    help="local file path for loading policy summaries",
    type=click.File(encoding="utf-8"),
)
@click.option(
    "--debug",
    is_flag=True,
    help="Debug setting, will run validation but not load to db",
    default=False,
)
@click.option(
    "--dbdir", help="Subfolder to build database", default=DATA_DIR, show_default=True
)
@click.option(
    "--errdir",
    help="Subfolder to write errors to, defaults to the same folder as the original file",
    default=None,
)
def load(data: TextIO, debug: bool, dbdir: str, errdir: str):
    """Loads and validates climate policy summaries"""
    click.echo(f"Validating document: {data.name}")

    pr = PolicyReader(data)
    pr.validate()

    if not pr.problem_rows.empty:
        error_out = error_file_name(original=data.name, errdir=errdir)
        pr.problem_rows.to_csv(error_out, index=False)
        click.echo(f"Found {len(pr.problem_rows)} issues, writing to: {error_out}")

    db = DB(debug=debug, dbdir=dbdir)
    db.df_to_table(pr.df)

    click.echo(f"Loaded {len(pr.df)} policies, from {data.name}")


@click.command()
@click.option(
    "--keyword",
    "-k",
    "keywords",
    multiple=True,
    required=True,
    help="Keyword to search with, can be used multiple times, for example: -k key -k word",
)
@click.option(
    "--dbdir",
    help="Subfolder to find an existing database in",
    default=DATA_DIR,
    show_default=True,
)
@click.option(
    "--sort",
    "sort_by_relevancy",
    help="Order the results by relevancy",
    default=False,
    is_flag=True,
    show_default=True,
)
def retrieve(keywords, dbdir, sort_by_relevancy):
    """Query the policy titles and descriptions with keywords"""
    db = DB(dbdir=dbdir)
    rows = db.query_policies(keywords)
    output = build_output(rows, keywords=keywords, sort_by_relevancy=sort_by_relevancy)
    click.echo(output)


def entrypoint():
    cli.add_command(load)
    cli.add_command(retrieve)
    cli()


if __name__ == "__main__":
    entrypoint()
