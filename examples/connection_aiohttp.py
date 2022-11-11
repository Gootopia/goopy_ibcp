import asyncio
from loguru import logger

from goopy_ibcp.clientportal_http_aio import ClientPortalHttpAio
from goopy_ibcp.clientportal_websockets import ClientPortalWebsocketsBase


@logger.catch
async def main():
    logger.add("testlog.log")
    client_http = ClientPortalHttpAio(watchdog_start=False)
    r = await client_http.clientrequest_validate()
    r = await client_http.clientrequest_user()
    r = await client_http.clientrequest_portfolio_accounts()
    r = await client_http.clientrequest_authentication_status()
    await client_http.clientrequest_server_accounts()
    await asyncio.sleep(5)

    while True:
        await client_http.clientrequest_marketdata("495512551", "31")
        await asyncio.sleep(1)


@logger.catch
def main_ws():
    logger.add("testlog.log")
    client_ws = ClientPortalWebsocketsBase()
    client_ws.loop()


if __name__ == "__main__":
    # Use this for the websocket demo
    main_ws()

    # Use this for the http demo
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
