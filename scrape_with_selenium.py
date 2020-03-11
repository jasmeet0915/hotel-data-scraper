from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

hotel_features_html = {
    "hotel_name": ("h3", "p-name"),
    "hotel_landmarks": ("ul", "property-lanmarks"),
    "hotel_details": ("div", "additional-details resp-module"),
    "hotel_reviews": ("div", "details resp-module"),
    "hotel_TA_rating": ("div", "ta-logo"),
    "hotel_price": ("aside", "pricing resp-module")
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


def get_soup_by_class(soup, tag, class_):
    raw_soup = soup.find_all(tag, {'class': class_})
    raw_list = [element.text for element in raw_soup]
    return raw_list


if __name__ == "__main__":
    source_soup = get_mainsoup_obj("https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-id=549499&q-destination=London,%20England,%20United%20Kingdom&q-check-in=2020-03-08&q-check-out=2020-03-09&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&sort-order=BEST_SELLER")
    print(source_soup)

    names = get_soup_by_class(source_soup, hotel_features_html["hotel_name"][0], hotel_features_html["hotel_name"][1])
    details = get_soup_by_class(source_soup, hotel_features_html["hotel_details"][0], hotel_features_html["hotel_details"][1])
    price = get_soup_by_class(source_soup, hotel_features_html["hotel_price"][0], hotel_features_html["hotel_price"][1])
    print("--------names-----------")
    print(names)
    print("---------details--------------")
    print(details)
    print("---------prices------------")
    print(price)

