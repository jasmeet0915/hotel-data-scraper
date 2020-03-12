from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup

with open("source.html") as source:
    soup = BeautifulSoup(source, "lxml")

def get_soup_by_class(soup, tag, class_):
    raw_soup = soup.find_all(tag, {'class': class_})
    raw_list = [element.text for element in raw_soup]
    return raw_list


checkin = ["2020-04-11"]
checkout = ["2020-04-12"]
print(soup.prettify())
index = 0
names = get_soup_by_class(soup, 'h3', "p-name")
for name in names:
    if name == "Everything You Need. All Right Here. 10A":
        index = names.index(name)
        names.pop(index)
        break

prices = get_soup_by_class(soup, 'aside', "pricing resp-module")
details = get_soup_by_class(soup, 'div', "additional-details resp-module")
reviews = get_soup_by_class(soup, 'div', "details resp-module")
details.pop(index)
reviews.pop(index)


print(len(prices))
print(prices)

headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

checkin_dates = [checkin] * len(names)
checkout_dates = [checkout] * len(names)
print(len(checkin_dates))
print(len(checkout_dates))
print(len(names))
print(len(prices))
print(len(details))
print(len(reviews))

hotel_dict = dict(zip(headers, [names, details, reviews, prices, checkin_dates, checkout_dates]))

hotel_df = pd.DataFrame(hotel_dict)

hotel_df.to_pickle("data.pkl", protocol=3)
print(hotel_df.shape)
print(hotel_df.head())