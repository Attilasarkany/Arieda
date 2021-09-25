# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 22:38:36 2021

@author: Attila
"""

import pandas as pd
import os

os.chdir('C:\\Users\\Attila\\Desktop\\arieda\\valasztasi_eredmenyek_1990-2019\\2014_parlamenti')


# szavazokor is the smallest area of aggregation
# open the the we would like to merge:2014 and 2018
# there was a law change in Hungary in 2012 regarding the elections
# source and information about the elections: https://en.wikipedia.org/wiki/2014_Hungarian_parliamentary_election
# soource for the variables  (origin:2002!!):https://static.valasztas.hu/parval2002/esz/esz_hu/informaciok_ind.htm
# here:fogalmak or rövidítések jegyzéke (definitons or abbreviations)
# for english version, you can find some defintions here: (again: these definitions were defnied in 2002, did not find others)
# https://static.valasztas.hu/parval2002/esz/esz_hu/informaciok_ind.htm
# https://static.valasztas.hu/parval2006/hu/17/fogalmak/fogalmak1.html
 
election_2014_szavazokor=pd.read_excel(io='Egyéni-szavazás-jkv.xlsx', sheet_name='Sheet1',na_filter=False)

#change folder
os.chdir('C:\\Users\\Attila\\Desktop\\arieda\\valasztasi_eredmenyek_1990-2019\\2018_parlamenti')

election_2018_szavazokor=pd.read_excel(io='Egyéni_szavazás_szkjkv.xlsx', sheet_name='Munka1',na_filter=False)

# we need to remain the columns but first lets check whether the columns name are the same in the two files

columns_name_2018=election_2018_szavazokor.columns.values.tolist()
columns_name_2014=election_2014_szavazokor.columns.values.tolist()
#save the columns name as an xls file and descrie them
columns_name=pd.DataFrame(columns_name_2018,columns=["Name of the variables"])
columns_name.to_excel("decription_of_the_variables.xlsx")

if columns_name_2018 == columns_name_2014:
    print ("The lists are identical")
else :
    print ("The lists are not identical")

#yes the lists are identical so we can just concatenate them but first lets rename the columns
list_of_names=["voting_area_id","JKV_id","individual","county_code","county","OEVK","chief_town_of_the_county","SZH_KER",
               "settlement_serial_number","settlement","voting_area",
               "number_of_registered_voters","appeared_voters","votes_in_the_urn","diff_between_appeared_urn",
               "invalid","valid","candidate","party","votes"]

    
election_2014_szavazokor.columns=list_of_names
election_2018_szavazokor.columns=list_of_names
# add an additional identifier for each of the groups
election_2014_szavazokor["year"]=2014
election_2018_szavazokor["year"]=2018

election_2014_2018_joined = pd.concat([election_2014_szavazokor, election_2018_szavazokor])
#it takes time to save it as an excel
election_2014_2018_joined .to_excel("election_2014_2018_joined.xlsx")

