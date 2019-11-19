# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import re
import time
import os


def get_title(soup):
    title_soup = soup.find("h1",{"class": "_t1q67t0 _1juw1gq"})
    title = title_soup.get_text()
    print(f'{title}')
    
    return title


def get_value(soup):
    value_soup = soup.find("span",{"class": "_ckr320"})
    value = value_soup.get_text() if (value_soup is not None) else 'Sold!'
    print(f'{value}')
    money = int(value) if value.isdigit() else None
    
    return value,money


def get_condition(soup):
    condition_soup = soup.find("span",{"data-test": "item-condition"})
    condition = condition_soup.get_text() if (condition_soup is not None) else 'No Condition INFO!'
    print(f'{condition}')
    
    return condition


def get_description(soup):
    description_soup = soup.find("div",{"data-test": "item-description"})
    description = description_soup.get_text() if (description_soup is not None) else 'No Description!'
    print(f'{description}')

    return description


def get_picture(soup):
    picture_soup = soup.find_all("img",{"class": "_fk4cz1","src": re.compile("https://photos\.offerup\.com/.")})
    pic_num = len(picture_soup)
    pic_urls = []
    if pic_num != 0:
        for i in range(len(picture_soup)):
            pic_urls.append(picture_soup[i]['src']) 
    print(f'Picture number is: {pic_num}')
    return pic_num, pic_urls

def get_shipping(soup):
    delivery_soup = soup.find("span",{"class": "_147ao2d8 hidden-xs _149pqlo","data-name": "delivery-info"})
    shipping_soup = soup.find("span",{"class": "_1v68mn6s _17axpax","data-name": "shipping-text"})
    # get the delivery info text
    delivery = delivery_soup.get_text() if (delivery_soup is not None) else 'No delivery INFO!'
    # get the shipping info text
    shipping = shipping_soup.get_text() if (shipping_soup is not None) else 'No shipping INFO!'
    
    # pattern to decide pick-up distance in integer
    ptn_dist = r"\d+" 
    # pattern to decide shipping location & price (when only delivery option is available)
    print('shipping is: ',shipping)
    ptn_ship_loc_price = r"(?<=from ).+" 
    # pattern to decide shipping price (when both delivery and pick-up options are available)
    ptn_ship_price = r"(?<=Ships for \$)"
    # pattern to decide whether shipping included
    # ptn_pick = r"^Local pickup" 
    
    distance = None
    ship_loc = None
    ship_price = None
    
    if delivery != 'No delivery INFO!':
        distance = int(re.search(ptn_dist,delivery).group(0))
        print(f'The distance for pick-up is: {distance}')
    
    if shipping != 'No shipping INFO!' and delivery != 'No delivery INFO!':
        ship_price = re.search(ptn_ship_price,shipping).group(0)
        print(f'The shipping price is {ship_price}')
        
    if shipping != 'No shipping INFO!' and delivery == 'No delivery INFO!':
        ship_loc_price = re.search(ptn_ship_loc_price,shipping).group(0)
        ship_loc = ship_loc_price.split(' for $')[0]
        ship_price = ship_loc_price.split(' for $')[1]
        print('ship_price is: ',ship_price)
        print(f'The seller\'s location is: {ship_loc}')
        
    return delivery, shipping, distance, ship_loc, ship_price
    
def get_location(soup,ship_loc):
    location_soup = soup.find("a",{"class": "_g85abvs _133jvmu8"})
    # when the product has shipping option
    if ship_loc is not None:
        location = ship_loc
        city, state = location.split(',',1)
        print(f'{location}')
        return location, city, state
    # when pick-up is the option
    else:
        location = location_soup.get_text() if (location_soup is not None) else 'No location INFO!'
        if location != 'No location INFO!':
            city, state = location.split(',',1)
            print(f'{location}')
            return location, city, state
        else:
            print(f'{location}')
            city = None
            state = None
            return location, city, state


def get_time(soup):
    time_soup = soup.find("div",{"class": "_147ao2d8"})
    time_text = time_soup.get_text() if (time_soup is not None) else 'Unknown Time!'
    
    ptn_time = r"\d+\s\w+\s"
    time = re.search(ptn_time,time_text).group(0)
    time_num, time_unit = time.split(' ',1)
    print(time_num + ' ' + time_unit + 'ago')
    return time

base_url = "https://offerup.com" # This is the main target webpage
search_results = []
#search_url = base_url + "/search/?q=iphone%20x&delivery_param=s" # The search page
search_url = base_url + "/search/?q=iphone%20x" # The search page

scroll_times = 5
cwd = os.path.abspath(os.path.dirname(__file__))
path_driver = cwd + '/chromedriver'
browser = webdriver.Chrome(path_driver)
browser.get(search_url)
browser.implicitly_wait(10)

for _ in range(scroll_times):
    # execute_script will scroll the page down to the bottom
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)  # sleep a little while to avoid delay or conflict

print("Search Starts")
html = urlopen(search_url).read().decode('utf-8') # Load the webpage
soup = BeautifulSoup(html, features='lxml') # BF4 analysis
print("Search Finished!")

# get all the item urls
sub_urls = soup.find_all("a", {"class": "_109rpto _1anrh0x", "href": re.compile("/item/detail/\d+/")})
if len(sub_urls) != 0:
    for i in range(len(sub_urls)):
        search_results.append(sub_urls[i]['href'])
else:
    # no valid sub link found
    pass
print(search_results)

for items in search_results:
    full_url = base_url + items
    print(f'\nLoading Url: {full_url}')
    sub_html = urlopen(full_url).read().decode('utf-8')
    sub_soup = BeautifulSoup(sub_html, features='lxml')
    print("Loading Item Finished!")
    
    print("Getting Title!")
    get_title(sub_soup)
    
    print("Getting Value!")
    get_value(sub_soup)
    
    print("Getting Item Condition!")
    get_condition(sub_soup)
    
    print("Getting Item Description!")
    get_description(sub_soup)
    
    print("Getting Item Picture")
    get_picture(sub_soup)
    
    print("Getting Shipping INFO!")
    delivery, shipping, distance, ship_loc,ship_price = get_shipping(sub_soup)
    
    print("Getting Location!")
    location,city,state = get_location(sub_soup,ship_loc)
    
    print("Getting Time!")
    get_time(sub_soup)
