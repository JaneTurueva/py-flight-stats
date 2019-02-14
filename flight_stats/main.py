import argparse
import json
import os
from typing import Dict, Any

import dateutil.parser as date_parser
import requests
from terminaltables import AsciiTable


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')


parser = argparse.ArgumentParser()
parser.add_argument('--app-id', type=str, required=True)
parser.add_argument('--app-key', type=str, required=True)

subparsers = parser.add_subparsers()
subparsers.required = True
subparsers.dest = 'command'

subparser = subparsers.add_parser('get-airports')

arrivals_parser = subparsers.add_parser('get-arrivals')
arrivals_parser.add_argument('--airport', type=str, required=True)

departures_parser = subparsers.add_parser('get-departures')
departures_parser.add_argument('--airport', type=str, required=True)

flight_parser = subparsers.add_parser('get-flight')
flight_parser.add_argument('--flight-id', type=int, required=True)


def get_airports(query_params: Dict[str, Any]):
    """Display airports list"""
    # response = requests.get(
    #     'https://api.flightstats.com/flex/airports/rest/v1/json/active',
    #     params=query_params
    # )
    # data = response.json()

    with open(os.path.join(EXAMPLES_DIR, 'airports.json')) as f:
        data = json.loads(f.read())

    if 'error' in data:
        print('Error: ' + data['error']['errorMessage'])
        exit(1)

    data['airports'] = sorted(data['airports'], key=lambda k: k['fs'])
    result = [['Code', 'Airport name']]
    for airport in data['airports']:
        result.append([airport['fs'], airport['name']])

    table = AsciiTable(result)
    print(table.table)


def get_arrivals(airport: str, query_params: Dict[str, Any]):
    """Display current arrivals for specified airport"""
    # response = requests.get(
    #     (
    #         'https://api.flightstats.com/flex/flightstatus/rest/v2/json'
    #         f'/airport/status/{airport}/arr/2019/02/14/01'
    #     ),
    #     params=query_params
    # )
    # data = response.json()

    with open(os.path.join(EXAMPLES_DIR, 'flights.json')) as f:
        data = json.loads(f.read())

    if 'error' in data:
        print('Error: ' + data['error']['errorMessage'])
        exit(1)

    result = [['ID', 'Departure', 'Arrival', 'Date']]
    for flight in data['flightStatuses']:
        date = date_parser.parse(flight['arrivalDate']['dateLocal'])
        result.append([
            flight['flightId'],
            flight['departureAirportFsCode'],
            flight['arrivalAirportFsCode'],
            date.strftime('%H:%M %d.%m')
        ])

    table = AsciiTable(result)
    print(table.table)


def get_departures(airport: str, query_params: Dict[str, Any]):
    """Display current departures for specified airport"""

    # response = requests.get(
    #     (
    #         'https://api.flightstats.com/flex/flightstatus/rest/v2/json'
    #         f'/airport/status/{airport}/dep/2019/02/14/01'
    #     ),
    #     params=query_params
    # )
    # data = response.json()
    with open(os.path.join(EXAMPLES_DIR, 'flights.json')) as f:
        data = json.loads(f.read())

    if 'error' in data:
        print('Error: ' + data['error']['errorMessage'])
        exit(1)

    result = [['ID', 'Departure', 'Arrival', 'Date']]
    for flight in data['flightStatuses']:
        date = date_parser.parse(flight['departureDate']['dateLocal'])
        result.append([
            flight['flightId'],
            flight['departureAirportFsCode'],
            flight['arrivalAirportFsCode'],
            date.strftime('%H:%M %d.%m')
        ])

    table = AsciiTable(result)
    print(table.table)


def get_flight(flight_id: int, query_params: Dict[str, Any]):
    """Get flight by flight id"""
    # response = requests.get(
    #     (
    #         'https://api.flightstats.com/flex'
    #         f'/flightstatus/rest/v2/json/flight/status/{flight_id}'
    #     ),
    #     params=query_params
    # )
    # data = response.json()

    with open(os.path.join(EXAMPLES_DIR, 'flight.json')) as f:
        data = json.loads(f.read())

    departure_date = date_parser.parse(
        data['flightStatus']['departureDate']['dateLocal']
    )
    arrival_date = date_parser.parse(
        data['flightStatus']['arrivalDate']['dateLocal']
    )
    result = [
        ['ID', data['flightStatus']['flightId']],
        ['Number', data['flightStatus']['flightNumber']],
        ['Airlines', data['appendix']['airlines'][0]['name']],
        ['Departure airport', data['flightStatus']['departureAirportFsCode']],
        ['Departure date', departure_date.strftime('%H:%M %d.%m')],
        ['Arrival airport', data['flightStatus']['arrivalAirportFsCode']],
        ['Arrival date', arrival_date.strftime('%H:%M %d.%m')],
    ]
    table = AsciiTable(result)
    table.inner_heading_row_border = False
    print(table.table)


def main():
    args = parser.parse_args()

    query_params = {
        'app-id': args.app_id,
        'app-key': args.app_key
    }

    if args.command == 'get-airports':
        get_airports(query_params)

    elif args.command == 'get-arrivals':
        get_arrivals(args.airport, query_params)

    elif args.command == 'get-departures':
        get_departures(args.airport, query_params)

    elif args.command == 'get-flight':
        get_flight(args.flight_id, query_params)
