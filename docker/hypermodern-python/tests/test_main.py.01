import click.testing
import pytest

from hypermodern_python import __main__

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
