import argparse

import aiohttp

API_BASE_URL = 'https://api.flightstats.com'

parser = argparse.ArgumentParser()
parser.add_argument('--app-id', type=str, required=True)
parser.add_argument('--app-key', type=str, required=True)

subparsers = parser.add_subparsers()
subparsers.required = True
subparsers.dest = 'command'

airports_parser = subparsers.add_parser('get-airports')

arrivals_parser = subparsers.add_parser('get-arrivals')
arrivals_parser.add_argument('--airport', type=str, required=True)

departures_parser = subparsers.add_parser('get-departures')
departures_parser.add_argument('--airport', type=str, required=True)

flight_parser = subparsers.add_parser('get-flight')
flight_parser.add_argument('--flight-id', type=str, required=True)


async def get_airports(app_id: str, app_key: str, ):
    url = ''.join([
        API_BASE_URL,
        '/flex/airports/rest/v1/json/active'
    ])

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={
            'app_id': app_id,
            'app_key': app_key
        }) as resp:
            return await resp.json()


async def get_arrivals(app_id: str, app_key: str, airport: str, year: str,
                       month: str, day: str, hour: str):
    url = ''.join([
        API_BASE_URL,
        f'/flex/flightstatus/rest/v2/json/airport/status/{airport}/dep/{year}/{month}/{day}/{hour}'
    ])

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={
            'app_id': app_id,
            'app_key': app_key
        }) as resp:
            return await resp.json()


async def get_departures(app_id: str, app_key: str, airport: str, year: str, month: str, day: str,
                         hour: str):
    url = ''.join([
        API_BASE_URL,
        f'/flex/flightstatus/rest/v2/json/airport/status/{airport}/arr/{year}/{month}/{day}/{hour}'
    ])

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={
            'app_id': app_id,
            'app_key': app_key
        }) as resp:
            return await resp.json()


async def get_flight(app_id: str, app_key: str, flight_id: str):
    url = ''.join([
        API_BASE_URL,
        '/flex/flightstatus/rest/v2/json/flight/status/',
        flight_id
    ])

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={
            'app_id': app_id,
            'app_key': app_key
        }) as resp:
            return await resp.json()


def main():
    args = parser.parse_args()
    print(args)
    print(args.command)
    print(args.app_id)
    print('Hello')