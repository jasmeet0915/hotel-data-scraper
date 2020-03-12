import pandas as pd

headers = ['name', 'distance_to_city_centre', 'distance_to_airport', 'reviews', 'price', 'checkin_date', 'checkout_date']

df = pd.read_pickle("data.pkl")
review_temps = [content.split('Fabulous ')[-1].split('Good ')[-1].split('Superb ')[-1].split('Exceptional ')[-1].split('Gym ')[-1].split('Conditioning')[-1].split('friendly')[-1].split('reviews')[0] for content in df['review_box']]
review_temps = [content.split('good')[-1].split(',')[0].split('nights')[-1] for content in review_temps]

centre = [content.split(' km')[0] for content in df['hotel_details']]

print(centre[1507])
print(df['hotel_details'][1507])
city_centre = []
flag = 1
for dist in centre:
    for char in dist:
        if char.isdigit():
            dist_deci = dist.split(char)[-1]
            dist = str(char) + str(dist_deci)
            city_centre.append(dist)
            flag = 0
        if flag == 0:
            flag = 1
            break

print("------------------------------------")


airport = [content.split("centre")[-1].split(' km')[0] for content in df['hotel_details']]

for i in range(len(df['price'])):
    df['price'][i] = str(df['price'][i])

prices = [money.split('.')[-1].split('*')[-1].split("Choose")[0].split("Cancel")[0].split('Enter')[0].split('s')[-1] for money in df['price']]


print(city_centre)
print(len(df['name']))
print(len(city_centre))
print(len(airport))
print(len(review_temps))
print(len(prices))


checkin = '2020-04-11'
checkout = '2020-04-12'


checkin_dates = [checkin] * len(df['name'])
checkout_dates = [checkout] * len(df['name'])

hotel_dict = dict(zip(headers, [df['name'], city_centre, airport, review_temps, prices, checkin_dates, checkout_dates]))

hotel_df = pd.DataFrame(hotel_dict)

hotel_df.to_pickle("text_removed_data.pkl", protocol=3)
hotel_df.to_csv("text_removed_data.csv")


print(df['price'][0])

print(prices)
print(airport)
print(city_centre)

print(review_temps)