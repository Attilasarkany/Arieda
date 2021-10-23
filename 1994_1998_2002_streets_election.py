# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 21:23:37 2021

@author: Attila
"""


# i found a better source for streets
# https://valtor.valasztas.hu/valtort/jsp/tmd1.jsp?TIP=2
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

#you have to download a chromedriver-->the path will have to refer to the exe file
DRIVER_PATH = 'C:/Users/Attila/Desktop/arieda/chromedriver'


# I grabbed the data from second round!


#linkek a websitrol
#https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=8&TIP=0&URLTIP=1&URL=szavkorval&URLPAR=URL%3D2%26URLPAR%3D2&CH=a
#options = Options()
#options.headless = True
#options.add_argument("--window-size=1920,1200")
list_abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','z']
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
links_abc=[]

for k in list_abc:
    testurll='https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=8&TIP=0&URLTIP=1&URL=szavkorval&URLPAR=URL%3D2%26URLPAR%3D2&CH={}'.format(k)
    driver.get('%s' % testurll)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links=[]
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    links=links[22:]
    links_abc.append(links)




#options = Options()
#options.headless = True
#options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
solution=[]
for z in links_abc:
    
    for i in z:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # ez jó:)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[2])
        main_table['city']=city
        solution.append(main_table)
        
    
 #let the first row as a header and delete the first row cause it is redundant       


list_of_names_2018=['voting_area','street','city']

header_solution=[]
for q in solution:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018
    header_solution.append(q)

before_final=df = pd.concat(header_solution, axis=0, ignore_index=True)
#1994 btw

before_final.to_excel("before_final_1990.xlsx")
# data for budapest will not be good cause the number of tables are different
#yes, get just the links  without links=links[22:]
budapest_links=links[22:44]
driver = webdriver.Chrome(executable_path=DRIVER_PATH)


bp_solution=[]
for i in budapest_links:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # ez jó:)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[1])
        main_table['city']=city
        bp_solution.append(main_table)
        
header_solution_budapest=[]
for q in bp_solution:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018
    header_solution_budapest.append(q)

#1994 btw
before_final_bp=df = pd.concat(header_solution_budapest, axis=0, ignore_index=True)
before_final_bp.to_excel("before_final_1994_bp.xlsx")

# by hand I merged the data ( the two excel files): where there was "szavazókör" in the city I passed
# Budapest districts there

##############1998#######
DRIVER_PATH = 'C:/Users/Attila/Desktop/arieda/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

list_abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','z']
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
links_abc=[]

for k in list_abc:
    testurll='https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=15&TIP=0&URLTIP=1&URL=szavkorval&URLPAR=URL%3D2%26URLPAR%3D2&CH={}'.format(k)
                
    driver.get('%s' % testurll)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links=[]
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    links=links[22:]
    links_abc.append(links)
# it is unneccesary to use list_abc_here, it immediately grabs what we need
links_no_abc=links_abc
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
solution_1998=[]
    
for z in links_no_abc:
    for i in z:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # ez jó:)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[2])
        main_table['city']=city
        solution_1998.append(main_table)

# again here the city name for Budapest is wrong, lets correct it later
list_of_names_2018=['voting_area','street','city']

header_solution_1998=[]
for q in solution_1998:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018
    header_solution_1998.append(q)

before_final_1998=df = pd.concat(header_solution_1998, axis=0, ignore_index=True)

before_final_1998.to_excel("before_final_1998.xlsx")



###########Budapest 1998################

    DRIVER_PATH = 'C:/Users/Attila/Desktop/arieda/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    testurll='https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=15&URLTIP=1&URL=1&URLPAR=URL%3D2%26URLPAR%3D2'

    driver.get('%s' % testurll)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links=[]
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    


budapest_links_1998=links[22:45]


driver = webdriver.Chrome(executable_path=DRIVER_PATH)


bp_solution_1998=[]
for i in budapest_links_1998:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # ez jó:)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[1])
        main_table['city']=city
        bp_solution_1998.append(main_table)
        
header_solution_budapest_1998=[]
for q in bp_solution_1998:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018
    header_solution_budapest_1998.append(q)

    before_final_bp_1998=df = pd.concat(header_solution_budapest_1998, axis=0, ignore_index=True)
    before_final_bp_1998.to_excel("before_final_1998_bp.xlsx")

###############2002##################

DRIVER_PATH = 'C:/Users/Attila/Desktop/arieda/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

list_abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','z']
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
links_abc=[]

for k in list_abc:
    testurll='https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=18&TIP=0&URLTIP=1&URL=szavkorval&URLPAR=URL%3D2%26URLPAR%3D2&CH={}'.format(k)
                
    driver.get('%s' % testurll)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links=[]
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    links=links[22:]
    links_abc.append(links)
# it is unneccesary to use list_abc_here, it immediately grabs what we need
links_no_abc=links_abc
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
solution_2002=[]
    
for z in links_no_abc:
    for i in z:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # 
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[2])
        main_table['city']=city
        solution_2002.append(main_table)

# again here the city name for Budapest is wrong, lets correct it later
list_of_names_2018=['voting_area','street','city']

header_solution_2002=[]
for q in solution_2002:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018# it is okay, it is just a name for the columns
    header_solution_2002.append(q)

before_final_2002=df = pd.concat(header_solution_2002, axis=0, ignore_index=True)

before_final_2002.to_excel("before_final_2002.xlsx")

##########Budapest 2002 ###########



DRIVER_PATH = 'C:/Users/Attila/Desktop/arieda/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    testurll='https://valtor.valasztas.hu/valtort/jsp/telkiv.jsp?EA=18&URLTIP=1&URL=1&URLPAR=URL%3D2%26URLPAR%3D2'

    driver.get('%s' % testurll)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links=[]
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    


budapest_links_2002=links[22:45]


driver = webdriver.Chrome(executable_path=DRIVER_PATH)


bp_solution_2002=[]
for i in budapest_links_2002:
        testurl='https://valtor.valasztas.hu/valtort/jsp/{}'.format(i)
        driver.get('%s' % testurl)
    # ez jó:)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')
        headers=soup.find_all('b')
        dfs = pd.read_html(str(tables))
        main_table=dfs[3]
        main_table=main_table[[0,1]]
        city=str(headers[1])
        main_table['city']=city
        bp_solution_2002.append(main_table)
        
header_solution_budapest_2002=[]
for q in bp_solution_2002:
    header_row = 0
    q.columns = q.iloc[header_row]
    q=q.drop(q.index[0])
    q.columns=list_of_names_2018
    header_solution_budapest_2002.append(q)

    before_final_bp_2002=df = pd.concat(header_solution_budapest_2002, axis=0, ignore_index=True)
    before_final_bp_2002.to_excel("before_final_2002_bp.xlsx")
