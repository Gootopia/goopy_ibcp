import asyncio

from loguru import logger

from goopy_ibcp.clientportal_http_aio import ClientPortalHttpAio
from goopy_ibcp.ibparser import IBParser
from goopy_ibcp.error import Error
from goopy_ibcp.environment_var import Environment_Var


@logger.catch
async def main_http():
    logger.add("testlog.log")
    client_http = ClientPortalHttpAio(watchdog_start=False)

    # These are flex queries...need to have a token working for them to function properly!
    # r = await client_http.clientrequest_flexquery_request(queryid="873489")
    # r = await client_http.clientrequest_flexquery_request(queryid="873480")
    r = await client_http.clientrequest_user()

    if r.error is Error.No_Error:
        accounts, err = IBParser.get_accounts(r.json)

        r = await client_http.clientrequest_authentication_status()
        r = await client_http.clientrequest_server_accounts()
        r = await client_http.clientrequest_portfolio_accounts()
        r = await client_http.clientrequest_switch_account(
            Environment_Var.IB_ACTIVE_ACCOUNT
        )
        r = await client_http.clientrequest_trades()
        trades, err = IBParser.get_trades(r.json)

        r = await client_http.clientrequest_validate()
        await asyncio.sleep(5)

        while True:
            await client_http.clientrequest_marketdata("495512572", "31")
            await client_http.clientrequest_validate()
            await asyncio.sleep(5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_http())
