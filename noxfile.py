import nox

nox.options.sessions = "tests", "format", "lint"

python_sessions = ["3.11.4", "3.10.11", "3.9.13"]
locations = "src", "tests", "noxfile.py", "examples"


@nox.session(venv_backend="venv", python=python_sessions)
def tests(session: nox.Session) -> None:
    session.run("poetry", "install", "--with=dev", external=True)
    session.run("pytest", "-v", "--cov")


@nox.session(venv_backend="venv", python=python_sessions[0])
def format(session: nox.Session) -> None:
    args = session.posargs or locations
    session.run("poetry", "install", "--only=format", external=True)
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(venv_backend="venv", python=python_sessions[0])
def lint(session: nox.Session) -> None:
    args = session.posargs or locations
    session.run("poetry", "install", "--only=lint", external=True)
    session.run("flake8", *args)
    session.run("mypy", *args)
