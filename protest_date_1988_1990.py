# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 21:49:21 2021

@author: Attila
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import re


# To get the part of the links (days)
http_main = 'https://tuntetes-archivum.hu'
data  = requests.get(http_main,verify=False).text
soup = BeautifulSoup(data, 'html5lib')
soup_a = str(soup.find_all('a'))
soup_href = set(re.findall(r"a \D{4}=\D\d\d\d\d\.\d\d\.\d\d", soup_a))
soup_href_str=str(sorted(soup_href))

# we will use this to get the right url-s
days = re.findall(r"\d\d\d\d\.\d\d\.\d\d", soup_href_str)

text = len(days)*[0]
links = []
text_str = []
day1 = []
# lets save the solution into a dictionary
merge_date_text = {}
# To get all links from the main page
for i in range(len(days)):
    day = days[i]
    html = f'https://tuntetes-archivum.hu/{day}'  
    links.append(html)
    # To get the name from the link
    # The first line of the text
    data_name  = requests.get(links[i],verify=False).text
    soup_data = BeautifulSoup(data_name, 'html5lib')
    for title in soup_data.find_all('title'):
        soup_name = (title.get_text())
    name = soup_name.replace(" | Tüntetések, demonstrációk 1988-1989","") # to get rid of the main title
    
# To get the text from each of the links
    text_list = []
    data  = requests.get(links[i],verify=False).text
    soup_days = BeautifulSoup(data, 'html5lib')    
    for n in soup_days.find_all("p"):
        text_list.append(n.get_text())
        text_str = ' '.join([str(elem) for elem in text_list])
    text[i] = text_str
    merge_date_text[name] = text[i]
    
df = pd.DataFrame(data=  merge_date_text, index=[0])
df = (df.T)

df.to_excel('protest_date.xlsx')