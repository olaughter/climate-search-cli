from tempfile import TemporaryDirectory

import pandas as pd
from click.testing import CliRunner
from sqlalchemy import create_engine

from cs.cli import cli, load, retrieve


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_load__missing_file():
    runner = CliRunner()
    result = runner.invoke(load, ["--debug", "--localpath", "not-a-file"])

    assert result.exit_code == 2


def test_load__good_file():
    fixture_path = "tests/fixtures/empty_sample.csv"
    runner = CliRunner()
    result = runner.invoke(load, ["--debug", "--localpath", fixture_path])

    assert result.exit_code == 0


def test_retrieve__without_load():
    with TemporaryDirectory(dir="data") as tempdir:
        # Create a table so queries will not fail
        fixture_path = "tests/fixtures/empty_sample.csv"
        engine = create_engine(f"sqlite:///{tempdir}/database.db", echo=True)
        with engine.connect() as conn:
            pd.read_csv(fixture_path).to_sql("policy", conn)

        #  Run command
        runner = CliRunner()
        result = runner.invoke(retrieve, ["--dbdir", tempdir, "-k", "green"])

        assert result.exit_code == 0
