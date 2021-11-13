from goopy_ibcp.error import Error

class RequestResult:
    # Decoded message for error
    error = Error.No_Error
    # Client portal Web Error Code
    statusCode = 0
    # Client Portal JSON string
    json: str = None
