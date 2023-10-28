"""ClientPortal Command Line Interface"""

import typer
from rich import print

# Kick off typer
app = typer.Typer()


@app.command()
def version():
    print(f"Version")


@app.command()
def start():
    print(f"Starting!")


if __name__ == "__main__":
    app()
