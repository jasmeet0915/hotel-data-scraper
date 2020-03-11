from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd

hotel_features_html = {
    "hotel_name": ("h3", "p-name"),
    "hotel_landmarks": ("ul", "property-lanmarks"),
    "hotel_details": ("div", "additional-details resp-module"),
    "hotel_reviews": ("div", "details resp-module"),
    "hotel_TA_rating": ("div", "ta-logo"),
    "hotel_price": ("div", "price")
}


def get_mainsoup_obj(url):
    # use chrome options to open the webpage with devtools automatically to keep list-loadings element in view
    options = webdriver.ChromeOptions()
    options.add_argument("--auto-open-devtools-for-tabs")

    driver = webdriver.Chrome("chromedriver_linux64/chromedriver", chrome_options=options)

    # chrome window and maximize it
    driver.get(url)
    driver.maximize_window()

    '''has_loaded_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        loading = driver.find_element_by_id("listings-loading")
        print("---------scrolled into view--------------")

        for attempt in range(20):
            print("attempt no: " + str(attempt))

            try:
                if loading.value_of_css_property("display") == "block":
                    print("..loading..")
                    has_loaded_count = 0
                else:
                    print("loaded")
                    time.sleep(0.05)
                    has_loaded_count = has_loaded_count + 1
                    break
            except:
                continue

        if has_loaded_count > 20:
            break
'''
    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'lxml')
    driver.close()
    return soup


# function to scrape data from given bs4 object
def get_soup_by_class(soup, tag, class_):
    raw_soup = soup.find_all(tag, {'class': class_})
    raw_list = [element.text for element in raw_soup]
    return raw_list


def get_raw_dataframe(checkin, checkout, source_soup):

    # create list of dataframe headers for hotel dataframe
    headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

    # scrap name, details, price and reviews from website
    names = get_soup_by_class(source_soup, hotel_features_html["hotel_name"][0], hotel_features_html["hotel_name"][1])
    details = get_soup_by_class(source_soup, hotel_features_html["hotel_details"][0],
                                hotel_features_html["hotel_details"][1])
    price = get_soup_by_class(source_soup, hotel_features_html["hotel_price"][0], hotel_features_html["hotel_price"][1])
    reviews = get_soup_by_class(source_soup, hotel_features_html["hotel_reviews"][0],
                                hotel_features_html["hotel_reviews"][1])

    print("--------names-----------")
    print(names)
    print("---------details--------------")
    print(details)
    print("---------prices------------")
    print(price)
    print("---------landmarks------------")
    print("---------reviews-----------")
    print(reviews)

    # create python dictionary from scraped data
    hotel_dict = dict(zip(headers, [names, details, reviews, price, checkin, checkout]))

    # create pandas data from from the dictionary
    hotel_df = pd.DataFrame(hotel_dict)

    print(hotel_df.shape)
    print(hotel_df.head())
    return hotel_df

