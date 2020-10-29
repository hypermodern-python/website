import click.testing

from hypermodern_python import __main__

def test_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
