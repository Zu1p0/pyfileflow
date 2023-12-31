"""Nox sessions."""

import nox

nox.options.sessions = "tests", "format", "lint"

python_sessions = ["3.11.4"]
locations = "src", "tests", "noxfile.py", "docs/conf.py", "examples"


@nox.session(venv_backend="venv", python=python_sessions)
def tests(session: nox.Session) -> None:
    """Test sessions.

    Launch pytest with coverage and typeguard.

    Args:
        session: Nox session
    """
    session.run("poetry", "install", "--with=tests,typeguard,coverage", external=True)
    session.run(
        "pytest",
        "-v",
        "--typeguard-packages=pyfileflow",
        "--cov",
        "--no-cov-on-fail",
    )


@nox.session(venv_backend="venv")
def format(session: nox.Session) -> None:
    """Format session.

    Launch autoflake, isort and black.

    Args:
        session: Nox session
    """
    args = session.posargs or locations
    session.run("poetry", "install", "--only=format", external=True)
    session.run("autoflake", *args)
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(venv_backend="venv")
def lint(session: nox.Session) -> None:
    """Lint session.

    Launch flake8 with multiple extensions.

    Args:
        session: Nox session

    """
    args = session.posargs or locations
    session.run("poetry", "install", "--only=lint", external=True)
    session.run("flake8", *args)


@nox.session(venv_backend="venv")
def coverage(session: nox.Session) -> None:
    """Upload coverage data.

    Launch coverage and codecov

    Args:
        session: Nox session
    """
    session.run("poetry", "install", "--with=coverage,codecov", external=True)
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(venv_backend="venv")
def docs(session: nox.Session) -> None:
    """Build the documentation.

    Launch Sphinx

    Args:
        session: Nox session
    """
    session.run("poetry", "install", "--with=docs", external=True)
    session.run("sphinx-build", "docs", "docs/_build")
