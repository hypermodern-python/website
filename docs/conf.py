"""Sphinx configuration."""
from datetime import datetime


project = "Hypermodern Python"
author = "Claudio Jolowicz"
copyright = f"{datetime.now().year}, {author}"
language = "en"
html_theme = "furo"
extensions = ["myst_parser", "pygments_pytest", "sphinx_copybutton"]
