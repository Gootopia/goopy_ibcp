import asyncio
from loguru import logger

from goopy_ibcp.clientportal_http_aio import ClientPortalHttpAio
        
@logger.catch
async def main():
    logger.add('testlog.log')
    client_http = ClientPortalHttpAio(watchdog_start=False)
    await client_http.clientrequest_validate()
    await client_http.clientrequest_user()
    await client_http.clientrequest_portfolio_accounts()
    await client_http.clientrequest_authentication_status()
    await client_http.clientrequest_server_accounts()
    await asyncio.sleep(5)
    
    while True:
        await client_http.clientrequest_marketdata("461318816", "31")
        await asyncio.sleep(1)

if __name__ == '__main__':
     loop = asyncio.get_event_loop()
     loop.run_until_complete(main())
