"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Hypermodern Python Website."""


if __name__ == "__main__":
    main(prog_name="hypermodern-python-website")  # pragma: no cover
