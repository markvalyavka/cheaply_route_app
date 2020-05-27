"""
Module to retrieve route data
"""


import urllib.request
import urllib.parse
import json


map_key = "***"
DISTANCE_MATRIX_BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?"
GEOCODING_BASE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"


class AddressIncorrectFormError(Exception):
    pass


def get_coordinates_from_place_name(place):
    """ (str) -> (tuple)

    Return coordinates (lat, lng) of a specific place
    from place's name
    """
    params = {'input': place,
              'inputtype': 'textquery',
              'fields': 'geometry',
              'key': map_key}
    params_str = urllib.parse.urlencode(params)
    request_url = GEOCODING_BASE_URL + params_str
    with urllib.request.urlopen(request_url) as response:
        data = response.read()
        data = json.loads(data.decode("utf-8"))
    try:
        lat = data['candidates'][0]['geometry']['location']['lat']
        lng = data['candidates'][0]['geometry']['location']['lng']
    except IndexError:
        raise AddressIncorrectFormError("You have either input a wrong address or it can not be interpreted")
    return lat, lng


def get_route_data_from_url(origin, destination, mode):
    """ (str, str, str) -> (dict)

    Get route data from distance matrix API
    """
    params = {'origins': origin,
              'destinations': destination,
              'mode': mode,
              'language': 'uk',
              'key': map_key}
    params_str = urllib.parse.urlencode(params)
    request_url = DISTANCE_MATRIX_BASE_URL + params_str
    with urllib.request.urlopen(request_url) as response:
        data = response.read()
        data = json.loads(data.decode("utf-8"))
    return data


def get_route_distance_and_duration(origin, destination, mode):
    """ (str, str, str) -> (tuple)

    Get route distance and duration from a json response
    """
    data = get_route_data_from_url(origin, destination, mode)
    try:
        distance = data['rows'][0]['elements'][0]['distance']
        duration = data['rows'][0]['elements'][0]['duration']
    except KeyError:
        raise AddressIncorrectFormError("You have either input a wrong address or it can not be interpreted")
    route_data = {'distance': (distance['text'], distance['value']),
                  'duration': (duration['text'], duration['value'])}

    return route_data


def get_walking_data(origin, destination):
    """

    """
    route_data = get_route_distance_and_duration(origin, destination, "walking")
    route_data['price'] = 0
    return {'walking': route_data}


def get_cycling_data(origin, destination):
    """

    """
    flag = "no data available"
    try:
        route_data = get_route_distance_and_duration(origin, destination, "bicycling")
        route_data['price'] = 0
        return {'cycling' : route_data}
    except:
        route_data = get_route_distance_and_duration(origin, destination, "")
        return {'cycling' : {'distance': (flag, flag), 'duration': (flag, flag), 'price': flag}}


def get_transit_data(origin, destination):
    """

    """
    route_data_plain = get_route_data_from_url(origin, destination, "transit")
    route_data = get_route_distance_and_duration(origin, destination, "transit")
    if 'fare' in route_data_plain['rows'][0]['elements'][0]:
        fare = route_data_plain['rows'][0]['elements'][0]['fare']['value']
        route_data['price'] = fare
    else:
        route_data['price'] = None
    return {'transit': route_data}


def calculate_fastest_cheapest(data):
    """

    """
    icons_dict = {'uklon': 'images/icons/uklon.svg',
                  'bolt': 'images/icons/bolt.svg',
                  'driving': 'images/icons/driving.svg',
                  'cycling': 'images/icons/cycling.svg',
                  'walking': 'images/icons/walking.svg',
                  'transit': 'images/icons/transit.svg'}

    result = {'fastest': {},
              'cheapest': {}}
    modes_chosen = []
    for mode in data:
        if mode == 'taxi':
            modes_chosen.append(('uklon', data[mode]['uklon']['Standard'], data['taxi']['duration'][1]))
            modes_chosen.append(('bolt', data[mode]['bolt']['Bolt'], data['taxi']['duration'][1]))
        else:
            modes_chosen.append((mode, data[mode]['price'], data[mode]['duration'][1]))
    print(modes_chosen)
    modes_chosen = list(filter(lambda x: isinstance(x[1], int), modes_chosen))
    if not modes_chosen:
        flag = "no data available"
        result = {'fastest' : {'name' : flag, 'icon_url' : 'images/icons/blank_error.svg', 'duration' : flag,
                      'price' : flag},
                 'cheapest' : {'name' : flag, 'icon_url' : 'images/icons/blank_error.svg', 'duration' : flag,
                               'price' : flag}}
        return result
    fastest = sorted(modes_chosen, key=lambda x: x[2])[0]
    cheapest = sorted(modes_chosen, key=lambda x: x[1])[0]
    print(fastest, cheapest)
    print(fastest[0], fastest[0] in data)
    result['fastest']['name'] = fastest[0]
    result['cheapest']['name'] = cheapest[0]
    result['fastest']['icon_url'] = icons_dict[fastest[0]]
    result['cheapest']['icon_url'] = icons_dict[cheapest[0]]

    if fastest[0] in data:
        result['fastest']['duration'] = data[fastest[0]]['duration'][0]
        result['fastest']['price'] = data[fastest[0]]['price']
    else:
        result['fastest']['duration'] = data['taxi']['duration'][0]
        if fastest[0] == "uklon" :
            result['fastest']['price'] = data['taxi'][fastest[0]]['Standard']
        elif fastest[0] == "bolt" :
            result['fastest']['price'] = data['taxi'][fastest[0]]['Bolt']

    if cheapest[0] in data:
        result['cheapest']['duration'] = data[cheapest[0]]['duration'][0]
        result['cheapest']['price'] = data[cheapest[0]]['price']
    else:
        result['cheapest']['duration'] = data['taxi']['duration'][0]
        if cheapest[0] == "uklon" :
            print( data['taxi'][cheapest[0]])
            result['cheapest']['price'] = data['taxi'][cheapest[0]]['Standard']
        elif cheapest[0] == "bolt" :
            result['cheapest']['price'] = data['taxi'][cheapest[0]]['Bolt']

    return result


if __name__ == "__main__":
    print('Testing retrieve_route_data ...')
