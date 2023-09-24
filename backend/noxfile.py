import nox


@nox.session
def format(session: nox.Session) -> None:
    session.install("ufmt", "black", "isort")
    session.run("ufmt", "format", "users/src")
    session.run("black", "--config=configs/.black.toml", "users/src")
    session.run("isort", "--sp=configs/.isort.cfg", "users/src")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff", "flake8", "mypy")
    session.run(
        "ruff",
        "check",
        "--config=configs/.ruff.toml",
        "--fix",
        "users/src",
    )
    session.run("flake8", "--config=configs/.flake8", "users/src")
    # session.run("mypy", "--config-file=configs/.mypy.ini", "src")