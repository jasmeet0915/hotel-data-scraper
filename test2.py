from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd

headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")

url = "https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-id=549499&q-destination=London,%20England,%20United%20Kingdom&q-check-in=2020-04-11&q-check-out=2020-04-12&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id=540099"

driver = webdriver.Chrome("chromedriver_linux64/chromedriver", chrome_options=options)

# chrome window and maximize it
driver.get(url)
driver.maximize_window()

has_loaded_count = 0
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

while True:
    loading = driver.find_element_by_id("listings-loading")
    driver.execute_script("arguments[0].scrollIntoView();", loading)
    print("---------scrolled into view--------------")

    for attempt in range(20):
        print("attempt no: " + str(attempt))

        try:
            if loading.value_of_css_property("display") == "block":
                has_loaded_count = 0
            else:
                time.sleep(0.05)
                has_loaded_count = has_loaded_count + 1
                break
        except:
            continue

    if has_loaded_count > 20:
        break

driver.close()
innerHTML = driver.execute_script("return document.body.innerHTML")
soup = BeautifulSoup(innerHTML, 'lxml')

names = soup.find_all('h3', class_="p-name")
prices = soup.find_all('aside', class_="pricing resp-module")
details = soup.find_all('div', class_="additional-details resp-module")
reviews = soup.find_all('div', clas_="details resp-module")

print(len(names))
print(len(prices))
print(len(details))
print(len(reviews))


checkin = "2020-04-11"
checkout = "2020-04-12"

names_list = [name.text for name in names]
price_list = [price.text for price in prices]
details_list = [detail.text for detail in details]
reviews_list = [review.text for review in reviews]

print(len(names_list))
print(len(price_list))
print(len(details_list))
print(len(reviews_list))

print(price_list)
print(names_list)

checkin_dates = [checkin] * len(names)
checkout_dates = [checkout] * len(names)

hotel_dict = dict(zip(headers, [names, details, reviews, prices, checkin_dates, checkout_dates]))
hotel_df = pd.DataFrame(hotel_dict)

print(hotel_df.shape)
print(hotel_df.head())

hotel_df.to_pickle("london_final_raw_data.pkl", protocol=3)
print("SAVED")




