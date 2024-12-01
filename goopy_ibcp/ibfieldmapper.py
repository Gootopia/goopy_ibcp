"""IB Field Mappings.

Map IB fields to more human readable ones.
"""


class IBFieldMapper:
    """Conversion between IB fields and "human-readable" ones."""

    Topic: str = "topic"
    Time: str = "_updated"
    Conid: str = "conid"
    Websocket_SubscribeMarketData: str = "smd"

    """
    Tick codes used by IB. Websockets must subscribe to each type when requesting the data.
    See https://interactivebrokers.github.io/cpwebapi/endpoints#operations-tag-Market_Data.
    """

    Price_Last: str = "31"
    Price_High: str = "70"
    Price_Low: str = "71"
    Price_Bid: str = "84"
    Price_Ask: str = "86"
    Price_Open: str = "7295"
    Price_Close: str = "7296"

    Market_Data_Availability: str = "6509"
