import pytest
from goopy_ibcp.ibfieldmapper import IBFieldMapper


class Test_IBFieldMapper:
    """Test class for mapping to/from IB fields."""

    def test_ibfieldvalues(self):
        """Sanity check to make sure we are using proper IB field codes."""
        assert IBFieldMapper.Conid == "conid"
        assert IBFieldMapper.Time == "_updated"
        assert IBFieldMapper.Topic == "topic"
        assert IBFieldMapper.Price_Last == "31"
        assert IBFieldMapper.Price_Ask == "86"
        assert IBFieldMapper.Price_Bid == "84"
        assert IBFieldMapper.Market_Data_Availability == "6509"
