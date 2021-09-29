# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 22:38:36 2021

@author: Attila
"""

import pandas as pd
import os
import re


os.chdir('C:\\Users\\Attila\\Desktop\\arieda\\valasztasi_eredmenyek_1990-2019\\2014_parlamenti')


# szavazokor is the smallest area of aggregation
# we would like to merge:2014 and 2018
# there was a law change in Hungary in 2012 regarding the elections
# source and information about the elections: https://en.wikipedia.org/wiki/2014_Hungarian_parliamentary_election
# soource for the variables  (origin:2002!!):https://static.valasztas.hu/parval2002/esz/esz_hu/informaciok_ind.htm
# from the above source,please check these:"fogalmak" or "rövidítések" jegyzéke (definitons or abbreviations)
# for english version, you can find some defintions here: (again: these definitions were defnied in 2002, did not find others)
# https://static.valasztas.hu/parval2002/esz/esz_hu/informaciok_ind.htm
# https://static.valasztas.hu/parval2006/hu/17/fogalmak/fogalmak1.html
 
#open the xlsx file from 2014
election_2014_szavazokor=pd.read_excel(io='Egyéni-szavazás-jkv.xlsx', sheet_name='Sheet1',na_filter=False)

#change folder
os.chdir('C:\\Users\\Attila\\Desktop\\arieda\\valasztasi_eredmenyek_1990-2019\\2018_parlamenti')

#open the xlsx file from 2018
election_2018_szavazokor=pd.read_excel(io='Egyéni_szavazás_szkjkv.xlsx', sheet_name='Munka1',na_filter=False)

# we need to rename the columns but first lets check whether the columns name are the same in the two files

#make a list from the columns
columns_name_2018=election_2018_szavazokor.columns.values.tolist()
columns_name_2014=election_2014_szavazokor.columns.values.tolist()
#save the columns name as an xls file and descrie them
columns_name=pd.DataFrame(columns_name_2018,columns=["Name of the variables"])
columns_name.to_excel("decription_of_the_variables.xlsx")

# check whether the columns are the same
if columns_name_2018 == columns_name_2014:
    print ("The lists are identical")
else :
    print ("The lists are not identical")

#yes the lists are identical so we can just concatenate them but first lets rename the columns
list_of_names=["voting_area_id","JKV_id","individual","county_code","county","OEVK","chief_town_of_the_county","SZH_KER",
               "settlement_serial_number","settlement","voting_area",
               "number_of_registered_voters","appeared_voters","votes_in_the_urn","diff_between_appeared_urn",
               "invalid","valid","candidate","party","votes"]

#update the name of the columns    
election_2014_szavazokor.columns=list_of_names
election_2018_szavazokor.columns=list_of_names
# add an additional identifier for each of the groups
election_2014_szavazokor["year"]=2014
election_2018_szavazokor["year"]=2018

#concatenate the tables
election_2014_2018_joined = pd.concat([election_2014_szavazokor, election_2018_szavazokor])
#it takes time to save it as an excel
election_2014_2018_joined .to_excel("election_2014_2018_joined.xlsx")

####################### get the street numbers


import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import re




# To get all links from the main page
# first do it with data from 2014: https://static.valasztas.hu/dyn/pv14/szavossz/hu/TK/szkkivtk.html

     
            
# Make a list of letter from the web site
    albab1 = list(string.ascii_lowercase)
    list_to_remove = ['q','w','x','y']
    list1 = [ i for i in albab1 if i not in list_to_remove]
    
    # To get all links from the main page
    final = []
    links_main = []
    for i in range(len(list1)):
        letter = list1[i]
        html_main = f'https://static.valasztas.hu/dyn/pv14/szavossz/hu/TK/szkkivtk{letter}.html'
        links_main.append(html_main)    
    # To get all links from the every letter  
    # here we are going to have duplicates
        for m in range(len(links_main)):
            html = links_main[m]
            data  = requests.get(html).text
            soup = BeautifulSoup(data, 'html5lib')
            all_a = soup.find_all('a')
            for i in range(len(all_a)):
                all_aa = str(all_a[i])
                result = re.findall(r"\D\d\d/\D\d\d\d\D+html", all_aa)
                if result != []:
                    final.append(result)
    # links for cities
    links_city = []
    for i in range(len(final)):
        letter = final[i][0]
        html_main = f'https://static.valasztas.hu/dyn/pv14/szavossz/hu/{letter}'
        links_city.append(html_main)    



colums_name=["Sorszám","Cím","Átjelentkezettek szavazási helye","Átjelentkezettek és külképviseleti szavazatok számlálására kijelölt","district"]

# I made the first =cheat_cities_dataframe

links_city[1]

data  = requests.get("https://static.valasztas.hu/dyn/pv14/szavossz/hu/M07/T001/szkkiv.html"
).text
soup = BeautifulSoup(data, 'html5lib')
table = soup.find_all('h3')
name_of_the_settlement=table[0].get_text()
read_html_pandas_data = pd.read_html(str(soup),converters={"Sorszám": str})
cities_dataframe = read_html_pandas_data[1]
cities_dataframe['district']=name_of_the_settlement
cheat_cities_dataframe=cities_dataframe


#grab the street name for each of the sorszám=voting_area+ get the header
# this header will contains additional information: we need to get rid of it
# because we want to merge on this information:district = settlement+ others
for i in links_city[1:]:

    data  = requests.get(i).text
    soup = BeautifulSoup(data, 'html5lib')
    table = soup.find_all('h3')
    name_of_the_settlement=table[0].get_text()
    read_html_pandas_data = pd.read_html(str(soup),converters={"Sorszám": str})
    cities_dataframe = read_html_pandas_data[1]
    cities_dataframe['district']=name_of_the_settlement
    cheat_cities_dataframe=cheat_cities_dataframe.append(cities_dataframe)


########### I found out that we have duplicates, but just after 
########### the process.. lets keep everything, and delete afterwards

# check duplicates
links_city_df = pd.DataFrame(links_city,columns =['htmls'])
links_city_df=links_city_df.sort_values(by='htmls')
# yes we have, no problem drop them later. 

######################################################################

cheat_cities_dataframe.to_excel('district_streets.xlsx')
cheat_cities_dataframe['szavazokor_and_center'] = cheat_cities_dataframe['district'].str.extract(r'((Budapest\s)?\S+\sszavazókörei)')

cheat_cities_dataframe[['settlement','other']] = cheat_cities_dataframe.szavazokor_and_center.str.split("szavazókörei",expand=True)

cheat_cities_dataframe=cheat_cities_dataframe.rename(columns={'Cím': 'street','Sorszám': 'voting_area'})
cheat_cities_dataframe.to_excel('settlements_streets_2014.xlsx')
## check whether there are missing values in the settlement column
## we are doing this because we would like to merge the other data set on this column
cheat_cities_dataframe['settlement'].isnull().values.any()


############### streets for 2018 #####################################x
# the website is horrible for this, so I need to do differently.... ######
## very strange: when there is 0 1 2 3.. "szavazókör"=voting_area
# many times the street names are the same
import codecs
from bs4 import BeautifulSoup
import pandas as pd
os.chdir('file:///C:/Users/Attila/Desktop/arieda/valasztasi_eredmenyek_1990-2019/2018_parlamenti/html/szavossz/hu/oevker.html')




final=[]
f = open('oevker.html' ,encoding="utf8")    #read File
content = f.read()
soup = BeautifulSoup(content, 'html.parser')
all_a_2018 = soup.find_all('a')
       
#get all of the links     
for i in range(len(all_a_2018)):
      ka= str(all_a[i])
      result = re.findall(r"\D\d\d/\D\d\d\D+html", ka)
      if result != []:
            final.append(result)

# now we have all of the links, just need to grab the tables
tables_settlements_2018=pd.DataFrame()
# we need the 5th table. lets make equal tables_settlements_2018 to the first 
#table and after that we just append this DataFrame
pds_df = pd.read_html('M01/E01/evkjkv.html',converters={"Sorszám": str})

tables_settlements_2018=pds_df[5]

for i in final[1:]:
    temporary=pd.read_html(i[0],converters={"Sorszám": str})
    table_5=temporary[5]

    tables_settlements_2018=tables_settlements_2018.append(table_5)


list_of_names_street_2018=["settlement","voting_area","steet","Átjelentkezettek és külképviseleti szavazatok számlálására kijelölt",'Átjelentkezettek és településszintű lakosok szavazására kijelölt']
tables_settlements_2018.columns=list_of_names_street_2018
tables_settlements_2018.to_excel('settlements_steet_2018.xlsx')

###### put everything together: settlements_steet_2018.xlsx and settlements_streets_2014.xlsx
###### problems:"Budapest xy kerület " is Budapest xy ker. in the ohter file.
###### Maybe there are orther problems as well...

settlement_2018 = pd.read_excel (r'C:\Users\Attila\Desktop\arieda\valasztasi_eredmenyek_1990-2019\settlements_steet_2018.xlsx',converters={"voting_area": str})
settlement_2014 = pd.read_excel (r'C:\Users\Attila\Desktop\arieda\valasztasi_eredmenyek_1990-2019\settlements_streets_2014.xlsx',converters={"voting_area": str})

#sort by settlement
settlement_2018=settlement_2018.sort_values(by=['settlement'])
settlement_2014=settlement_2014.sort_values(by=['settlement'])
# delete some useless columns
del settlement_2014['szavazokor_and_center']
del settlement_2014['district']
del settlement_2014['other']

#check if other columns are the same
columns_name_2018=settlement_2018.columns.values.tolist()
columns_name_2014=settlement_2014.columns.values.tolist()

if columns_name_2018 == columns_name_2014:
    print ("The lists are identical")
else :
    print ("The lists are not identical")
    
# if we carefully check we do not need the following columns eather: these
# are about foreing representation and those who changed location to vote..

del settlement_2014['Átjelentkezettek szavazási helye']
del settlement_2014['Átjelentkezettek és külképviseleti szavazatok számlálására kijelölt']
del settlement_2018['Átjelentkezettek és külképviseleti szavazatok számlálására kijelölt']
del settlement_2018['Átjelentkezettek és településszintű lakosok szavazására kijelölt']

settlement_2018 = settlement_2018[['Unnamed: 0','voting_area','settlement','steet']]
settlement_2014 = settlement_2014[['Unnamed: 0','voting_area','settlement','street']]
# mistake .. in settlement_2018 street is steet...
list_of_names_2018=['Unnamed: 0','voting_area','settlement','street']
settlement_2018.columns=list_of_names_2018

### we need to drop the duplicates from 2014 elections
settlement_try_2014=settlement_2014.drop_duplicates(subset=['street'])
settlement_try_2018=settlement_2018.drop_duplicates(subset=['street'])
# if we carefully check then we see that the number of obs are different
# plus we deleted important rowes:where the voting are
# different but the streets are the same. we need to do group by
groups_2018=settlement_2018.groupby(['settlement','voting_area']).ngroup()
settlement_2018['groups']=groups_2018

groups_2014=settlement_2014.groupby(['settlement','voting_area']).ngroup()
settlement_2014['groups']=groups_2014

# now we can drop the duplicates by the groups identifier
settlement_2018 = settlement_2018.drop_duplicates(subset=['groups'])
settlement_2014 = settlement_2014.drop_duplicates(subset=['groups'])

settlement_2018.to_excel('cleaned_streets_2018.xlsx')
settlement_2014.to_excel('cleaned_streets_2014.xlsx',encoding="utf8")

########### here i was just trying to merge, finally  I did but it is wrong

# lets merge the data on the settlement and voting area
# we expect many unmatch because i.e "kerület"!= "ker." regarding Budapest
# first we need to have the same type
settlement_2014['groups'] = settlement_2014['groups'].astype(str)
settlement_2014['settlement'] = settlement_2014['settlement'].astype(str)
settlement_2014['voting_area'] = settlement_2014['voting_area'].astype(str)

# cant merge, try this one
settlement_2014=settlement_2014.reset_index(drop=True)
settlement_2018.reset_index(drop=True)

settlement_2018['groups'] = settlement_2018['groups'].astype(str)
settlement_2018['settlement'] = settlement_2018['settlement'].astype(str)

#try


merged_data_election_2014_2018 = settlement_2014.merge(settlement_2018.rename({'street': 'street_r','voting_area': 'voting_area_r'},axis=1), left_on=["street","voting_area"],right_on=["street_r","voting_area_r"],how="left",indicator=True)

