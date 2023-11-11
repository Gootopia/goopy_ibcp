"""ClientPortal CLI: Launch
Starts an event loop for HTTP or Websocket interface to IB ClientPortal
"""

from rich import print


class CliCommandLaunch:
    helpstr: str = (
        "Start infinite loop CLI interface for processing IB commands (WS or HTTP)"
    )


if __name__ == "__main__":
    print(f"=== IB ClientPortal (Launch)")
