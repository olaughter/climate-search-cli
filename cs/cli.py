from typing import TextIO

import click
import pandas as pd


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--localpath",
    "-p",
    required=True,
    help="local file path for loading policy summaries",
    type=click.File(),
)
def load(localpath: TextIO):
    """Loads and validates climate policy summaries"""
    click.echo(f"Validating document: {localpath.name}")
    df = pd.read_csv(localpath)


if __name__ == "__main__":
    cli.add_command(load)
    cli()
