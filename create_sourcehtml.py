import requests
from bs4 import BeautifulSoup

with open("test.html") as source:
    soup = BeautifulSoup(source, "lxml")

print(soup.prettify())
p = soup.find_all('p', class_="shiggy")
print(type(p[0].text))

index = 500

for elem in p:
    if elem.text == "":
        index = p.index(elem)

print(index)
print(p[0])
a = ["a", "b"]
a.append(p[0].text)
print(len(a))
print(a)