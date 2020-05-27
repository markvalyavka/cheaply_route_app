import os
import json


class Day:
    def __init__(self, current_provider, day_name=None):
        self.data = {}
        self.day_name = day_name
        self.current_provider = current_provider
        self.providers = {"uklon": self.get_uklon_data,
                          "bolt": self.get_bolt_data}
        self.get_data()

    def get_data(self):
        if self.day_name:
            for hour in list(os.walk(f'retrieved/bolt_data/{self.day_name}'))[0][2]:
                self.providers[self.current_provider](
                    f'retrieved/{self.current_provider}_data/{self.day_name}/{hour}', hour)
        else:
            for days in list(os.walk('retrieved/bolt_data'))[0][1]:
                for hour in list(os.walk(f'retrieved/bolt_data/{days}'))[0][2]:
                    self.providers[self.current_provider](
                        f'retrieved/{self.current_provider}_data/{days}/{hour}', hour)
        self.get_average()

    def get_bolt_data(self, path, filename):
        with open(path) as json_data:
            data = json.load(json_data)
            self.data.setdefault(int(filename[:2]), [])
            self.data[int(filename[:2])].append(
                int(data['data']['search_categories'][0]['price']['actual'][:-1]))

    def get_uklon_data(self, path, filename):
        with open(path) as json_data:
            data = json.load(json_data)
            self.data.setdefault(int(filename[:2]), [])
            self.data[int(filename[:2])].append(
                data['product_fares'][0]['low'])

    def get_average(self):
        for k, v in self.data.items():
            self.data[k] = round(sum(v)/len(v))

    @property
    def average(self):
        return round(sum(self.data.values())/24)

    @property
    def output(self):
        return [v for k,v in self.data.items()]

class Week(Day):
    def __init__(self, current_provider):
        self.data = {}
        self.current_provider = current_provider
        self.get_data()

    def get_data(self):
        for days in list(os.walk(f'retrieved/{self.current_provider}_data'))[0][1]:
            day = Day(self.current_provider, days)
            self.data.setdefault(days, day.average)
        return self.data


if __name__ == "__main__":
    print('Testing...')
    d = Day('bolt', 'Saturday')
    d2 = Day('uklon')
    print(d.get_data())
    print(d2.get_data())
    print(d.data)
    print(d.average)
    print(d.average)
    w = Week('bolt').output
    print(w)
