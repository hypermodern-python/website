import nox

@nox.session(python=["3.9", "3.8"])
def tests(session):
    session.install("pytest", ".")
    session.run("pytest")