from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


# use chrome options to open the webpage with devtools automatically
options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")

driver = webdriver.Chrome("chromedriver_linux64/chromedriver", chrome_options=options)

driver.get("https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-id=549499&q-destination=London,%20England,%20United%20Kingdom&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&sort-order=BEST_SELLER")

driver.maximize_window()

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    loading = driver.find_element_by_id("listings-loading")
    print("---------scrolled into view--------------")

    for attempt in range(20):
        print("attempt no: " + str(attempt))
        try:
            if loading.value_of_css_property("display") == "block":
                print("..loading..")
            else:
                print("loaded")
                time.sleep(0.05)
                break
        except:
            continue


