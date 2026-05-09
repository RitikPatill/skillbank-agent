def test_import():
    import skillbank
    assert skillbank.__version__ == "0.1.0"


def test_cli_entrypoint():
    from click.testing import CliRunner
    from skillbank.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output
    assert "list" in result.output
