import requests
from bs4 import BeautifulSoup

file = open("source.html", 'a')

source = requests.get("https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-id=549499&q-destination=London,%20England,%20United%20Kingdom&q-check-in=2020-03-08&q-check-out=2020-03-09&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&sort-order=BEST_SELLER")
source = source.text

print(type(source))
file.write(source)
soup = BeautifulSoup(source, 'lxml')
print(soup.prettify())
print(type(soup.prettify()))
file.close()