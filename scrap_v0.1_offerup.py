# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


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

def get_location(soup):
    location_soup = soup.find("a",{"class": "_g85abvs _133jvmu8"})
    location = location_soup.get_text() if (location_soup is not None) else 'No location INFO!'
    if location != 'No location INFO!':
        city, state = location.split(',',1) 
    print(f'{location}')
    
    return location, city, state

def get_time(soup):
    time_soup = soup.find("div",{"class": "_147ao2d8"})
    time_text = time_soup.get_text() if (time_soup is not None) else 'Unknown Time!'
    
    ptn_time = r"\d+\s\w+\s"
    time = re.search(ptn_time,time_text).group(0)
    time_num, time_unit = time.split(' ',1)
    print(time_num + ' ' + time_unit + 'ago')
    return time

def get_shipping(soup):
    shipping_soup = soup.find("span",{"data-name": "delivery-info"})
    shipping = shipping_soup.get_text() if (shipping_soup is not None) else 'No shipping INFO!' # get the shipping info text
    print(f'{shipping}')
    
    ptn_dist = r"\d+" # pattern to decide distance in integer
    ptn_ship_loc = r"^Ships from" # pattern to decide shipping location
    ptn_pick_or_ship = r"^Local pickup" # pattern to decide whether shipping included
    
    if shipping != 'No shipping INFO!' and re.search(ptn_pick_or_ship,shipping) is not None:
        #print(re.search(ptn_dist,shipping))
        distance = int(re.search(ptn_dist,shipping).group(0))
        ship_loc = None
        print(f'The distance for pick-up is: {distance}')
    elif shipping != 'No shipping INFO!':
        ship_loc = re.search(ptn_ship_loc,shipping)
        distance = None
        print(f'The seller\'s location is {ship_loc}')
    else:
        raise NotImplementedError
        
    return shipping, distance, ship_loc


base_url = "https://offerup.com" # This is the main target webpage
search_results = []
search_url = base_url + "/search/?q=iphone%20x" # The search page

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
    
    print("Getting Location!")
    get_location(sub_soup)
    
    print("Getting Time!")
    get_time(sub_soup)
    
    print("Getting Shipping INFO!")
    get_shipping(sub_soup)
    
