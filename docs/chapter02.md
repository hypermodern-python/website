# Testing

In this second chapter,
we're going to add automated testing to your project,
and teach the random fact generator foreign languages.

- [View changes](https://github.com/cjolowicz/hypermodern-python/compare/chapter01...chapter02)
- [Download code](https://github.com/cjolowicz/hypermodern-python/archive/chapter02.zip)

## Unit testing with pytest

![verne-oxen]

It's never too early to add unit tests to a project. 
Unit tests, as the name says, verify the functionality of a *unit of code*,
such as a single function or class.
While the [unittest] framework is part of the Python standard library,
[pytest] has become somewhat of a *de facto* standard.

Let's add this package as a development dependency,
using [poetry add] with the `--dev` option:

```sh
poetry add --dev pytest
```

<!--
```{note}
Dependencies are Python packages used by your project,
and they come in two types:

- *Core dependencies* are required by users running your code,
  and typically consist of third-party libraries imported by your package.
  When your package is distributed,
  the package metadata includes these dependencies,
  allowing tools like pip to automatically install them alongside your package.

- *Development dependencies* are only required by developers working on your code.
  Examples are applications used to run tests,
  to check code for style and correctness,
  or to build documentation.
  These dependencies are not a part of distribution packages,
  because users do not require them to run your code.
```
-->

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

<!--
Like its older sibling [tox],
Nox makes it easy to run any kind of job in an isolated environment,
with only those dependencies installed that the job needs.
-->

Install Nox via [pipx]:

```sh
pipx install nox
```

<!--
```{note}
Do not install Nox as a development dependency with Poetry.
Nox is a part of your global developer environment, like Poetry, pyenv, and pipx.
All of these tools are in a sense environment managers.
It's better to decouple them than to
enter a complex situation where environments are spawned from other environments.
To quote the [Zen of Python][PEP 20],
"Flat is better than nested."
```
-->

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

<!--
```{note}
Quotes are optional unless your shell is [zsh],
which assigns special meaning to square brackets.
```
-->

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

<!--
This is an indicator of missing branch coverage.

The `if` clause is missing from coverage because
its condition only evaluates to `True` when the module is run as a script.

```{note}
Branch coverage may seem redundant here, but consider the opposite case:
If the condition always evaluates to `True`, the body of the `if` statement is never skipped.
Statement coverage will only see that all lines of code were executed.
But skipping the body could conceivably break code after the `if` block.
This specific code path is never executed by the test suite.
Branch coverage alerts us to this situation.
```

Exercising this code path from the test suite is not impossible
(see [runpy] from the standard library for one approach).
-->

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
write a failing test before implementing a feature or fixing a bug.
```

## Automating coverage using Nox

![verne-white-dog]

In this section, we update the Nox session to collect coverage data when running tests.
We also add a Nox session to display the coverage report on the terminal.

But first we need to configure Coverage.py for its use in Nox environments.
There are two differences compared to running tests in the Poetry environment
that we need to account for:

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

Add a second session named `coverage`.
This session combines the coverage data from all the test runs.
It then generates the final coverage report.
The coverage session runs on the same Python version as Nox itself,
using the `@nox.session` decorator without arguments.

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
Here's the updated `tests` session:

```{code-block} python
---
caption: noxfile.py
linenos: true
lineno-start: 3
---

@nox.session(python=["3.9", "3.8"])
def tests(session):
    try:
        session.install("pytest", "coverage[toml]", ".")
        session.run("coverage", "run", "-m", "pytest", *session.posargs)
    finally:
        session.notify("coverage")
```

## Mocking with pytest-mock

![verne-landing]

Unit tests should be [fast, isolated, and repeatable][testing-first-principle].
The test for `__main__.main` is neither of these:

- It is not fast,
  because it takes a full round-trip to the Wikipedia API to complete.
- It does not run in an isolated environment,
  because it sends out an actual request over the network.
- It is not repeatable,
  because its outcome depends on the health, reachability, and behavior of the API.
  In particular, the test fails whenever the network is down.

The [unittest.mock] standard library allows you to replace parts of your system under test with mock objects.
Use it via the [pytest-mock] plugin, which integrates the library with `pytest`:

```sh
poetry add --dev pytest-mock
```

The plugin provides a `mocker` fixture,
which functions as a thin wrapper around the standard mocking library.
Use `mocker.patch` to replace the `httpx.get` function by a mock object.
The mock object will be useful for any test case involving the Wikipedia API,
so let's create a test fixture for it:

```python
# tests/test_main.py
@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")
```

Add the fixture to the function parameters of the test case:

```python
def test_main_succeeds(runner, mock_requests_get):
    ...
```
    
If you run Nox now,
the test fails because click expects to be passed a string for console output,
and receives a mock object instead.
Simply "knocking out" `requests.get` is not quite enough.
The mock object also needs to return something meaningful,
namely a response with a valid JSON object.

When a mock object is called, or when an attribute is accessed, it returns another mock object.
Sometimes this is sufficient to get you through a test case.
When it is not, you need to *configure* the mock object.
To configure an attribute, you simply set the attribute to the desired value.
To configure the return value for when the mock is called,
you set `return_value` on the mock object as if it were an attribute.

Let's look at the example again:

```python
with requests.get(API_URL) as response:
    response.raise_for_status()
    data = response.json()
```

The code above uses the response as a [context manager].
The `with` statement is syntactic sugar for the following slightly simplified pseudocode:

```python
context = requests.get(API_URL)
response = context.__enter__()

try:
    response.raise_for_status()
    data = response.json()
finally:
    context.__exit__(...)
```

So what you have is essentially a chain of function calls:

```python
data = requests.get(API_URL).__enter__().json()
```

Rewrite the fixture, and mirror this call chain when you configure the mock:

```python
@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock
```
    
Invoke Nox again to see that the test suite passes. 🎉

```sh
$ nox -r
...
nox > Ran multiple sessions:
nox > * tests-3.8: success
nox > * tests-3.7: success
```

Mocking not only speeds up your test suite,
or lets you hack offline on a plane or train.
By virtue of having a fixed, or deterministic, return value, the mock also enables you to write repeatable tests.
This means you can, for example, check that the title returned by the API is printed to the console:

```python
def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output
```

Additionally, mocks can be inspected to see if they were called, using the mock's [called] attribute.
This provides you with a way to check that `requests.get` was invoked to send a request to the API:

```python
# tests/test_console.py
def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called
```

Mock objects also allow you to inspect the arguments they were called with, using the [call_args] attribute.
This allows you to check the URL passed to `requests.get`:

```python
# tests/test_console.py
def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]
```

You can configure a mock to raise an exception instead of returning a value
by assigning the exception instance or class to the [side_effect] attribute of the mock.
Let's check that the program exits with a status code of 1 on request errors:

```python
# tests/test_console.py
def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
```

You should generally have a single assertion per test case,
because more fine-grained test cases make it easier to figure out
why the test suite failed when it does.

Tests for a feature or bugfix should be written *before* implementation.
This is also known as "[writing a failing test]".
The reason for this is that
it provides confidence that the tests are actually testing something,
and do not simply pass because of a flaw in the tests themselves.

## Example: Refactoring

![verne-fish]

The great thing about a good test suite is that
it allows you to refactor your code without fear of breaking it.
Let's move the Wikipedia client to a separate module.
Create a file `src/hypermodern-python/wikipedia.py` with the following contents:

```python
# src/hypermodern-python/wikipedia.py
import requests

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

def random_page():
    with requests.get(API_URL) as response:
        response.raise_for_status()
        return response.json()
```

The `console` module can now simply invoke `wikipedia.random_page`:

```python
# src/hypermodern-python/console.py
import textwrap

import click

from . import __version__, wikipedia

@click.command()
@click.version_option(version=__version__)
def main():
    """The hypermodern Python project."""
    data = wikipedia.random_page()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))
```

Finally, invoke Nox to see that nothing broke:

```sh
$ nox -r
...
nox > Ran multiple sessions:
nox > * tests-3.8: success
nox > * tests-3.7: success
```

## Example: Handling exceptions

![verne-tower]

If you run the example application without an Internet connection,
your terminal will be filled with a long traceback.
This is what happens when
the Python interpreter is terminated by an unhandled exception.
For common errors such as this,
it would be better to print a friendly, informative message to the screen.

Let's express this as a test case, by configuring the mock to raise a `RequestException`.
(The *requests* library has more specific exception classes,
but for the purposes of this example, we will only deal with the base class.)

```python
# tests/test_console.py
import requests

def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
```

The simplest way to get this test to pass is by converting the `RequestException` into a `ClickException`.
When click encounters this exception,
it prints the exception message to standard error and
exits the program with a status code of 1.
You can reuse the exception message by converting the original exception to a string.

Here is the updated `wikipedia` module:

```python
# src/hypermodern-python/wikipedia.py
import click
import requests

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

def random_page():
    try:
        with requests.get(API_URL) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
```

## Example: Selecting the Wikipedia language edition

![verne-boat]

In this section, we add a command-line option to
select the [language edition][wikipedia-language-editions] of Wikipedia. 

Wikipedia editions are identified by a language code,
which is used as a subdomain below wikipedia.org.
Usually, this is the two-letter or three-letter language code
assigned to the language by [ISO 639-1] and [ISO 639-3].
Here are some examples:

- `fr` for the French Wikipedia
- `jbo` for the [Lojban Wikipedia]
- `ceb` for the [Cebuano Wikipedia]

As a first step, let's add an optional parameter for the language code to the `wikipedia.random_page` function.
When an alternate language is passed, the API request should be sent to the corresponding Wikipedia edition.
The test case is placed in a new test module named `test_wikipedia.py`:

```python
# tests/test_wikipedia.py
from hypermodern_python import wikipedia

def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]
```

The `mock_requests_get` fixture is now used by two test modules.
You could move it to a separate module and import from there,
but Pytest offers a [more convenient way][pytest-conftest-py]:
Fixtures placed in a `conftest.py` file are discovered automatically,
and test modules at the same directory level can use them without explicit import.
Create the new file at the top-level of your tests package,
and move the fixture there:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock
```

To get the test to pass,
we turn `API_URL` into a format string,
and interpolate the specified language code into the URL using [str.format]:

```python
# src/hypermodern-python/wikipedia.py
import click
import requests

API_URL = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"

def random_page(language="en"):
    url = API_URL.format(language=language)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
```

As the second step,
we make the new functionality accessible from the command line,
adding a `--language` option.
The test case mocks the `wikipedia.random_page` function,
and uses the [assert_called_with] method on the mock
to check that the language specified by the user is passed on to the function:

```python
# tests/test_console.py
@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("hypermodern_python.wikipedia.random_page")

def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")
```

We are now ready to implement the new functionality using the [click.option] decorator.
Without further ado, here is the final version of the `console` module:

```python
# src/hypermodern-python/console.py
import textwrap

import click

from . import wikipedia

@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option()
def main(language):
    """The hypermodern Python project."""
    data = wikipedia.random_page(language=language)

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))
```

You now have a polyglot random fact generator,
and a fun way to test your language skills
(and the Unicode skills of your terminal emulator).

## Using fakes

![verne-black-dog]

Mocks help you test code units depending on bulky subsystems,
but they are [not the only technique][test-doubles-fakes-mocks-stubs] to do so.
For example, if your function requires a database connection,
it may be both easier and more effective to pass an in-memory database than a mock object.
Fake implementations are a good alternative to mock objects,
which can be too forgiving when faced with wrong usage,
and too tightly coupled to implementation details of the system under test
(witness the `mock_requests_get` fixture).
Large data objects can be generated by test object factories,
instead of being replaced by mock objects
(check out the excellent [factoryboy] package).

Implementing a fake API is out of the scope of this tutorial,
but we will cover one aspect of it:
How to write a fixture which requires tear down code as well as set up code.
Suppose you have written the following fake API implementation:

```python
class FakeAPI:
    url = "http://localhost:5000/"

    @classmethod
    def create(cls):
        ...
    
    def shutdown(self):
        ...
```

The following will not work:

```python
@pytest.fixture
def fake_api():
    return FakeAPI.create()
```

The API needs to be shut down after use,
to free up resources such as the TCP port and the thread running the server.
You can do this by writing the fixture as a [generator]:

```python
@pytest.fixture
def fake_api():
    api = FakeAPI.create()
    yield api
    api.shutdown()
```

Pytest takes care of running the generator,
passing the yielded value to your test function,
and executing the shutdown code after it returns.
If setting up and tearing down the fixture is expensive,
you may also consider extending the [scope][pytest-scope] of the fixture.
By default, fixtures are created once per test function.
Instead, you could create the fake API server once per test session:

```python
@pytest.fixture(scope="session")
def fake_api():
    api = FakeAPI.create()
    yield api
    api.shutdown()
```

## End-to-end testing

![verne-capsule]

Testing against the live production server is bad practice for unit tests,
but there is nothing like the confidence you get
from seeing your code work in a real environment.
Such tests are known as *end-to-end tests*,
and while they are usually too slow, brittle, and unpredictable
for the kind of automated testing
you would want to do on a CI server or in the midst of development,
they do have their place.

Let's reinstate the original test case,
and use Pytest's [markers][pytest-markers] to apply a custom mark.
This will allow you to select or skip them later,
using Pytest's `-m` option.

```python
# tests/test_console.py
@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
```

Register the `e2e` marker using the `pytest_configure` hook, as shown below.
The hook is placed in the `conftest.py` file,
at the top-level of your tests package.
This ensures that Pytest can discover the module
and use it for the entire test suite.

```python
# tests/conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
```

Finally, exclude end-to-end tests from automated testing
by passing `-m "not e2e"` to Pytest:

```python
# noxfile.py
import nox

@nox.session(python=["3.8", "3.7"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
```

You can now run end-to-end tests by passing `-m e2e` to the Nox session,
using a double dash (`--`) to separate them from Nox's own options.
For example, here's how you would run end-to-end tests
inside the testing environment for Python 3.8:

```sh
nox -rs tests-3.8 -- -m e2e
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
[Cebuano Wikipedia]: https://en.wikipedia.org/wiki/Lsjbot
[Coverage.py]: https://coverage.readthedocs.io/
[ISO 639-1]: https://en.wikipedia.org/wiki/ISO_639-1
[ISO 639-3]: https://en.wikipedia.org/wiki/ISO_639-3
[Internet Archive]: https://archive.org/details/delaterrelalu00vern
[Lojban Wikipedia]: https://xkcd.com/191/
[Nox]: https://nox.thea.codes/
[PEP 20]: https://www.python.org/dev/peps/pep-0020
[The Public Domain Review]: https://publicdomainreview.org/collection/emile-antoine-bayard-s-illustrations-for-around-the-moon-by-jules-verne-1870
[assert_called_with]: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called_with
[call_args]: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args
[called]: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.called
[click.option]: https://click.palletsprojects.com/en/7.x/options/
[context manager]: https://docs.python.org/3/reference/datamodel.html#context-managers
[core-metadata-provides-extra]: https://packaging.python.org/specifications/core-metadata/#provides-extra-multiple-use
[coverage-combine]: https://coverage.readthedocs.io/en/coverage-5.3/cmd.html#combining-data-files-coverage-combine
[coverage-excluding-code]: https://coverage.readthedocs.io/en/coverage-5.3/excluding.html
[factoryboy]: https://factoryboy.readthedocs.io/
[fail_under]: https://coverage.readthedocs.io/en/stable/config.html#report
[generator]: https://docs.python.org/3/tutorial/classes.html#generators
[ned-batchelder-blog-include-your-tests]: https://nedbatchelder.com/blog/202008/you_should_include_your_tests_in_coverage.html
[nox-reuse-existing-virtualenvs]: https://nox.thea.codes/en/stable/usage.html#re-using-virtualenvs
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pipxproject.github.io/pipx/
[poetry add]: https://python-poetry.org/docs/cli/#add
[pytest-conftest-py]: https://pytest.readthedocs.io/en/latest/fixture.html#conftest-py-sharing-fixture-functions
[pytest-cov]: https://pytest-cov.readthedocs.io/en/latest/
[pytest-fixture]: https://docs.pytest.org/en/latest/fixture.html
[pytest-good-practices]: http://doc.pytest.org/en/latest/goodpractices.html#tests-outside-application-code
[pytest-markers]: https://docs.pytest.org/en/latest/example/markers.html
[pytest-mock]: https://github.com/pytest-dev/pytest-mock
[pytest-scope]: https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session
[pytest]: https://docs.pytest.org/en/latest/
[runpy]: https://docs.python.org/3/library/runpy.html
[session.posargs]: https://nox.thea.codes/en/stable/config.html#passing-arguments-into-sessions
[side_effect]: https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
[str.format]: https://docs.python.org/3/library/stdtypes.html#str.format
[test-doubles-fakes-mocks-stubs]: https://blog.pragmatists.com/test-doubles-fakes-mocks-and-stubs-1a7491dfa3da
[testing-first-principle]: http://agileinaflash.blogspot.com/2009/02/first.html
[tox]: https://tox.readthedocs.io/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
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
[wikipedia-language-editions]: https://en.wikipedia.org/wiki/List_of_Wikipedias
[writing a failing test]: https://www.icemobile.com/uploads/inline/test.driven.development.cartoon_0.jpeg
[zsh]: https://www.zsh.org/
