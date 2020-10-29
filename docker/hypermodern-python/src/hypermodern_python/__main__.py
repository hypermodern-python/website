import click

@click.command()
@click.version_option()
def main():
    """The hypermodern Python project."""
    click.echo("Hello, world!")
