from typing import TextIO

import click

from cs.policy_reader import PolicyReader
from cs.utils import error_file_name


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--localpath",
    "-p",
    required=True,
    help="local file path for loading policy summaries",
    type=click.File(encoding="utf-8"),
)
def load(localpath: TextIO):
    """Loads and validates climate policy summaries"""
    click.echo(f"Validating document: {localpath.name}")

    pr = PolicyReader(localpath)
    pr.validate()

    if not pr.problem_rows.empty:
        error_out = error_file_name(original=localpath.name)
        pr.problem_rows.to_csv(error_out, index=False)
        click.echo(f"Found {len(pr.problem_rows)} issues, writing to: {error_out}")
    else:
        pass


if __name__ == "__main__":
    cli.add_command(load)
    cli()
