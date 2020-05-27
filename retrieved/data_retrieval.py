"""Data retrieval module"""
import bolt
import uklon
import time
import json
from datetime import date
import os.path


def retrieve(dest, addr):
    while True:
        bolt_data = bolt.get_data(dest, addr)
        uklon_data = uklon.get_data(dest, addr)
        save_data(bolt_data, uklon_data)
        time.sleep(3600)


def save_data(bolt_data, uklon_data):
    bolt_json = json.loads(bolt_data.text)
    uklon_json = json.loads(uklon_data.text)

    data = (bolt_json, uklon_json)
    files = get_filenames()
    for i, each in enumerate(files):
        with open(each, 'w') as file:
            json.dump(data[i], file)
    print('Created: ', files)

    # print(bolt_json)
    # print(uklon_json)
    print('-' * 100)


def get_filenames():
    hour = time.strftime('%H')
    c_date = date.today().strftime('%d_%m')
    day = date.today().strftime("%A")

    bolt_path = check_path(c_date, day, 'bolt')
    uklon_path = check_path(c_date, day, 'uklon')

    print('Update: ', hour, day, c_date)
    return f'{bolt_path}/{hour}_{c_date}_data.json', \
           f'{uklon_path}/{hour}_{c_date}_data.json'


def check_path(c_date, day, service):
    if not os.path.exists(f'{service}_data'):
        os.mkdir(f'{service}_data')
        print("Directory ", f'{service}_data', " Created ")
        output = check_path(c_date, day, service)
    else:
        if not os.path.exists(f'{service}_data/{day}'):
            os.mkdir(f'{service}_data/{day}')
            print("Directory ", f'{service}_data/{day}', " Created ")
            output = check_path(c_date, day, service)
        else:
            return f'{service}_data/{day}/'
    return output


if __name__ == '__main__':
    DESTINATION = ('49.866873', '24.014777')
    ADDRESS = ('49.818009', '24.022778')
    retrieve(DESTINATION, ADDRESS)
