from click.testing import CliRunner

from cs.cli import cli, load


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_load__no_args():
    runner = CliRunner()
    result = runner.invoke(load, [])

    assert result.exit_code == 2


def test_load__missing_file():
    runner = CliRunner()
    result = runner.invoke(load, ["--debug", "--localpath", "not-a-file"])

    assert result.exit_code == 2


def test_load__good_file():
    fixture_path = "tests/fixtures/empty_sample.csv"
    runner = CliRunner()
    result = runner.invoke(load, ["--debug", "--localpath", fixture_path])

    assert result.exit_code == 0
