from bs4 import BeautifulSoup
import requests

next_page = requests.get("https://in.hotels.com/ho467613/?pa=1&q-check-out=2020-03-09&tab=description&q-room-0-adults=1&YGF=-1&q-check-in=2020-03-08&MGT=1&WOE=1&WOD=7&ZSX=0&SYE=2&q-room-0-children=0")

file = open("next.html", 'a')
next_page = next_page.text

print(type(next_page))
file.write(next_page)
soup = BeautifulSoup(next_page, 'lxml')
print(soup.prettify())
print(type(soup.prettify()))
file.close()

