from goopy_ibcp.clientportal_http import ClientPortalHttp
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase

client_http = ClientPortalHttp()
client_ws = ClientPortalWebsocketsBase()

r = client_http.clientrequest_authentication_status()
r = client_ws.loop()
