# Testing

In this second chapter,
we're going to add automated testing to your project.

- [View changes](https://github.com/cjolowicz/hypermodern-python/compare/chapter01...chapter02)
- [Download code](https://github.com/cjolowicz/hypermodern-python/archive/chapter02.zip)

## Testing with pytest

![verne-oxen]

It's never too early to add tests to a project. 
While the [unittest] framework is part of the Python standard library,
[pytest] has become somewhat of a *de facto* standard.

Let's add this package as a development dependency,
using [poetry add] with the `--dev` option:

```sh
poetry add --dev pytest
```

Organize tests in a [separate file hierarchy][pytest-good-practices] next to `src`, named `tests`:

```sh
hypermodern-python
├── src
└── tests
    ├── __init__.py
    └── test_main.py

3 directories, 2 files
```

The file `__init__.py` is empty and turns the test suite into a Python package.
This arrangement allows it to mirror the source layout of the package under test,
even when modules in different parts of the source tree have the same name.
Furthermore, it gives you the option to import modules from within your tests package.

The file `test_main.py` contains tests for the `__main__` module.
Our first test case checks whether the program exits with a status code of zero:

```{code-block} python
---
caption: tests/test_main.py
linenos: true
---

import click.testing

from hypermodern_python import __main__

def test_main_succeeds():
    runner = click.testing.CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
```

The test case uses `click.testing.CliRunner` to invoke the command-line interface in an isolated way.
This class makes it easy to inspect the output and exit code of your program without launching a subprocess.
Most test cases in the `test_main` module will need a `runner` instance.
Let's turn `runner` into a reusable *fixture*.

[Test fixtures][pytest-fixture] are simple functions declared with the `pytest.fixture` decorator.
Test cases can use a fixture by including a function parameter with the same name.
When the test case is run, the parameter receives the return value of the fixture function.

```{code-block} python
---
caption: tests/test_main.py
linenos: true
---

import click.testing
import pytest

from hypermodern_python import __main__

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
```

Invoke `pytest` to run the test suite:

```pytest
$ poetry run pytest
======================== test session starts ========================
platform linux -- Python 3.9.0, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /root/hypermodern-python
collected 1 item

tests/test_main.py .                                           [100%]

========================= 1 passed in 1.20s =========================
```

## Test automation with Nox

![verne-steam-rocket]

[Nox] automates testing in multiple Python environments.
Nox sessions are defined in a Python file named `noxfile.py`,
located in the project directory.
They consist of a virtual environment
and a set of commands to run in that environment.

```{hint}
Both Poetry and Nox set up virtual environments for your project.
While the Poetry environment lets you interact with your package during development,
Nox environments are useful for running checks in a repeatable way across multiple Python versions.
```

Install Nox via [pipx]:

```sh
pipx install nox
```

Create a `noxfile.py` with the following contents:

```{code-block} python
---
caption: noxfile.py
linenos: true
---

import nox

@nox.session(python=["3.9", "3.8"])
def tests(session):
    session.install("pytest", ".")
    session.run("pytest")
```

This file defines a session named `tests` that installs and runs pytest.
The second argument to `session.install` refers to the current directory, containing your Poetry project.
This means that the session installs your package into the same environment as pytest.

Invoke `nox` without options,
and it will create a virtual environment for each listed Python version,
and run the session inside it:

```sh
$ nox

nox > Running session tests-3.9
nox > Creating virtual environment (virtualenv) using python3.9 in .nox/tests-3-9
nox > pip install . pytest
nox > pytest
...
nox > Session tests-3.9 was successful.
nox > Running session tests-3.8
nox > Creating virtual environment (virtualenv) using python3.8 in .nox/tests-3-8
nox > pip install . pytest
nox > pytest
...
nox > Session tests-3.8 was successful.
nox > Ran multiple sessions:
nox > * tests-3.9: success
nox > * tests-3.8: success
```

```{hint}
How does `session.install(".")` actually get your package installed?
Behind the scenes, Nox forwards `session.install` arguments to [pip].
When passed a directory with a `pyproject.toml`,
pip builds and installs a wheel from it using the specified build backend.
In this case, the directory contains your Python package,
and the build backend is Poetry.
```

By default, Nox runs every session defined in `noxfile.py`,
but you can narrow this down:

- Use the `--session` option to restrict runs to a specific session.
- Use the `--python` option to restrict runs to a specific Python version.

Virtual environments are created from scratch on each invocation.
While this is a safe default,
you may find you need to speed things up during development.
Use the `--reuse-existing-virtualenvs` option to reuse environments when they already exist.
Here is an example of how you would re-run the test suite in the existing environment for Python 3.9:

```sh
nox --python=3.9 --session=tests --reuse-existing-virtualenvs
```

You can abbreviate this command using short options:

```sh
nox -p 3.9 -rs tests
```

Nox allows you to pass arbitrary options to a session after the `--` separator.
These session options are available via the [session.posargs] variable.
This means we can pass additional options to `pytest`, which is quite useful.
Let's modify the session to forward the session options to `pytest`:

```{code-block} python
---
caption: noxfile.py
linenos: true
---

import nox

@nox.session(python=["3.9", "3.8"])
def tests(session):
    session.install("pytest", ".")
    session.run("pytest", *session.posargs)
```

You can use this, for example, to run specific test modules or test functions:

```sh
nox --session=tests -- tests/test_main.py
nox --session=tests -- -k test_main_succeeds
```

Another example would be increasing pytest's verbosity:

```sh
nox --session=tests -- --verbose
```

## Code coverage with Coverage.py

![verne-starry-sky]

*Code coverage* is a measure of the degree to which
the source code of your program is executed while running its test suite.
The code coverage of Python programs can be determined using a tool called [Coverage.py].
Install it as a development dependency using Poetry:

```sh
poetry add --dev 'coverage[toml]'
```

The `[toml]` [extra][core-metadata-provides-extra] allows
Coverage.py to read its configuration from `pyproject.toml`.
Let's add the following contents to this file:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 21
---

[tool.coverage.run]
source = ["hypermodern_python", "tests"]
branch = true

[tool.coverage.report]
show_missing = true
```

We have added three configuration options for Coverage.py:

- The `tool.coverage.run.source` option specifies for which packages to collect coverage data.
  List the name of your package,
  [as well as the test suite][ned-batchelder-blog-include-your-tests] itself.

- The `tool.coverage.run.branch` option activates branch coverage.
  While statement coverage flags lines of code that are not executed,
  branch coverage allows you to identify uncovered branches in conditional code,
  such as `if...else` constructs.

- The `tool.coverage.report.show_missing` option enables the display of line numbers for missing coverage.

Coverage.py comes with a command-line interface named `coverage`.
In the simplest case, checking test coverage is a two-step process:

- `coverage run` executes a script or module (via the `-m` option) and collects coverage data.
- `coverage report` analyzes the coverage data and prints a textual summary.

```{tip}
The form `coverage run -m pytest` is a convenient way to
use the pytest package from the active environment.
```

Let's try this with our test suite:

```pytest
$ poetry run coverage run -m pytest

============================ test session starts =============================
platform linux -- Python 3.9.0, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /root/hypermodern-python
collected 1 item

tests/test_main.py .                                                   [100%]

============================= 1 passed in 0.74s ==============================

$ poetry run coverage report

Name                                 Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------
src/hypermodern_python/__init__.py       0      0      0      0   100%
src/hypermodern_python/__main__.py      16      1      2      1    89%   25->26, 26
tests/__init__.py                        0      0      0      0   100%
tests/test_main.py                       9      0      0      0   100%
--------------------------------------------------------------------------------
TOTAL                                   25      1      2      1    93%
```

The coverage report shows missing coverage at the end of the `__main__.py` module.
Let's inspect the `Missing` column more closely:

- `25->26` tells us that the condition on line `25` never evaluated to `True`.
- `26` tells us that line `26` was never executed.

Here are the relevant lines from `__main__.py` again:

```{code-block} python
---
lineno-start: 24
---


if __name__ == "__main__":
    main(prog_name="hypermodern_python")
```

`if __name__ == "__main__"` blocks are often [excluded from coverage][coverage-excluding-code]:
They are trivial boilerplate, yet cumbersome to exercise from a test.
Code can be excluded from Coverage.py using two main methods:

- The configuration option `tool.coverage.report.exclude_lines` takes a list of regular expressions.
- You can apply a special marker comment to a line or block of code: `# pragma: no cover`

We will take the second approach here:

```{code-block} python
---
lineno-start: 24
---


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="hypermodern_python")
```

Aiming for full code coverage is generally a good idea, especially for a fresh code base.
Anything less than that implies that some part of your code base is definitely untested.
And to quote [Bruce Eckel], "If it's not tested, it's broken."
Later, we will see some tools that help you achieve extensive code coverage.

Configure Coverage.py to require full test coverage (or any other target percentage)
using the option `tool.coverage.report.fail_under`:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 25
---

[tool.coverage.report]
fail_under = 100
```

```{important}
Code coverage tells you which lines and branches in your code base were hit.
This does not imply that your test suite has meaningful test cases for all uses and misuses of your program.
Take our test case, for example:
It did not check the functionality of the program at all, only its exit status;
yet it achieved full coverage.
A good way to build up a battery of meaningful tests is to
[write a failing test][cartoon-tdd] before implementing a feature or fixing a bug.
```

## Automating coverage using Nox

![verne-white-dog]

In this section, we update the Nox session to collect coverage data when running tests.
We also add a Nox session to display the coverage report on the terminal.

But first we need to configure Coverage.py for its use in Nox environments.
Compared to running tests in the Poetry environment,
there are two differences that we should account for:

- The Nox session runs the test suite against the installed package.
  In the Poetry environment, tests run against the source tree in your working directory.
- Tests are run with different versions of Python.
  Coverage reports should include coverage data from all of them.

To start with, configure Coverage.py to run in [parallel mode][coverage-combine].
This causes Coverage.py to create separate data files for every run,
rather than erasing the previous coverage data at each run.
The data files can be combined later on using the `coverage combine` command.
Enable parallel mode using the `tool.coverage.run.parallel` option:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 16
---

[tool.coverage.run]
parallel = true
```

Filenames in coverage data point to the installed package in the Nox environment.
Not only are those paths hard to read, they also depend on the Python version used.
Let's tell Coverage.py how to map the paths back to the source code,
so the coverage data can be aggregated correctly for the coverage report.
This is done using the `tool.coverage.paths` option:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 16
---


[tool.coverage.paths]
source = ["src", "*/site-packages"]
```

```{note}
Entries under `tool.coverage.paths` list paths that are considered equivalent:

- The first value in an entry is the location of the source code
  (the `src` directory in your project).

- The second value is a file pattern to match against paths of collected data.
  Python packages are installed into a directory named `site-packages`,
  so we use this name in a wildcard pattern.
```

The listing below shows the full Coverage configuration at this point:

```{code-block} toml
---
caption: pyproject.toml
lineno-start: 16
---


[tool.coverage.run]
source = ["hypermodern_python", "tests"]
branch = true
parallel = true

[tool.coverage.paths]
source = ["src", "*/site-packages"]

[tool.coverage.report]
fail_under = 100
show_missing = true
```

With this in place, we are ready to automate code coverage using Nox.

Adapt the `tests` session to collect coverage data when running tests:

```{code-block} python
---
caption: noxfile.py
linenos: true
---

import nox

@nox.session(python=["3.9", "3.8"])
def tests(session):
    session.install("pytest", "coverage[toml]", ".")
    session.run("coverage", "run", "-m", "pytest", *session.posargs)
```

Now add a second session named `coverage`:

```{code-block} python
---
caption: noxfile.py
linenos: true
lineno-start: 8
---

@nox.session
def coverage(session):
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
```

This session combines the coverage data from all the test runs, using `coverage combine`.
It then generates and displays the final coverage report, using `coverage report`.

```{note}
You can use the `@nox.session` decorator without specifying a Python version.
The session will run on the same Python interpreter as Nox itself.
```

If you run the `tests` session on its own,
your working directory will be littered with data files
waiting to be processed by `coverage combine`.
What's worse, the coverage data in these files gets stale over time.
This means that coverage reports may no longer reflect the current state of the code base.

Let's trigger the coverage session to run automatically
when the test suite has completed.
Nox supports this with the `session.notify` method.
If the notified session is not already selected,
it runs after all other sessions have completed.
A `try...finally` block ensures that
we get a coverage report even if a test failed.

Here's the full `noxfile.py` with the updated `tests` session:

```{code-block} python
---
caption: noxfile.py
linenos: true
---

import nox

@nox.session(python=["3.9", "3.8"])
def tests(session):
    try:
        session.install("pytest", "coverage[toml]", ".")
        session.run("coverage", "run", "-m", "pytest", *session.posargs)
    finally:
        session.notify("coverage")

@nox.session
def coverage(session):
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
```

```{admonition} Credits
:class: seealso

The images in this chapter come from Émile-Antoine Bayard's illustrations for
From the Earth to the Moon
(De la terre à la lune)
by Jules Verne (1870)
(source: [Internet Archive] via [The Public Domain Review]).
```

[Bruce Eckel]: https://en.wikipedia.org/wiki/Bruce_Eckel
[Coverage.py]: https://coverage.readthedocs.io/
[Internet Archive]: https://archive.org/details/delaterrelalu00vern
[Nox]: https://nox.thea.codes/
[The Public Domain Review]: https://publicdomainreview.org/collection/emile-antoine-bayard-s-illustrations-for-around-the-moon-by-jules-verne-1870
[core-metadata-provides-extra]: https://packaging.python.org/specifications/core-metadata/#provides-extra-multiple-use
[coverage-combine]: https://coverage.readthedocs.io/en/coverage-5.3/cmd.html#combining-data-files-coverage-combine
[coverage-excluding-code]: https://coverage.readthedocs.io/en/coverage-5.3/excluding.html
[fail_under]: https://coverage.readthedocs.io/en/stable/config.html#report
[ned-batchelder-blog-include-your-tests]: https://nedbatchelder.com/blog/202008/you_should_include_your_tests_in_coverage.html
[nox-reuse-existing-virtualenvs]: https://nox.thea.codes/en/stable/usage.html#re-using-virtualenvs
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pipxproject.github.io/pipx/
[poetry add]: https://python-poetry.org/docs/cli/#add
[pytest-fixture]: https://docs.pytest.org/en/latest/fixture.html
[pytest-good-practices]: http://doc.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
[pytest]: https://docs.pytest.org/en/latest/
[session.posargs]: https://nox.thea.codes/en/stable/config.html#passing-arguments-into-sessions
[tox]: https://tox.readthedocs.io/
[unittest]: https://docs.python.org/3/library/unittest.html
[verne-black-dog]: images/verne-black-dog.jpg
[verne-boat]: images/verne-boat.jpg
[verne-capsule]: images/verne-capsule.jpg
[verne-fish]: images/verne-fish.jpg
[verne-landing]: images/verne-landing.jpg
[verne-oxen]: images/verne-oxen.jpg
[verne-starry-sky]: images/verne-starry-sky.jpg
[verne-steam-rocket]: images/verne-steam-rocket.jpg
[verne-tower]: images/verne-tower.jpg
[verne-white-dog]: images/verne-white-dog.jpg
[cartoon-tdd]: https://www.icemobile.com/uploads/inline/test.driven.development.cartoon_0.jpeg
