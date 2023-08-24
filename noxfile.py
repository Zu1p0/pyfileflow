import nox

nox.options.sessions = "tests", "format", "lint"

python_sessions = ["3.11.4"]
locations = "src", "tests", "noxfile.py"


@nox.session(venv_backend="venv", python=python_sessions)
def tests(session: nox.Session) -> None:
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
    args = session.posargs or "src", "tests", "noxfile.py", "examples"
    session.run("poetry", "install", "--only=format", external=True)
    session.run("autoflake", *args)
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(venv_backend="venv")
def lint(session: nox.Session) -> None:
    args = session.posargs or "src", "tests", "noxfile.py"
    session.run("poetry", "install", "--only=lint", external=True)
    session.run("flake8", *args)
