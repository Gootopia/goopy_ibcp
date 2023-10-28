"""IB Flexquery3.

Interfaces for the IB Flex Query API.
Note: This uses Version3, which provides more error checking/info. V2 is not currently supported
See this page: https://www.ibkrguides.com/brokerportal/flex3.htm
"""


class IBFlexQuery3:
    """IB Flex Queries"""

    # Request Format: https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/SendRequest?t=TOKEN&q=QUERY&v=3
    # where:
    #   TOKEN is the IB Clientportal generated web-token
    #   QUERY is the IB Clientportal generated code for the desired FlexQuery
    # NOTE: A successful response will contain the GetStatement URL so we'll use that rather than hard-define
    # GetStatement Format: https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/GetStatement?t=TOKEN&q=REF_CODE&v=3
    # where:
    #   TOKEN is the IB Clientportal generated web-token
    #   REF_CODE is found in the reply from Request Format call

    QueryURL: str = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/SendRequest?"
    GetStatementURL: str = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/GetStatement?"

    class XMLFields:
        """XML fields returned via a FlexQuery Response
        === SUCCESSFUL ===
            <FlexStatementResponse timestamp="28 August, 2012 10:37 AM EDT">
            <Status>Success</Status>
            <ReferenceCode>1234567890</ReferenceCode>
            <url>https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement</url>
            </FlexStatementResponse>
        === FAILURE ===
            <FlexStatementResponse timestamp="28 August, 2012 10:37 AM EDT">
            <Status>Fail</Status>
            <ErrorCode>1012</ErrorCode>
            <ErrorMessage>Token has expired.</ErrorMessage>
            </FlexStatementResponse>
        See https://www.ibkrguides.com/brokerportal/flex3error.htm for error codes
        """

        FlexStatementResponse: str = "FlexStatementResponse"
        ReferenceCode: str = "ReferenceCode"
        Url: str = "Url"

        Status: str = "Status"

        class Result_Status:
            """Possible returns in the Status field"""

            Success: str = "Success"
            Fail: str = "Fail"

        ErrorCode: str = "ErrorCode"
        ErrorMessage: str = "ErrorMsg"

        # This might show up (if we give an invalid version in the URL, for example)
        NonVersion3Error: str = "code"
