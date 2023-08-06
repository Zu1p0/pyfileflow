import nox


@nox.session(venv_backend="venv", python=["3.11.4", "3.10.11", "3.9.13", "3.8.10"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")
