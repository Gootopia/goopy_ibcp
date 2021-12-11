"""
Simple test script to verify setup is running with IB
"""
from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase
import time

import asyncio
import websockets

# http for standard requests (placing orders, etc.)
client_http = ClientPortalHttp(min_ping_interval_sec=30)
print(client_http.clientrequest_brokerage_accounts())
print(client_http.clientrequest_reauthenticate())
print(client_http.clientrequest_validate())
print(client_http.clientrequest_authentication_status())

# websocket for quote data
client_ws = ClientPortalWebsocketsBase()

# loop forever in the client. Normally you do this in a worker thread as it runs perpetually to process messages
client_ws.loop()

print("====ALL DONE====")
