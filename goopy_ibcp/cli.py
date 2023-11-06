"""ClientPortal Command Line Interface"""

import typer

# https://rich.readthedocs.io/en/stable/markup.html
from rich import print

# from goopy_ibcp.cli_commands.cli_launch import

app = typer.Typer(help="[red]IB ClientPortal Command Line Interface (CLI)")


@app.command()
def version():
    """Display CLI Version"""
    print(f"[red]IB Client Portal Version 1.0.0")


@app.command()
def launch(
    ib_interface: str = typer.Argument("Websocket", help="interface help"),
):
    """Launch Websocket or HTTP ClientPortal interface (does not return)"""
    print(f"Launching {ib_interface}")


if __name__ == "__main__":
    app()
