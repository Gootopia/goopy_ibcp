import asyncio
from loguru import logger

from goopy_ibcp.clientportal_http_aio import ClientPortalHttpAio
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase


@logger.catch
async def main_http():
    logger.add("testlog.log")
    client_http = ClientPortalHttpAio(watchdog_start=False)
    # r = await client_http.clientrequest_validate()
    r = await client_http.clientrequest_user()
    r = await client_http.clientrequest_portfolio_accounts()
    r = await client_http.clientrequest_validate()
    r = await client_http.clientrequest_authentication_status()
    r = await client_http.clientrequest_server_accounts()
    await asyncio.sleep(5)

    while True:
        await client_http.clientrequest_marketdata("495512572", "31")
        await client_http.clientrequest_validate()
        await asyncio.sleep(5)


@logger.catch
def main_ws() -> None:
    logger.add("testlog.log")

    client_ws = ClientPortalWebsocketsBase()
    client_ws.loop()


if __name__ == "__main__":
    # event loop for the demos (websocket or http)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_ws())
    # loop.run_until_complete(main_http())
