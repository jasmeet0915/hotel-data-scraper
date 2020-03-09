from bs4 import BeautifulSoup
import requests


with open("source.html") as source_file:
    soup = BeautifulSoup(source_file, 'lxml')

body = soup.body
hotels_div = body.find('div', class_="resp-section")
main = hotels_div.find('main', class_="inner-section")
search_results = main.find('div', class_="resp-row", id="search-results")
hotel_col = search_results.find('div', class_="resp-col main").div

hotel_list = hotel_col.find('section', id="").div.ol
#hotel_data = hotel_list.li.article.section.div
hotel_data = hotel_list.find_all('li', class_="hotel sponsored")

for hotel in hotel_data:
    data = hotel.article.section.div
    price = hotel.aside.div.a.ins.text
    hotel_name = data.h3.text
    #next_page_url = "in.hotels.com" + str(hotel_data.h3.a['href'])
    #print(next_page_url)

    #star_html = requests.get(next_page_url)
    #star_soup = BeautifulSoup(star_html)
    #print(star_soup.prettify())

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
    print("Distance to city center: " + str(dist_cc))
    print("Distance from airport: " + str(dist_aero))
    print("Price of Room: " + str(price[2:]))
    print("")
    #print(landmarks.prettify())