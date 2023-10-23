"""IB Models.

Endpoint structure names for the clientportal JSON structures.
See this page: https://interactivebrokers.github.io/cpwebapi/endpoints
"""


class IBModels:
    """IB Model JSON field identifiers"""

    class User:
        """Response to /user/one (might be undocumented)"""

        Accounts: str = "accts"

    class Trade:
        """Response to /iserver/account/trades"""

        Trade_Execution: str = "execution_id"
