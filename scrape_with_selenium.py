from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

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
                    "check-out=" + str(out_date) + "&q-rooms=1&q-room-0-adults=1&q-room-0-children=0"
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

    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'lxml')
    file = open("source.html", 'a')
    file.write(innerHTML)
    file.close()
    driver.close()
    return soup


# function to scrape data from given bs4 object
def get_soup_by_class(soup, tag, class_):
    raw_soup = soup.find_all(tag, {'class': class_})
    raw_list = []
    empty_index = None

    for element in raw_soup:
        if element.text == "":
            empty_index = raw_soup.index(element)
        raw_list.append(element.text)

    return (raw_list, empty_index)


# create raw data frame from scraped data
def get_raw_dataframe(checkin, checkout, source_soup):

    # create list of dataframe headers for hotel dataframe
    headers = ['name', 'hotel_details', 'review_box', 'price', 'checkin_date', 'checkout_date']

    # scrap name, details, price and reviews from website
    (names, _) = get_soup_by_class(source_soup, hotel_features_html["hotel_name"][0], hotel_features_html["hotel_name"][1])
    (details, _) = get_soup_by_class(source_soup, hotel_features_html["hotel_details"][0],
                                hotel_features_html["hotel_details"][1])
    (price, index_without_price) = get_soup_by_class(source_soup, hotel_features_html["hotel_price"][0], hotel_features_html["hotel_price"][1])
    (reviews, _) = get_soup_by_class(source_soup, hotel_features_html["hotel_reviews"][0],
                                hotel_features_html["hotel_reviews"][1])
    price.append("")

    print(len(names))
    print(len(details))
    print(len(price))
    print(len(reviews))
    print(index_without_price)

    # create a list of same checkins and checkouts for all hotels to be entered in the data frame
    checkin_dates = [checkin] * len(names)
    checkout_dates = [checkout] * len(names)
    print(len(checkin_dates))
    print(len(checkout_dates))

    # create python dictionary from scraped data
    hotel_dict = dict(zip(headers, [names, details, reviews, price, checkin_dates, checkout_dates]))

    # create pandas data from from the dictionary
    hotel_df = pd.DataFrame(hotel_dict)

    print(hotel_df.shape)
    print(hotel_df.head())
    return hotel_df


list_checkin = ['2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16',
                '2020-04-17', '2020-04-18', '2020-04-19']
list_checkout = ['2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16', '2020-04-17',
                 '2020-04-18', '2020-04-19', '2020-04-20']

dates = []
for checkin, checkout in zip(list_checkin, list_checkout):
    dates.append((checkin, checkout))

# empty data frame created for concating with data frames of different dates together
final_dataframe = pd.DataFrame()

dates = [('2020-04-11', '2020-04-12')]
for date in dates:
    url = generate_url_from_dates("london", date[0], date[1])
    print(url)
    print(".....url for checkin: " + str(date[0]) +" generated.....")
    source = get_mainsoup_obj(url)
    print(".....Scrolled and soup gathered......")
    dataframe = get_raw_dataframe(date[0], date[1], source)
    print("....dataframe created......")
    final_dataframe = pd.concat([final_dataframe, dataframe], ignore_index=True)
    print("-------checkin: " + str(date[0]) + " completed-------")


print("------Saving as Pickle------")
final_dataframe.to_pickle("london_final_raw_data.pkl", protocol=3)
print("SAVED")
df2 = pd.read_pickle("london_final_raw_data.pkl")
print("loaded")
final_dataframe.to_csv("london_final_raw_data.csv")
