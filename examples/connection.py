"""
Simple example test script for connecting and subscribing to data
"""
from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase
import time

"""
Interfacing with the IB Client Portal:
- If running IBeam, the watchdog is not required since IBeam will take care of pinging/re-authentication for you
"""
client_http = ClientPortalHttp(watchdog_start=False)
client_http.clientrequest_brokerage_accounts()
time.sleep(1)
client_http.clientrequest_reauthenticate()
time.sleep(1)
#client_http.clientrequest_validate()
#client_http.clientrequest_authentication_status()

# Example call to search by name or symbol
secdef=client_http.clientrequest_search("ES")
#print(secdef.json[0])

conid="461318816"
# Get a tick snapshot of instruments (HTTP-based)
client_http.clientrequest_marketdata(conid)

# Get historical data (HTTP-based)
client_http.clientrequest_marketdata(conid)
time.sleep(1)
client_http.clientrequest_marketdata(conid)
time.sleep(1)
client_http.clientrequest_marketdata(conid)
time.sleep(1)
client_http.clientrequest_marketdata(conid)
time.sleep(1)

# Streaming data subscription (Websocket-based)
client_ws = ClientPortalWebsocketsBase()

try:
# loop forever in the client. Normally you do this in a worker thread as it runs perpetually to process messages
    client_ws.loop()
    print("Bye-Bye!")

except Exception as e:
    print(f"Exception: {e}")

finally:
    print("====ALL DONE====")

print("We be done!")
