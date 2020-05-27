"""
Module to retrieve Uklon and Bolt taxi data
"""

import retrieve_route_data as route_data
import requests
import json


def get_bolt_data(destination_coords, origin_coords):
    """ (tuple) -> response

    Get data about a trip using Bolt taxi
    """
    prices = {}
    url = "***"
    payload = {'campaign_code': "",
               'destination_stops': [
                   {'lat': destination_coords[0], 'lng': destination_coords[-1]}],
               'payment_method_id': 'cash',
               'payment_method_type': 'default',
               'pickup_stop': {
                   'address': 'Ukraine WOW',
                   'lat': origin_coords[0],
                   'lng': origin_coords[-1]},
               'preliminary': False,
               "timezone": "Europe/Kiev"
               }
    payload = json.dumps(payload)
    headers = {
        'authority': 'search.taxify.eu',
        'authorization': '***',
        'Content-Type': 'application/json'
    }

    with requests.request("POST", url, headers=headers, data=payload) as response:
        data = response.json()
        #print('bolt',data)
    for route_mode in data['data']['search_categories']:
        prices[route_mode['name']] = int(route_mode['price']['actual'][:-1])
    return prices


def get_uklon_data(origin_coords, destination_coords):
    """ (tuple) -> response

    Get data about a trip using Uklon taxi
    """
    prices = {}
    url = "https://rider.uklon.com.ua/api/v1/fare-estimate"
    payload = {
        'fare_id': '***',
        'pickup_time': None,
        'ride_conditions': [],
        'route': {
            'entrance': 0,
            'points': [{'lat': origin_coords[0], 'lng': origin_coords[-1], 'name': 'Stryiska street, 48B'},
                       {'lat': destination_coords[0], 'lng': destination_coords[-1], 'name': 'Yevropeiska square, 1'}]
        }
    }
    payload = json.dumps(payload)
    headers = {
        'User-Agent': '***',
        'X-FP': 'E164',
        'app_uid': '***',
        'client_id': '***',
        'locale': 'en',
        'city': 'kiev',
        'Authorization': '***',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept-Encoding': 'gzip',
        'Cookie': '***'
    }
    with requests.request("POST", url, headers=headers, data=payload) as response:
        data = response.json()
    for route_mode in data['product_fares']:
        prices[route_mode['product_type']] = int(route_mode['low'])
    return prices


def get_taxi_prices(origin, destination):
    """
    Get Bolt's and Uklon's prices of a trip
    """
    origin_coords = route_data.get_coordinates_from_place_name(origin)
    destination_coords = route_data.get_coordinates_from_place_name(destination)

    uklon_prices = get_uklon_data(origin_coords, destination_coords)
    bolt_prices = get_bolt_data(origin_coords, destination_coords)
    duration = route_data.get_route_distance_and_duration(origin, destination, "driving")['duration']

    return {'taxi': {'uklon': uklon_prices, 'bolt': bolt_prices, 'duration': duration}}


if __name__ == '__main__':
    print('Testing...')
    print(get_taxi_prices("Львів", "Київ"))
