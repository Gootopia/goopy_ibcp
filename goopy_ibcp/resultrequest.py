from dataclasses import dataclass

from goopy_ibcp.error import Error


@dataclass
class RequestResult:
    # request origin
    url: str = ""
    # Decoded message for error
    error = Error.No_Error
    # Client portal Web Error Code
    statusCode = 0
    # Client Portal JSON response string
    json: str = None
    # Raw string (From other formats like XML, etc.)
    raw: str = None
    # Converted Dict
    dict: [] = None
