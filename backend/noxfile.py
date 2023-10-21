import nox

DIRECTORIES = ["users/src"]


@nox.session
def format_lint(session: nox.Session) -> None:
    session.install("-r" "configs/requirements.txt")
    session.run("black", "--config=configs/.black.toml", *DIRECTORIES)
    session.run("isort", "--sp=configs/.isort.cfg", *DIRECTORIES)
    session.run(
        "ruff",
        "check",
        "--config=configs/.ruff.toml",
        "--fix",
        *DIRECTORIES,
    )
    session.run("flake8", "--config=configs/.flake8", *DIRECTORIES)
    # session.run("mypy", "--config-file=configs/.mypy.ini", *DIRECTORIES)