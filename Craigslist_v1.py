#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:53:18 2019

@author: kewang
"""

import requests
from bs4 import BeautifulSoup

import pandas as pd

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'Exception!'
    
def nextPage(soup):
    '''
    return: next_page url
    '''    
    url = 'https://sandiego.craigslist.org'
    body = soup.body
    button = body.section.find('span', class_ = 'buttons')
    buttonnext = button.find('a', class_ = 'button next')

    url +=  buttonnext['href']

    return url
    
def singlePost(url):
    '''
    param: url
    return: list of attributes list[str]
    
    '''
    r = getHTMLText(url)
    soup = BeautifulSoup(r,'html.parser')
    section= soup.body.section.section.section
    attrs = section.find('p', class_ = 'attrgroup')
    
    res = []
    try: 
        for a in attrs.find_all('span'):
            attr = ''
            for s in a:
                attr += s.string
            res.append(attr)
    except:
        pass
    
    return res

def fillItemList(text):
    '''
    param: text
    return: soup, list[list]
    
    
    '''
    soup = BeautifulSoup(text,'html.parser')
    body = soup.body
    for child in body.section.children:
        if child.name == 'form':
            form = child
        
    ct = form.find('div', class_ = 'content')
    item_list = ct.ul
    item_info = []

    for item in item_list.find_all('li'):
    
        item_title = item.p.a.string
        
        meta = item.p.find('span', class_ = 'result-meta')
        item_price = meta.span.string
        post_date = item.p.find('time')
        item_date = post_date['datetime']
        item_url = item.a['href']
        
        attr = singlePost(item_url) #attr = list[str]
        
        image = 'No' if len(item.a['class']) == 3 else 'Yes'
        name = item_title
        price = item_price
        postDate = item_date
        
        item_info.append([name, price, postDate, image, attr])
        
    return soup, item_info

def outputFile(d):
    '''
    param: d
    type: list[list]
    
    '''
    name, price, date, image, attr = [],[],[],[],[]
    for i in d:
        name.append(i[0])
        price.append(i[1])
        date.append(i[2])
        image.append(i[3])
        attr.append(i[4])
    
    dataframe = pd.DataFrame({'Name': name, 'Price': price, 'postDate': date, 'HasImage': image, 'Attributes': attr})
    dataframe.to_csv('/Users/kewang/craigslist_item_iphoneX.csv',index = True)

 


if __name__ == '__main__':
    url = 'https://sandiego.craigslist.org/search/sss?query=iphone%20x&sort=rel'
          
    r = getHTMLText(url)
    print('now processing page 1')
    s, d = fillItemList(r) #process first page
    
    try: 
        for i in range(10):
            print('now processing page {}'.format(i + 2))
            url = nextPage(s)
            print(url)
            r = getHTMLText(url)
            s_next, d_next = fillItemList(r)
            for i in d_next:
                d.append(i)
                s = s_next
    except:
        pass
       
    outputFile(d)

    
    
    
   
