"""
Simple test script to verify setup is running with IB
"""
from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase
import time

# http for standard requests (placing orders, etc.)
client_http = ClientPortalHttp(min_ping_interval_sec=5)

time.sleep(5000)

print("DONE!")
#r = client_http.clientrequest_authentication_status()

# websocket for quote data
# client_ws = ClientPortalWebsocketsBase()

#r = client_http.clientrequest_authentication_status()
# r = client_ws.loop()
