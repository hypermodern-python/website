import textwrap

import click
import httpx

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

@click.command()
@click.version_option()
def main():
    """The hypermodern Python project."""
    response = httpx.get(API_URL)
    response.raise_for_status()
    data = response.json()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))

if __name__ == "__main__":
    main(prog_name="hypermodern-python")
