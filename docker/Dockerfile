FROM ubuntu:20.10
ARG DEBIAN_FRONTEND=noninteractive

# pyenv

RUN apt update && apt install -y curl git
RUN curl https://pyenv.run | bash
ENV PATH /root/.pyenv/bin:/root/.pyenv/shims:/root/.pyenv/plugins/pyenv-virtualenv/shims:$PATH
ENV PYENV_SHELL bash
ENV PYENV_VIRTUALENV_INIT 1
RUN apt update && apt install -y --no-install-recommends \
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

# poetry

RUN curl -fsSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

# pipx

RUN pip install --user pipx
RUN python -m pipx ensurepath
ENV PATH /root/.local/bin:$PATH

# project

ENV PROJECT hypermodern-python
ENV PACKAGE hypermodern_python
WORKDIR /root/$PROJECT
RUN echo "# $PROJECT" > README.md
RUN touch LICENSE
RUN mkdir -p src/$PACKAGE
RUN touch src/$PACKAGE/__init__.py
COPY pyproject.v2.toml pyproject.toml
COPY __main__.v2.py src/$PACKAGE/__main__.py
RUN poetry install
RUN pipx install .
# Chapter 02
RUN poetry add --dev pytest
RUN mkdir tests
RUN touch tests/__init__.py
COPY test_main.py tests/
RUN poetry run pytest
RUN poetry add --dev 'coverage[toml]'
COPY pyproject.v3.toml pyproject.toml
RUN poetry run coverage run -m pytest
RUN poetry run coverage report
RUN sed -i '/^if/s/$/  # pragma: no cover/' src/$PACKAGE/__main__.py
