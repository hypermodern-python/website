# Setup

In this first chapter,
we set up a Python project using [Poetry].
Our example project is a simple command-line application
that uses the Wikipedia API to display random facts on the console.

- [View changes](https://github.com/cjolowicz/hypermodern-python/compare/initial...chapter01)
- [Download code](https://github.com/cjolowicz/hypermodern-python/archive/chapter01.zip)

```{tip}
This guide has a companion repository: [cjolowicz/hypermodern-python].
Each article in the guide corresponds to a set of commits in the GitHub repository.
```

```{important}
Throughout this guide, replace `hypermodern-python` with the name of your own repository.
Choosing a different name avoids a name collision on [PyPI].
```

## Creating a repository on GitHub

![opera02]

For the purposes of this guide,
[GitHub] is used to host the public git repository for your project.
Other popular options are [GitLab] and [BitBucket].

Create a repository on GitHub,
and populate it with `README.md` and `LICENSE` files.
For this project, I will use the [MIT license],
a simple permissive license.

Clone the repository to your machine, and `cd` into it:

```sh
git clone git@github.com:<your-username>/hypermodern-python.git
cd hypermodern-python
```

```{tip}
As you follow the rest of this guide,
create a series of [small, atomic commits][git-best-practices] documenting your steps.
Use `git status` to discover files generated by commands shown in the guide.
```

Let's continue by setting up the developer environment.

## Installing Python

![opera03]

When maintaining Python projects, you often need to check them with different Python versions.
Ideally, these would be the latest releases of every major Python version supported by your project.
Bonus points if you also check against the development version of the upcoming Python release.

### Installing Python on Windows

If you are working natively on Windows,
install the official binary for each desired Python version from [python.org].
In this guide, we will be using the current release (Python 3.9) and its predecessor (Python 3.8).

```{warning}
Do not check the *Add Python to PATH* box in the installer,
unless you wish to use that particular Python version as your system default.
```

During development, use the [Python launcher for Windows] to run the desired Python version:

```sh
> py -3.9 --version
Python 3.9.0

> py -3.8 --version
Python 3.8.6
```

### Installing Python with pyenv

```{tip}
On some Linux distributions,
you may be able to install multiple Python versions from binary packages.
For example, on [Fedora] you can install multiple Python interpreters using ``dnf``.
On a Debian-based Linux distribution such as Ubuntu,
you can install multiple Python versions from the [deadsnakes PPA].
Invoke specific Python versions from the console using their versioned name, such as ``python3.9``.
```

If you are working on Linux, Unix, or Mac, or using the [Windows Subsystem for Linux],
you can install multiple Python versions with [pyenv], a Python version manager.
Install pyenv like this:

```sh
curl https://pyenv.run | bash
```

Add the following lines to your `~/.bashrc`:

```sh
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Open a new shell, or source `~/.bashrc` in your current shell:

```sh
source ~/.bashrc
```

Install the Python build dependencies for your platform,
using one of the commands listed in the [official instructions][pyenv-wiki].
For example, on a recent [Ubuntu] this would be:

```sh
sudo apt-get update; sudo apt-get install --no-install-recommends make \
build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
```

You're ready to install the latest Python releases. This may take a while:

```sh
pyenv install 3.9.0
pyenv install 3.8.6
```

Make your fresh Pythons available inside the repository:

```sh
pyenv local 3.9.0 3.8.6
```

Congratulations! You have access to the latest and greatest of Python:

```sh
$ python --version
Python 3.9.0

$ python3.8 --version
Python 3.8.6
```

Python 3.9.0 is the default version and can be invoked as `python`, but both
versions are accessible as `python3.8` and `python3.9`, respectively.

## Setting up a project with Poetry

![opera05]

[Poetry] is a Python packaging and dependencies manager,
similar in spirit to JavaScript's `npm` and Rust's `cargo`.
Common alternatives are [pipenv], [setuptools] with [pip-tools], and [flit].

<!-- 
[dephell]: https://dephell.org/
[enscons]: https://github.com/dholth/enscons
[hatch]: https://github.com/ofek/hatch
[pbr]: https://docs.openstack.org/pbr/latest/
[pdm]: https://pdm.fming.dev/
[pyflow]: https://github.com/David-OConnor/pyflow
[pymsbuild]: https://github.com/zooba/pymsbuild

The Big List of Python Packaging and Distribution Tools:

[cs01-python-packaging]: https://grassfedcode.com/python-packaging/
-->

Install Poetry by downloading and running [get-poetry.py]:

```sh
python get-poetry.py
```

Open a new shell, or configure your current shell using the following command:

```sh
source ~/.poetry/env
```

Inside your repository, initialize a new Python project:

```sh
poetry init
```

This command will create a `pyproject.toml` file,
containing the package configuration in [TOML] format:


```{code-block} toml
---
caption: pyproject.toml
linenos: true
---

[tool.poetry]
name = "hypermodern-python"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

```{note}
The `pyproject.toml` configuration file was specified in [PEP 517] and [PEP 518],
and consists of two sections (or *tables*, in TOML parlance):

- The ``build-system`` table declares the requirements and entry point
  for building a distribution package for your project.
- The ``tool`` table contains sub-tables
  where tools can store configuration under their [PyPI] name.
  The `tool.poetry` sub-table
  contains the metadata for your package,
  such as its name, version, and authors,
  as well as the list of dependencies for the package.
```

Poetry added a dependency on Python 3.9,
because this is the Python version you ran it in.
Support the previous release as well by changing it to Python 3.8:

```{code-block} toml
---
lineno-start: 7
---

[tool.poetry.dependencies]
python = "^3.8"
```

The caret (`^`) in front of the version number means "up to the next major release".
In other words, you are promising that your package won't break when users upgrade to Python 3.9 or 3.10,
but giving no guarantees for its use with a future [Python 4.0].

Let's also update the metadata for the package:

```{code-block} toml
---
lineno-start: 1
---

[tool.poetry]
name = "hypermodern-python"
version = "0.1.0"
description = "The hypermodern Python project"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/<username>/<repository>"
repository = "https://github.com/<username>/<repository>"
```

```{seealso}
Refer to the [Poetry documentation][pyproject.toml]
for a detailed description of each configuration key.
```

## Creating a Python package

![opera06]

Let's create an initial skeleton package.
Organize your package in [src layout], like this:

```sh
hypermodern-python
├── pyproject.toml
└── src
    └── hypermodern_python
        └── __init__.py

3 directories, 2 files
```

The `hypermodern_python` directory contains a single empty file named `__init__.py`,
which turns it into an importable [Python package].

Use underscores in the package name `hypermodern_python`, rather than hyphens.
This ensures that the package name is a valid Python identifier,
unlike the repository name `hypermodern-python`.
These naming conventions are also known as [snake case] and [kebab case].

## Managing environments with Poetry

![opera07]

A [virtual environment] gives your project an isolated runtime environment,
consisting of a specific Python version and an independent set of installed Python packages.
This way, the dependencies of your current project do not interfere with the system-wide Python installation,
or other projects you're working on.

Poetry manages virtual environments for your projects.
To see it in action,
install the skeleton package using the command [poetry install]:

```sh
$ poetry install

Creating virtualenv hypermodern-python-PsI7ns-N-py3.9 in /root/.cache/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

Installing the current project: hypermodern-python (0.1.0)
```

Poetry created a virtual environment dedicated to your project,
and installed your initial package into it.
It also created a so-called *lock file*, named `poetry.lock`.
You will learn more about this file in the next section.

Let's run a Python session inside the new virtual environment,
using the command [poetry run]:

```sh
$ poetry run python

Python 3.9.0 (default, Oct 13 2020, 20:14:06)
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import hypermodern_python
>>>
```

There isn't much more we can do at the moment,
because our package does not contain any Python code yet.

## Managing dependencies with Poetry

![opera08]

Let's install the first dependency, the [click] package.
This Python package allows you to create beautiful command-line interfaces
in a composable way with as little code as necessary.
You can install dependencies using the command [poetry add]:

```sh
$ poetry add click

Using version ^7.1.2 for click

Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

Package operations: 1 install, 0 updates, 0 removals

  - Installing click (7.1.2)
```

Several things are happening here:

- The package is downloaded and installed into the virtual environment.
- The installed version is registered in the lock file `poetry.lock`.
- A more general version constraint is added to `pyproject.toml`.

The dependency entry in `pyproject.toml` contains a [version constraint] for the installed package: `^7.1.2`.
This means that users of the package need to have at least the current release, `7.1.2`.
The constraint also allows newer releases of the package,
as long as the version number does not indicate breaking changes.
([Semantic Versioning] limits breaking changes to major releases, once the version reaches `1.0.0`.)

By contrast, `poetry.lock` contains the exact version of `click` installed into the virtual environment.
Place this file under source control.
It allows everybody in your team to work with the same environment.
It also helps you [keep production and development environments as similar as possible][dev-prod-parity].

Upgrading the dependency to a new minor or patch release is now as easy as
invoking [poetry update] with the package name:

```sh
poetry update click
```

To upgrade to a new major release, use the following command instead:

```sh
poetry add click@latest
```

This will also update the version constraint.

## Command-line interfaces with click

![opera09]

Time to add some actual code to the package.
As you may have guessed, we're going to create a console application using `click`.
Create a file named `__main__.py` next to `__init__.py` with the following contents:

```{code-block} python
---
caption: src/hypermodern_python/\_\_main\_\_.py
linenos: true
---

import click

@click.command()
@click.version_option()
def main():
    """The hypermodern Python project."""
    click.echo("Hello, world!")
```

This module defines a minimal command-line application, supporting `--help` and `--version` options.

Register the script in `pyproject.toml`:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 17
---

[tool.poetry.scripts]
hypermodern-python = "hypermodern_python.__main__:main"
```

Finally, install the package into the virtual environment:

```sh
poetry install
```

You can now run the script like this:

```sh
$ poetry run hypermodern-python

Hello, world!
```

```{hint}
Prefixing the command by `poetry run` is only required during development.
When the application has been installed into its final location,
users can invoke it by typing `hypermodern-python` in their shell.
```

Let's use the `--help` option to print the usage message:

```sh
$ poetry run hypermodern-python --help

Usage: hypermodern-python [OPTIONS]

  The hypermodern Python project.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```

As you can see, 
`click` used the documentation string at the start of the `main` function to describe the command to the user.

The `--version` option displays the program version,
according to the package metadata:

```sh
$ poetry run hypermodern-python --version

hypermodern-python, version 0.1.0
```

Using the name `__main__.py` for this module is not a mere convention.
If you invoke Python with the option `-m` followed by the name of your package,
it executes this module, and sets its name to `__main__`.

```{tip}
Isn't this module always named `__main__`?
Actually, no.
When imported normally, the module name is `hypermodern_python.__main__`,
prefixed by the package name.
```

To leverage this, add two lines to the bottom of the module,
to invoke `main` when the module is run as a script:

```{code-block} python
---
caption: src/hypermodern_python/\_\_main\_\_.py
linenos: true
---

import click

@click.command()
@click.version_option()
def main():
    """The hypermodern Python project."""
    click.echo("Hello, world!")
    
if __name__ == "__main__":
    main(prog_name="hypermodern-python")
```

Pass the program name explicitly in the `prog_name` parameter.
This ensures that it is displayed properly in the `--help` output.

```{tip}
Do you find it confusing where the `prog_name` parameter comes from?
The parameter was not declared in our `main` function,
but the `@click.command` decorator turns that function into a `click.Command` object.
This object is callable and accepts some common keyword-arguments,
including `prog_name`.
```

Let's try it:

```sh
$ poetry run python -m hypermodern_python

Hello, world!
```

Invoking a script using Python's `-m` option can be advantageous in some situations:

- The script can be located using the Python module namespace rather than the filesystem.
- You don't require an entry-point script at all.
- You can specify [exactly which Python][xkcd1987] you want to run the application with.

## Example: Consuming an API with httpx

![opera10]

Let's build an example application that prints random facts to the console.
The data is retrieved from the [Wikipedia API].

Install [httpx], an HTTP client library:

```sh
poetry add httpx
```

```{note}
If you are familiar with [requests], httpx uses a very similar API.
```

Next, replace the file `src/hypermodern-python/__main__.py` with the source code shown below.

```{code-block} python
---
caption: src/hypermodern_python/\_\_main\_\_.py
linenos: true
---

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
```

Let's take a look at the imports at the top of the module first:

```{code-block} python
---
lineno-start: 1
---

import textwrap

import click
import httpx
```

The [textwrap] module from the standard library allows you to wrap lines when printing text to the console.
We also import the newly installed `httpx` package.
A blank line separates standard library modules from third party packages,
as recommended in [PEP 8].

The `API_URL` constant points to the [REST API] of the English Wikipedia,
or more specifically, its `/page/random/summary` endpoint,
which returns the summary of a random Wikipedia article:

```{code-block} python
---
lineno-start: 6
---

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
```

In the body of the `main` function,
the `httpx.get` invocation sends an [HTTP GET] request to the Wikipedia API.
Before looking at the response body, we check the HTTP status code and raise an exception if it signals an error.
The response body contains the resource data in [JSON] format,
which can be accessed using the `response.json()` method.

```{code-block} python
---
lineno-start: 12
---

    response = httpx.get(API_URL)
    response.raise_for_status()
    data = response.json()
```

We are only interested in the `title` and `extract` attributes,
containing the title of the Wikipedia page and a short plain text extract, respectively:

```{code-block} python
---
lineno-start: 16
---

    title = data["title"]
    extract = data["extract"]
```

Finally, we print the title and extract to the console, using the `click.echo` and `click.secho` functions.
The latter function allows you to specify the foreground color using the `fg` keyword attribute.
The `textwrap.fill` function wraps the text in `extract` so that every line is at most 70 characters long.

```{code-block} python
---
lineno-start: 19
---

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))
```

Let's try it out!

```sh
$ poetry run hypermodern-python

Jägersbleeker Teich
The Jägersbleeker Teich in the Harz Mountains of central Germany is a
storage pond near the town of Clausthal-Zellerfeld in the county of
Goslar in Lower Saxony. It is one of the Upper Harz Ponds that were
created for the mining industry.
```

Feel free to play around with this a little.
Here are some things you might want to try:

- Display a friendly error message when the API is not reachable.
- Add an option to select the Wikipedia edition for another language.
- If you feel adventurous: auto-detect the user's preferred language edition, using [locale].

## Uploading your package to PyPI

![opera01]

The [Python Package Index][PyPI] (PyPI) is Python's official package registry,
also known by its affectionate nickname "[the Cheese Shop][Cheese Shop sketch]".
Uploading your package to PyPI allows others to install it with [pip], like so:

```sh
pip install hypermodern-python
```

```{warning}
See the next section to avoid some pitfalls when using pip.
```

Create an account on [PyPI] using *Register* in the top menu.
Enable two-factor authentication for an additional layer of security.

Before you can upload your Python package, you need to generate *distribution packages*.
These are compressed archives which an end-user can download and install on their system.
They come in two flavours: source (or *sdist*) archives, and binary packages in the [wheel] format.
Poetry supports generating both with the [poetry build] command:

```sh
$ poetry build

Building hypermodern-python (0.1.0)
 - Building sdist
 - Built hypermodern-python-0.1.0.tar.gz

 - Building wheel
 - Built hypermodern_python-0.1.0-py3-none-any.whl
```

Poetry also supports uploading your package to PyPI, with the [poetry publish] command:

```sh
$ poetry publish

Publishing hypermodern-python (0.1.0) to PyPI
Username: <your-username>
Password:
 - Uploading hypermodern-python-0.1.0.tar.gz 100%
 - Uploading hypermodern_python-0.1.0-py3-none-any.whl 100%
```

```{note}
In the last chapter of this guide, we are going to automate the PyPI release process.
Automation helps you ensure your Python package passes all checks before it is published,
and keeps the build and upload process itself reliable.
```

## Installing packages with pip

![opera04]

With distribution archives of your package on PyPI,
users can add it as a dependency to their own Python projects.
Wheels and sdists are standard package formats in the Python world,
so this will also work with packaging tools other than Poetry.
For example, your package can be added to a [requirements.txt] or [Pipfile][pipenv] like any other package.

Users can also install your package and its entry-point script directly to their system.
In the case of our example application,
this allows them to invoke it as `hypermodern-python`,
without prefixing the command by `poetry run`,
and without having Poetry installed.

The most common way to do so is [pip],
the package installer that comes bundled with Python.
This is a simple and widely available installation method,
but it comes with two caveats:

1. Specify the target Python installation, by using `pythonX.Y -m pip` instead of plain `pip`.
   If you don't care about the minor version, `python3 -m pip` is also fine.
2. Keep your packages separate from the system installation.
   The `--user` option installs packages to a location in your home directory,
   the [per user site-packages directory][PEP 370].

For example, this would add your program to the user packages for Python 3.9:

```sh
python3.9 -m pip install --user hypermodern-python
```

```{note}
If the `python3.9` command cannot be located,
use `py -3.9` instead (on Windows),
or enable it with `pyenv shell 3.9.0` (if you're using pyenv).
```

Users also need to add the user script directory to their `PATH` environment variable.
This directory is located in `~/.local/bin` on Unix (including Mac), and `%APPDATA%\Python\Scripts` on Windows.
See the next section for a simple cross-platform way to take care of this.

## Installing applications with pipx

![opera04]

[pipx] is a higher-level tool built on top of pip,
and designed specifically for the installation of Python applications.
Its primary benefit is that applications are installed into isolated environments,
without polluting the system environment, or the environments of other applications.
This way, applications can use specific versions of their direct and indirect dependencies,
without getting in each other's way.

Install pipx using pip, and ensure the script directory is on your `PATH`:

```sh
python3.9 -m pip install --user pipx
python3.9 -m pipx ensurepath
```

Let's try pipx on our own application!

````{note}
If you already installed the application with pip in the previous section,
you should uninstall it first:

   ```sh
   python3.9 -m pip uninstall hypermodern-python
   ```
````

Installing applications with pipx is straightforward:

```sh
pipx install hypermodern-python
```

If all went well,
you should now be able to invoke your application directly:

```sh
$ hypermodern-python --version

hypermodern-python, version 0.1.0
```

## Summary

![opera05]

In this chapter, we set up a basic Python developer environment,
consisting of the following tools:

- [pyenv] (on Linux, Unix, and Mac)
- [py][Python launcher for Windows] (on Windows)
- [Poetry]
- [pipx]

We also created a simple Python package using Poetry,
with dependencies on [click] and [httpx].

Finally we published the package to [PyPI],
and installed it using pipx.

```{admonition} Credits
:class: seealso

The images in this chapter are details from the hand-colored print
*Le Sortie de l'opéra en l'an 2000*
(Leaving the opera in the year 2000)
by Albert Robida, ca 1902
(source: [Library of Congress][Albert Robida]).
```

[Albert Robida]: http://www.loc.gov/pictures/item/2007676247/
[BitBucket]: https://bitbucket.org/
[Cheese Shop sketch]: https://en.wikipedia.org/wiki/Cheese_Shop_sketch
[Debian]: https://www.debian.org/
[Fedora]: https://developer.fedoraproject.org/tech/languages/python/multiple-pythons.html
[GitHub]: https://github.com
[GitLab]: https://gitlab.com/
[HTTP GET]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
[JSON]: https://www.json.org/
[MIT license]: https://choosealicense.com/licenses/mit/
[PEP 370]: https://www.python.org/dev/peps/pep-0370
[PEP 517]: https://www.python.org/dev/peps/pep-0517/
[PEP 518]: https://www.python.org/dev/peps/pep-0518/
[PEP 8]: https://www.python.org/dev/peps/pep-0008/#imports
[Poetry]: https://python-poetry.org/
[PyPI]: https://pypi.org/
[Python 4.0]: https://twitter.com/gvanrossum/status/1306082472443084801?s=20
[Python launcher for Windows]: https://docs.python.org/3/using/windows.html#python-launcher-for-windows
[Python package]: https://docs.python.org/3/tutorial/modules.html#packages
[REST API]: https://restfulapi.net/
[Semantic Versioning]: https://semver.org/
[TOML]: https://toml.io/
[Ubuntu]: https://ubuntu.com/
[Wikipedia API]: https://www.mediawiki.org/wiki/REST_API
[Windows Subsystem for Linux]: https://docs.microsoft.com/en-us/windows/wsl/install-win10
[cjolowicz/hypermodern-python]: https://github.com/cjolowicz/hypermodern-python
[click]: https://click.palletsprojects.com/
[deadsnakes PPA]: https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa
[dev-prod-parity]: https://12factor.net/dev-prod-parity
[flit]: https://github.com/takluyver/flit
[get-poetry.py]: https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
[git-best-practices]: https://deepsource.io/blog/git-best-practices/
[httpx]: https://www.python-httpx.org/
[kebab case]: https://en.wiktionary.org/wiki/Kebab_case
[locale]: https://docs.python.org/3.8/library/locale.html
[opera01]: images/hypermodern-python-01/opera_crop01.jpg
[opera02]: images/hypermodern-python-01/opera_crop02.jpg
[opera03]: images/hypermodern-python-01/opera_crop03.jpg
[opera04]: images/hypermodern-python-01/opera_crop04.jpg
[opera05]: images/hypermodern-python-01/opera_crop05.jpg
[opera06]: images/hypermodern-python-01/opera_crop06.jpg
[opera07]: images/hypermodern-python-01/opera_crop07.jpg
[opera08]: images/hypermodern-python-01/opera_crop08.jpg
[opera09]: images/hypermodern-python-01/opera_crop09.jpg
[opera10]: images/hypermodern-python-01/opera_crop10.jpg
[pip-tools]: https://github.com/jazzband/pip-tools
[pip]: https://pip.pypa.io/
[pipenv]: https://pipenv.pypa.io/
[pipx]: https://pipxproject.github.io/pipx/
[poetry add]: https://python-poetry.org/docs/cli/#add
[poetry build]: https://python-poetry.org/docs/cli/#build
[poetry install]: https://python-poetry.org/docs/cli/#install
[poetry publish]: https://python-poetry.org/docs/cli/#publish
[poetry run]: https://python-poetry.org/docs/cli/#run
[poetry update]: https://python-poetry.org/docs/cli/#update
[pyenv-wiki]: https://github.com/pyenv/pyenv/wiki
[pyenv]: https://github.com/pyenv/pyenv
[pyproject.toml]: https://python-poetry.org/docs/pyproject/
[python.org]: https://www.python.org/downloads/
[requests]: https://requests.readthedocs.io/
[requirements.txt]: https://pip.pypa.io/en/stable/user_guide/#requirements-files
[setuptools]: http://setuptools.readthedocs.io
[snake case]: https://en.wikipedia.org/wiki/Snake_case
[src layout]: https://hynek.me/articles/testing-packaging/
[textwrap]: https://docs.python.org/3/library/textwrap.html
[version constraint]: https://python-poetry.org/docs/versions/
[virtual environment]: https://docs.python.org/3/tutorial/venv.html
[wheel]: https://www.python.org/dev/peps/pep-0427/ 
[xkcd1987]: https://xkcd.com/1987/