FROM ubuntu:20.10 as base
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y curl git

###############################################################################
#                                 Chapter 01                                  #
###############################################################################

#
# Creating a repository on GitHub
#

FROM base as github
ENV PROJECT hypermodern-python
ENV PACKAGE hypermodern_python
WORKDIR /root/$PROJECT
COPY hypermodern-python/README.md .
COPY hypermodern-python/LICENSE .

#
# Installing Python with pyenv
#

FROM github as pyenv
RUN curl https://pyenv.run | bash
RUN echo 'export PATH="~/.pyenv/bin:$PATH"' >> /root/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> /root/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc
ENV PATH /root/.pyenv/bin:/root/.pyenv/shims:/root/.pyenv/plugins/pyenv-virtualenv/shims:$PATH
ENV PYENV_SHELL bash
ENV PYENV_VIRTUALENV_INIT 1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev
RUN pyenv install 3.9.0
RUN pyenv install 3.8.6
RUN pyenv global 3.9.0 3.8.6
RUN python --version
RUN python3.8 --version

#
# Setting up a project with Poetry
#

FROM pyenv as poetry
RUN curl -fsSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH
RUN poetry init --no-interaction
COPY hypermodern-python/pyproject.toml.01.patch /tmp
RUN patch -p1 < /tmp/pyproject.toml.01.patch
COPY hypermodern-python/pyproject.toml.02.patch /tmp
RUN patch -p1 < /tmp/pyproject.toml.02.patch

#
# Creating a Python package
#

FROM poetry as package
RUN mkdir -p src/$PACKAGE
RUN touch src/$PACKAGE/__init__.py

#
# Managing environments with Poetry
#

FROM package as environments
RUN poetry install
RUN poetry run python -c "import $PACKAGE"

#
# Managing dependencies with Poetry
#

FROM environments as dependencies
RUN poetry add click
COPY hypermodern-python/src/hypermodern_python/__main__.py src/$PACKAGE/__main__.py
COPY hypermodern-python/pyproject.toml.03.patch /tmp
RUN patch -p1 < /tmp/pyproject.toml.03.patch
RUN poetry install
RUN poetry run $PROJECT
RUN poetry run $PROJECT --help
RUN poetry run $PROJECT --version
COPY hypermodern-python/src/hypermodern_python/__main__.py.01.patch /tmp
RUN patch -p1 < /tmp/__main__.py.01.patch
RUN poetry run python -m $PACKAGE

#
# Example: Consuming an API with httpx
#

FROM dependencies as httpx
RUN poetry add httpx
COPY hypermodern-python/src/hypermodern_python/__main__.py.02 src/$PACKAGE/__main__.py
RUN poetry run $PROJECT

#
# Uploading your package to PyPI
#

FROM httpx as pypi
RUN poetry build
RUN : poetry publish

#
# Installing applications with pipx
#

FROM pypi as pipx
RUN python3.9 -m pip install --user pipx
RUN python3.9 -m pipx ensurepath
ENV PATH /root/.local/bin:$PATH
RUN pipx install .
RUN $PROJECT --version

FROM pipx as chapter01

###############################################################################
#                                 Chapter 02                                  #
###############################################################################

#
# Unit testing with pytest
#

FROM chapter01 as pytest
RUN poetry add --dev pytest
RUN mkdir tests
RUN touch tests/__init__.py
COPY hypermodern-python/tests/test_main.py tests/test_main.py
COPY hypermodern-python/tests/test_main.py.01.patch /tmp/patch
RUN patch -p1 < /tmp/patch
RUN poetry run pytest

#
# Test automation with Nox
#

FROM pytest as nox
RUN pipx install nox
COPY hypermodern-python/noxfile.py noxfile.py
RUN nox
RUN nox --session=tests --python=3.9 --reuse-existing-virtualenvs
RUN nox -p 3.9 -rs tests

#
# Code coverage with Coverage.py
#

FROM nox as coverage
RUN poetry add --dev 'coverage[toml]'
COPY hypermodern-python/pyproject.toml.04.patch /tmp/patch
RUN patch < /tmp/patch
RUN poetry run coverage run -m pytest
RUN poetry run coverage report
COPY hypermodern-python/src/hypermodern_python/__main__.py.03.patch /tmp/patch
RUN patch -p1 < /tmp/patch
RUN poetry run coverage run -m pytest
RUN poetry run coverage report
COPY hypermodern-python/pyproject.toml.05.patch /tmp/patch
RUN patch -p1 < /tmp/patch
