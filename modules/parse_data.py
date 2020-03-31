import bs4 as bs
import urllib.request

car_specs_url = "https://www.auto-data.net"
sauce = urllib.request.urlopen("https://www.auto-data.net/en/results?search=bmw%20i8").read()
soup = bs.BeautifulSoup(sauce, 'lxml')

print(soup.find('div', class_ = ['down', 'down2']).attrs)
# for url in soup.find('div', class_ = 'down'):
#     print('href' in url)
#     print(url['href'])
