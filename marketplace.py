from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup as soup 
import re 
import pandas as pd 

base_url = 'https://www.facebook.com/marketplace/110990915591698/vehicles?'

max_year = 2010
min_year = 2006
make = 308436969822020 #Honda 
model = 337357940220456 #Civic
folder = 'marketplace-raw/'
file = '8th-Gen-Honda-Civic.csv'

url = f"{base_url}maxYear={max_year}&minYear={min_year}&sortBy=creation_time_descend&make={make}&model={model}"

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(5)

n_scrolls = 3
for i in range(1, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

html_source = driver.page_source
market_soup = soup(html_source, 'html.parser')
driver.quit()

titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
titles_list = [title.text.strip() for title in titles_div]
prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
prices_list = [price.text.strip() for price in prices_div]
mileage_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
mileage_list = [mileage.text.strip() for mileage in mileage_div]
urls_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv")
urls_list = [url.get('href') for url in urls_div]

pattern = re.compile(r'(\w+(?:-\w+)?, [A-Z]{2})')
mileage_list2 = []
for item in mileage_list:
    if item == '':
        mileage_list2.append('0 Km')
    else:
        mileage_list2.append(item)

mileage_pattern_km = r'(\d+)K km'
mileage_pattern_low_km = r'(\d+) km'
mileage_pattern_miles = r'(\d+)K miles'

mileage_clean = []

for item in mileage_list2:
    match_mileage_km = re.search(mileage_pattern_km, item)
    match_mileage_miles = re.search(mileage_pattern_miles, item)
    match_mileage_low_km = re.search(mileage_pattern_low_km, item)

    if match_mileage_km or match_mileage_low_km or match_mileage_miles:
        if match_mileage_km:
            mileage_clean.append(int(match_mileage_km.group(1))*1000)
        elif match_mileage_low_km:
            mileage_clean.append(int(match_mileage_low_km.group(1)))
        else:
            mileage_clean.append(int(match_mileage_miles.group(1))*1600)

vehicles_list = []

for i, item in enumerate(titles_list):
        cars_dict = {}

        title_split = titles_list[i].split()

        cars_dict['Year'] = int(title_split[0])
        cars_dict['Make'] = title_split[1]
        cars_dict['Model'] = title_split[2]
        cars_dict['Price'] = re.sub(r'[^\d.]','', prices_list[i])
        cars_dict['Mileage'] = mileage_clean[i]
        cars_dict['URL'] = "https://www.facebook.com" + urls_list[i]
        vehicles_list.append(cars_dict)

vehicles_df = pd.DataFrame(vehicles_list)
vehicles_df.to_csv(folder + file)

