# Hypermodern Python

```{toctree}
:hidden:
Setup <chapter01>
Testing <chapter02>
Linting <chapter03>
Typing <chapter04>
Documentation <chapter05>
CI/CD <chapter06>
```

![opera04]

This article series [^*] is a guide to modern Python tooling
with a focus on simplicity and minimalism.
It walks you through the creation of a complete Python project structure,
with unit tests, static analysis, type-checking, documentation, and continuous integration and delivery.

The guide is aimed at intermediate developers
and presumes basic knowledge of the Python programming language.
You may also find it an interesting read if you are already a seasoned Python developer,
but want to see how to implement best practices with a new generation of Python tools. [^+]

This guide has a companion repository: [cjolowicz/hypermodern-python].
Each article in the guide corresponds to a set of commits in the GitHub repository.

```{tip}
For a project template based on this guide,
check out the [Hypermodern Python Cookiecutter].
```

```{admonition} Requirements
You need a recent Linux, Unix, or Mac system with
[curl] and [git] for this tutorial,
or Windows 10 with [Git for Windows].
```

[^*]: The title of this guide is inspired by the book
*Die hypermoderne Schachpartie* (The hypermodern chess game),
written by [Savielly Tartakower] in 1924.
It surveys the revolution that had taken place in chess theory in the decade after the First World War.

[^+]: If you are a complete beginner,
I would recommend to read an introductory book first,
for example [Automate the Boring Stuff with Python],
or any of the learning resources listed in [The Hitchhiker's Guide to Python].

[opera04]: images/hypermodern-python-01/opera_crop04.jpg
[bash]: https://www.gnu.org/software/bash/
[curl]: https://curl.haxx.se
[git]: https://www.git-scm.com
[Git for Windows]: https://gitforwindows.org/
[Savielly Tartakower]: https://en.wikipedia.org/wiki/Savielly_Tartakower
[Automate the Boring Stuff with Python]: https://automatetheboringstuff.com/
[The Hitchhiker's Guide to Python]: https://docs.python-guide.org/intro/learning/
[cjolowicz/hypermodern-python]: https://github.com/cjolowicz/hypermodern-python
[Hypermodern Python Cookiecutter]: https://cookiecutter-hypermodern-python.readthedocs.io/
