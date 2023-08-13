import json
import os
from tempfile import TemporaryDirectory

from click.testing import CliRunner

from cs.cli import cli, load, retrieve


def test_integration():
    with TemporaryDirectory(dir="cs/data") as tempdir:
        # Fixture with one bad row and five good rows
        fixture_path = "tests/fixtures/integration.csv"
        error_doc = os.path.join(tempdir, "integration_errors.csv")

        # Prepare Cli
        cli.add_command(load)
        cli.add_command(retrieve)
        runner = CliRunner()

        # cs command
        cs = runner.invoke(cli, [])
        assert cs.exit_code == 0

        # Load
        cs_load = runner.invoke(
            cli,
            [
                "load",
                "--dbdir",
                tempdir,
                "--localpath",
                fixture_path,
                "--errdir",
                tempdir,
            ],
        )
        assert cs_load.exit_code == 0
        # Check Errors
        with open(error_doc, "r") as f:
            lines = f.readlines()
            assert len(lines) == 2  # Headers plus error row

        # Retrieve different amounts
        cs_retrieve_1 = runner.invoke(
            cli, ["retrieve", "--dbdir", tempdir, "-k", "XXVIII"]
        )
        assert cs_load.exit_code == 0
        matches = json.loads(cs_retrieve_1.output).get("matches")
        assert len(matches) == 1

        cs_retrieve_2 = runner.invoke(
            cli, ["retrieve", "--dbdir", tempdir, "-k", "environment"]
        )
        assert cs_load.exit_code == 0
        matches = json.loads(cs_retrieve_2.output).get("matches")
        assert len(matches) == 2

        cs_retrieve_3 = runner.invoke(
            cli,
            [
                "retrieve",
                "--dbdir",
                tempdir,
                "-k",
                "storage",
                "-k",
                "economy",
                "-k",
                "plan",
                "-k",
                "policy",
                "-k",
                "national",
                "-k",
                "development",
            ],
        )
        assert cs_load.exit_code == 0
        matches = json.loads(cs_retrieve_3.output).get("matches")
        assert len(matches) == 5

        #  with sort
        cs_retrieve_3 = runner.invoke(
            cli, ["retrieve", "--dbdir", tempdir, "-k", "development", "--sort"]
        )
        assert cs_load.exit_code == 0
        matches = json.loads(cs_retrieve_3.output).get("matches")
        assert len(matches) == 3
        scores = [match["relevance"] for match in matches]
        assert scores == sorted(scores, reverse=True)
