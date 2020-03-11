from bs4 import BeautifulSoup
import requests

source = requests.get("https://in.hotels.com/search.do?resolved-location=CITY%3A549499%3AUNKNOWN%3AUNKNOWN&destination-id=549499&q-destination=London,%20England,%20United%20Kingdom&q-check-in=2020-03-08&q-check-out=2020-03-09&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&sort-order=BEST_SELLER")
source = source.text
soup = BeautifulSoup(source, 'lxml')
print("source downloaded")

body = soup.body
hotels_div = body.find('div', class_="resp-section")
main = hotels_div.find('main', class_="inner-section")
search_results = main.find('div', class_="resp-row", id="search-results")
hotel_col = search_results.find('div', class_="resp-col main").div


hotel_list = hotel_col.find('section', id="").div.ol
#hotel_data = hotel_list.li.article.section.div
hotel_data = hotel_list.find_all('li')


for hotel in hotel_data:
    print(hotel['class'][0])

    if "hotel" in hotel['class'][0]:
        data = hotel.article.section.div            # div tag with hotel data
        if hotel.aside.div is None:
            price = "0"
        else:
            price = hotel.aside.div.a.ins.text[2:]                                                     # aside tag with price data
        next_page_url = "in.hotels.com" + str(hotel.article.section.div.h3.a['href'])          # hotel specific page url

        '''star_html = requests.get(next_page_url)
        star_soup = BeautifulSoup(star_html, 'lxml')
        print(star_soup.prettify())
        star_body = star_soup.body
        main_section = body.find('div', class_="resp-section").main
        resp_row = main_section.find('div', class_="resp-row clearfix dateful")
        resp_row = resp_row.find('div', class_="clearfix col-24-24").div.div.div
        rating = resp_row.find('span', class_="star-rating-text widget-star-rating-overlay widget-tooltip widget-tooltip-responsive widget-tooltip-ignore-touch")
        rating = rating.span.text
    '''


        hotel_name = data.h3.text
        hotel_resp_module = data.find('div', class_ ="details resp-module")
        landmarks = hotel_resp_module.find('div', class_="additional-details resp-module").div.ul
        landmarks = landmarks.find_all('li', class_="")

        dist_cc = landmarks[0].text.split(" ")
        dist_cc = dist_cc[0]
        dist_aero = landmarks[1].text.split(" ")
        dist_aero = dist_aero[0]

        rating = hotel_resp_module.find('div', class_="reviews-box resp-module").strong.text
        rating = rating.split(" ")


        print("Name of hotel: " + str(hotel_name))
        print("Rating of the Hotel: " + str(rating[1]))
        #print("Stars of hotel: " + str(rating[0]))
        print("Distance to city center: " + str(dist_cc))
        print("Distance from airport: " + str(dist_aero))
        print("Price of Room: " + price)
        print("")
        #print(landmarks.prettify())


with open("next.html") as next_page:
    next = BeautifulSoup(next_page, 'lxml')


