
import urllib.request
import urllib.parse
import json

map_key = "**GOOGLE_API_KEY**"
BASE_URL = "https://maps.googleapis.com/maps/api/distancematrix/json?"
params = { 'origins': "Львів, Форум",
           'destinations': "Львів, УКУ",
           'mode': "walking",
           'language': 'uk',
           'key': map_key}

def get_data_from_URL(base_url, params):

    params_str = urllib.parse.urlencode(params)
    request_url = base_url + params_str
    request = urllib.request.Request(request_url)
    with urllib.request.urlopen(request_url) as response:
        data = response.read()
        data = json.loads(data.decode("utf-8"))
    return data

def get_distance_and_time_from_data(data):

    destination_address = data['destination_addresses'][0]
    origin_address = data['origin_addresses'][0]
    distance_time_data = data['rows'][0]['elements'][0]
    distance = distance_time_data['distance']['text']
    time = distance_time_data['duration']['text']

    print(f"Travel from {origin_address} to {destination_address}"
          f"takes {time} and is {distance} long")


data = get_data_from_URL(BASE_URL, params)
get_distance_and_time_from_data(data)