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
    return value

def get_location(soup):
    location_soup = soup.find("a",{"class": "_g85abvs _133jvmu8"})
    location = location_soup.get_text() if (location_soup is not None) else 'No location INFO!'
    print(f'{location}')
    return location

def get_time(soup):
    time_soup = soup.find("div",{"class": "_147ao2d8"})
    time = time_soup.get_text() if (time_soup is not None) else 'Unknown Time!'
    print(f'{time}')
    return time


base_url = "https://offerup.com" # This is the main target webpage
search_results = []
search_url = base_url + "/search/?q=iphone%20x" # The search page

print("Search Starts")
html = urlopen(search_url).read().decode('utf-8') # Load the webpage
soup = BeautifulSoup(html, features='lxml') # BF4 analysis
print("Search Finished!")

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
    
    print("Getting Location!")
    get_location(sub_soup)
    
    print("getting Time!")
    get_time(sub_soup)
    
