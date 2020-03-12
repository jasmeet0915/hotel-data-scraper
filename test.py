from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup

with open("source.html") as source:
    soup = BeautifulSoup(source, "lxml")

def get_soup_by_class(soup, tag, class_):
    raw_list = []
    empty_index = None
    raw_soup = soup.find_all(tag, {'class': class_})

    for element in raw_soup:
        if element.text == "":
            empty_index = raw_soup.index(element)
        raw_list.append(element.text)

    return (raw_list, empty_index)


checkin = ["2020-04-11"]
checkout = ["2020-04-12"]

(names, _) = get_soup_by_class(soup, 'h3', "p-name")
(prices, index) = get_soup_by_class(soup, 'aside', "pricing resp-module")

(details, _) = get_soup_by_class(soup, 'div', "additional-details resp-module")
(reviews, _) = get_soup_by_class(soup, 'div', "details resp-module")

'''
for price in prices:
    if name == "Everything You Need. All Right Here. 10A":
        index = 0
        print("popped")
        index = names.index(name)
        names.pop(index)
        details.pop(index)
        reviews.pop(index)
        break
'''


headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

checkin_dates = [checkin] * len(names)
checkout_dates = [checkout] * len(names)

print(len(checkin_dates))
print(len(checkout_dates))
print(len(names))
print(len(prices))
print(len(details))
print(len(reviews))
print(index)

prices.append([""])
prices.append([""])
prices.append([""])

print(len(prices))
'''for i in range(len(prices)):
    print(names[i])
    print(prices[i])
    print("")
'''

hotel_dict = dict(zip(headers, [names, details, reviews, prices, checkin_dates, checkout_dates]))

hotel_df = pd.DataFrame(hotel_dict)

print(names[len(names)-1])
hotel_df.to_pickle("data.pkl", protocol=3)
print(hotel_df.shape)
print(hotel_df.head())
hotel_df.to_csv("data.csv")