"""IB Field Mappings.

Map IB fields to more human readable ones.
"""


class IBFieldMapper:
    """Conversion between IB fields and "human-readable" ones."""

    Topic: str = "topic"
    Time: str = "_updated"
    Conid: str = "conid"

    """
    Tick codes used by IB. Websockets must subscribe to each type when requesting the data.
    See https://interactivebrokers.github.io/cpwebapi/endpoints#operations-tag-Market_Data.
    """

    Price_Last: str = "31"
    Price_Bid: str = "84"
    Price_Ask: str = "86"
    Market_Data_Availability: str = "6509"

    @classmethod
    def map_from_ib(cls, ib_field_code: str = None):
        if ib_field_code is None:
            raise ValueError("field code cannot be 'NoneType'")
