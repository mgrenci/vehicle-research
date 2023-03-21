import csv 
from requests_html import HTMLSession
session = HTMLSession()

# Url path with filters pre-applied. 
honda_civic = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/honda-civic-2006__2014-new__used/c174l1700241a54a1000054a68a49?radius=77.0&address=Woodstock%2C+ON&ll=43.131497,-80.747165&for-sale-by=ownr'
# Chevy Cruze
chevy_cruze = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/chevrolet-cruze-2006__2014-new__used/c174l1700241a54a1000054a68a49?ll=43.131497%2C-80.747165&for-sale-by=ownr&address=Woodstock%2C+ON&radius=77.0'
# Dodge Dart 
dodge_dart = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/dodge-dart-2006__2014/c174l1700241a54a1000054a68?radius=77.0&address=Woodstock%2C+ON&ll=43.131497,-80.747165&for-sale-by=ownr'
# Volkswagen Jetta 
volkswagen_jetta = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/volkswagen-jetta-2006__2014/c174l1700241a54a1000054a68?radius=77.0&address=Woodstock%2C+ON&ll=43.131497,-80.747165&for-sale-by=ownr'
# Volkswagen Golf 
volkswagen_golf = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/volkswagen-golf-2006__2014/c174l1700241a54a1000054a68?radius=77.0&address=Woodstock%2C+ON&ll=43.131497,-80.747165&for-sale-by=ownr'


urls = [honda_civic, chevy_cruze, dodge_dart, volkswagen_golf, volkswagen_jetta]

def main(url):
    r = session.get(url)

    my_dict = {}
    price_list = []
    title_list = []
    description_list = []
    distance_list = []
    vehicle_key = []
    date_list = []

    infos = r.html.find('.info')
    list_length = len(infos)
    for length in range(list_length):
        vehicle_key.append('vehicle'+str(length+1)) 

    prices = r.html.find('.price')
    for price in prices: 
        price_list.append(price.text)

    titles = r.html.find('a.title')
    for title in titles:
        title_list.append(title.text)

    descriptions = r.html.find('.description')
    for description in descriptions:
        description_list.append(description.text)

    distances = r.html.find('.distance')
    for distance in distances: 
        distance_list.append(distance.text)

    dates = r.html.find('.date-posted')
    for date in dates: 
        date_list.append(date.text)

    for x in range(list_length):
        my_dict[vehicle_key[x]] = {'title': title_list[x], 'price':price_list[x], 'distance':distance_list[x], 'date-posted':date_list[x], 'description':description_list[x]}

    return my_dict 


txt_files = ['honda-civic', 'chevy-cruze', 'dodge-dart', 'volkswagen-golf', 'volkswagen-jetta']
count = 0
for url in urls:
    my_dict = main(url)
    with open(txt_files[count]+'.txt', 'w') as f:
        count += 1
        for key in my_dict:
            f.write("\n")
            for obj in my_dict[key]:
                f.write("%s\n"%my_dict[key][obj])
            







