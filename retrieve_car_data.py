"""Car info retrieval module"""
import bs4
import requests, json
from bs4 import BeautifulSoup
from retrieve_route_data import get_route_distance_and_duration
import urllib.request, urllib.error, urllib.parse
import station_list


def transform_to_fueltype(fuel):
    """

    """
    fueltype_dict = {'gasoline': 'a95f',
                     'Бензин': 'a95f',
                     'diesel': 'dtf',
                     'Дизель': 'dtf'}
    return fueltype_dict[fuel]

def get_fuel_cost(fuel: str):
    """Gets actual fuel cost and returns
    a sorted list ( from the most expensive to the least )
    of existing fuel stations and their cost
    for specific type of fuel.
    Disclaimer: cost is average by country"""
    fueltype = transform_to_fueltype(fuel)
    payload = {}
    output_data = {}
    for azs in station_list.fuelStations:
        url = f"https://auto.ria.com/content/news/templetify/fuel_price_page/?langId=4&refuel={azs['id']}&size={1}"
        headers = {
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Referer': f"https://auto.ria.com/uk/toplivo/{azs['eng']}",
            'TE': 'Trailers'}
        response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
        cost = response['buckets'][0][fueltype]['avg']
        if cost:
            output_data[azs['name']] = float(cost)

    return output_data


def get_car_url(car_id: int):
    """

    """
    url = f'http://autoportal.ua/catalogue/newcars/compare_{car_id}_56663.html'
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    cars_data = soup.findAll("td", {"class" : "textcenter"})
    for car_data in cars_data :
        link = car_data.find('a')
        if link and not ("tesla" in link["href"]) :
            car_url = link["href"]
            return car_url


def get_car_info(car_id: int):
    """Retrieves: fuel capacity,
    type of fuel. Returns None if
    selected electric car"""

    car_info = {"fuel": "", "expenditure": ""}
    url = get_car_url(car_id)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    spans = soup.findAll("span")
    for span in spans:
        if span.text == "Топливо":
            fuel = span.next_sibling.next_sibling.text
            car_info["fuel"] = fuel
        if span.text == "Расход по городу, л":
            litrage = span.next_sibling.next_sibling.text.replace(",", ".")
            fuel_expenditure = float(litrage)
            car_info["expenditure"] = fuel_expenditure

    return car_info


def get_car_data(origin, destination, car_id):
    """

    """
    route_data = get_route_distance_and_duration(origin, destination, "driving")
    car_info = get_car_info(car_id)
    if car_info['fuel'] and car_info['expenditure']:
        if car_info['fuel'] == "Электричество":
            route_data['price'] = "Electricity"
            route_data['station_price'] = "Electricity"
            return {'driving' : route_data}
        fuel_prices = get_fuel_cost(car_info['fuel'])
        price = (((route_data['distance'][1] / 1000) * car_info['expenditure']) / 100) * fuel_prices['ОККО']
        route_data['price'] = round(price,1)
        route_data['station_price'] = fuel_prices['ОККО']
        return {'driving': route_data}
    else:
        route_data['price'] = "no data available"
        route_data['station_price'] = "no data available"
        return {'driving': route_data}


if __name__ == '__main__':
    # Todo: need to fix when electric car selected eg. Tesla
    print(get_car_data("Львів","Київ",715))
    print('Done!')
