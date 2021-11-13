"""
Simple test script to verify setup is running with IB
"""
from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase

# http for standard requests (placing orders, etc.)
client_http = ClientPortalHttp()
# websocket for quote data
client_ws = ClientPortalWebsocketsBase()

r = client_http.clientrequest_authentication_status()
r = client_ws.loop()
