# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 08:54:18 2022

@author: shawn
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
 
#Get current month and year to add to excel file name
month = datetime.now().strftime('%B')
year = datetime.now().strftime('%Y')
 
#Set url to applicable website
url = 'https://ethanolrfa.org/resources/ethanol-biorefinery-locations'
 
#Open browser instance and give it url address
browser = webdriver.Chrome(r"C:\Temp\ChromeDriver\chromedriver.exe")
browser.get(url)
 
#Find table code on the webpage
locations = browser.find_element_by_css_selector('#locationsTable').get_attribute('outerHTML')
 
#Parse the html code into string
soup = BeautifulSoup(locations, 'html.parser')
 
#Convert the table data into a dataframe to later be exported to excel
dfLocations = pd.read_html(str(soup))[0]
 
#Replaces any dashes with 0's so the columns can be converted into numbers
dfLocations['PROD. CAPACITY (MGY)'] = dfLocations['PROD. CAPACITY (MGY)'].replace({'-':0})
 
#Convert two columns into numeric values
dfLocations['PROD. CAPACITY (MGY)'] = pd.to_numeric(dfLocations['PROD. CAPACITY (MGY)'])
dfLocations['UNDER CONSTR. (MGY)'] = pd.to_numeric(dfLocations['UNDER CONSTR. (MGY)'])
 
#Remove U.S. total row at the bottom to prevent double counting in Tableau
dfLocations = dfLocations.iloc[:-1]
 
#Writes data to an excel file
dfLocations.to_excel(r'C:\Users\shawn\Documents\Python Scripts\Webscraping\Biorefinery Locations ' + month + ' ' + year + '.xlsx', index=False)
 
print('Success')
browser.close()

