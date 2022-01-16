import aiohttp
import asyncio

from goopy_ibcp.clientportal_http_aio import ClientPortalHttpAio

async def aio_get(url,params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, timeout=10.0, params=params) as response:
            retval = await response.text()
            return retval           

async def main():
    client_http = ClientPortalHttpAio(watchdog_start=False)
    await client_http.clientrequest_validate()
    await client_http.clientrequest_brokerage_accounts()
    await client_http.clientrequest_marketdata("461318816", "31")
    #val = await aio_get('https://localhost:5000/v1/api/sso/validate')
    #print(val)
    #val = await aio_get('https://localhost:5000/v1/api/portfolio/accounts')
    #print(val)
    #params = {"conids":"461318816", "fields":"31"}

    #while True:
    #    val = await aio_get('https://localhost:5000/v1/api/iserver/marketdata/snapshot', params=params)
    #    print(val)
    #    await asyncio.sleep(2)

if __name__ == '__main__':
     loop = asyncio.get_event_loop()
     loop.run_until_complete(main())
