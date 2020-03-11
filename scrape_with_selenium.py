from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# aside tag used for hotel_price because <div class="price"> is not used for soldout hotels
# dictionary with required data and respective tags
hotel_features_html = {
    "hotel_name": ("h3", "p-name"),
    "hotel_landmarks": ("ul", "property-landmarks"),
    "hotel_details": ("div", "additional-details resp-module"),
    "hotel_reviews": ("div", "details resp-module"),
    "hotel_TA_rating": ("div", "ta-logo"),
    "hotel_price": ("aside", "pricing resp-module")
}


# generate url for specific place and dates
def generate_url_from_dates(city, in_date, out_date):
    if city == "london":
        url_london = "https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-" \
                    "id=549499&q-destination=London,%20England,%20United%20Kingdom&q-check-in=" + str(in_date) + "&q-" \
                    "check-out=" + str(out_date) + "2020-03-14&q-rooms=1&q-room-0-adults=1&q-room-0-children=0"
        return url_london

    if city == "paris":
        url_paris = "https://in.hotels.com/search.do?resolved-location=CITY%3A504261%3AUNKNOWN%3AUNKNOWN&destination-" \
                "id=504261&q-destination=Paris,%20France&q-check-in=" + str(in_date) + "&q-" \
                "check-out=" + str(out_date) + "&q-rooms=1&q-room-0-adults=1&q-room-0-children=0"
        return url_paris


# function to infinitely scroll to bottom of the page till no more hotels can be loaded and return soup of body
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


# create raw data frame from scraped data
def get_raw_dataframe(checkin, checkout, source_soup):

    # create list of dataframe headers for hotel dataframe
    headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

    # scrap name, details, price and reviews from website
    names = get_soup_by_class(source_soup, hotel_features_html["hotel_name"][0], hotel_features_html["hotel_name"][1])
    details = get_soup_by_class(source_soup, hotel_features_html["hotel_details"][0],
                                hotel_features_html["hotel_details"][1])
    landmarks = get_soup_by_class(source_soup, hotel_features_html["hotel_landmarks"][0],
                                  hotel_features_html["hotel_landmarks"][1])
    price = get_soup_by_class(source_soup, hotel_features_html["hotel_price"][0], hotel_features_html["hotel_price"][1])
    reviews = get_soup_by_class(source_soup, hotel_features_html["hotel_reviews"][0],
                                hotel_features_html["hotel_reviews"][1])

    print("--------names-----------")
    print(names)
    print(len(names))
    print("---------details--------------")
    print(details)
    print(len(details))
    print("---------prices------------")
    print(price)
    print(len(price))
    print("---------reviews-----------")
    print(reviews)
    print(len(reviews))
    print("-----------landmarks-----------")
    print(landmarks)
    print(len(landmarks))

    # create a list of same checkins and checkouts for all hotels to be entered in the data frame
    checkin_dates = [checkin] * len(names)
    checkout_dates = [checkout] * len(names)

    # create python dictionary from scraped data
    hotel_dict = dict(zip(headers, [names, details, reviews, price, landmarks, checkin_dates, checkout_dates]))

    # create pandas data from from the dictionary
    hotel_df = pd.DataFrame(hotel_dict)

    print(hotel_df.shape)
    print(hotel_df.head())
    return hotel_df


url = generate_url_from_dates("london", "2020-03-13", "2020-03-14")
source = get_mainsoup_obj(url)
dataframe = get_raw_dataframe("2020-03-13", "2020-03-14", source)

list_checkin = ['2020-03-11', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16',
                '2020-03-17', '2020-03-18', '2020-03-19']
list_checkout = ['2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17',
                 '2020-03-18', '2020-03-19', '2020-03-20']

dates = []
for checkin, checkout in zip(list_checkin, list_checkout):
    dates.append((checkin, checkout))

