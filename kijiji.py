import csv 
from requests_html import HTMLSession
session = HTMLSession()

# Url path with filters pre-applied. 
honda = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/honda-2006__2014-new__used/c174l1700241a54a68a49?for-sale-by=ownr'
# Chevy Cruze
chevy = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/chevrolet-2006__2014-new__used/c174l1700241a54a68a49?for-sale-by=ownr'
# Dodge Dart 
dodge = 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/dodge-2006__2014-new__used/c174l1700241a54a68a49?for-sale-by=ownr'
# Volkswagen Jetta 
volkswagen= 'https://www.kijiji.ca/b-cars-trucks/woodstock-on/volkswagen-2006__2014-new__used/c174l1700241a54a68a49?for-sale-by=ownr'
# Volkswagen Golf 

urls = [honda, chevy, dodge, volkswagen]

def main(url):
    r = session.get(url)

    my_dict = {}
    price_list = []
    title_list = []
    description_list = []
    distance_list = []
    vehicle_key = []
    links = []
    cleaned_links = []

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
        links = title.absolute_links
        for link in links: 
            cleaned_links.append(link)

    descriptions = r.html.find('.description')
    for description in descriptions:
        description_list.append(description.text)

    distances = r.html.find('.location')
    for distance in distances: 
        distance_list.append(distance.text)

    for x in range(list_length):
        my_dict[vehicle_key[x]] = {'title': title_list[x], 'price':price_list[x], 'distance':distance_list[x], 'description':description_list[x], 'link':cleaned_links[x]}

    return my_dict 


txt_files = ['honda', 'chevy', 'dodge', 'volkswagen']
count = 0
for url in urls:
    my_dict = main(url)
    with open(txt_files[count]+'.txt', 'w', encoding="utf-8") as f:
        count += 1
        for key in my_dict:
            f.write("\n")
            for obj in my_dict[key]:
                f.write("%s\n"%my_dict[key][obj])
                
            







