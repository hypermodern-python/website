"""Nox sessions."""
import shutil
from pathlib import Path

import nox
import nox_poetry.patch
from nox.sessions import Session


nox.options.sessions = ["docs-build"]
sphinx_extensions = [
    "furo",
    "myst-parser",
    "pygments-pytest",
    "sphinx-copybutton",
]


@nox.session(name="docs-build", python="3.8")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    shutil.rmtree(Path("docs", "_build"), ignore_errors=True)

    args = session.posargs or ["docs", "docs/_build"]
    session.install("sphinx", *sphinx_extensions)
    session.run("sphinx-build", *args)


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    shutil.rmtree(Path("docs", "_build"), ignore_errors=True)

    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install("sphinx-autobuild", *sphinx_extensions)
    session.run("sphinx-autobuild", *args)
