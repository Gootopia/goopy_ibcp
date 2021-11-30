"""
Simple test script to verify setup is running with IB
"""
from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase
import time

# http for standard requests (placing orders, etc.)
client_http = ClientPortalHttp(min_ping_interval_sec=30)
<<<<<<< HEAD
print(client_http.clientrequest_brokerage_accounts())
print(client_http.clientrequest_reauthenticate())
print(client_http.clientrequest_validate())
print(client_http.clientrequest_authentication_status())

# websocket for quote data
client_ws = ClientPortalWebsocketsBase()
=======
r = client_http.clientrequest_authentication_status()

# websocket for quote data
client_ws = ClientPortalWebsocketsBase()

r = client_http.clientrequest_authentication_status()
>>>>>>> 380e7182b772436a6acd63208a563906608be9dc

# loop forever in the client. Normally you do this in a worker thread as it runs perpetually to process messages
client_ws.loop()
