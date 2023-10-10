"""IB Models.

Endpoint structure names for the clientportal JSON structures.
See this page: https://interactivebrokers.github.io/cpwebapi/endpoints
"""


class IBModels:
    """IB Model JSON field identifiers"""

    class ClientRequest_User:
        """Structure returned via clientrequest_user()"""

        Accounts: str = "accts"
