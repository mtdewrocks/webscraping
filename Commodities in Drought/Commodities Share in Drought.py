# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:05:10 2022

@author: shawn
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import os
 
#os.chdir(r'C:\Users\shawn\Documents\Python Scripts\Webscraping')
directory = os.getcwd() 

beginningTime = time.time()
 
##Change the file path to where your chromedriver.exe file is
browser = webdriver.Chrome(r'C:\Temp\ChromeDriver\chromedriver.exe')
 
url = 'https://agindrought.unl.edu/Table/TablebyLocation.aspx'
 
browser.get(url)
browser.maximize_window()
 
##Finds the Agriculture type button and selects the option
select = Select(browser.find_element_by_id('location'))
select.select_by_visible_text('CONUS')
select = Select(browser.find_element_by_id('ContentPlaceHolder1_croptype'))

#year = Select(browser.find_element_by_id("yr-all"))
commodities = ["Cattle", "Hogs and Pigs", "Milk Cows"]
data = []

for commodity in commodities:
    select.select_by_visible_text(commodity)
    browser.find_element_by_id('yr-all').click()
 
    table = browser.find_element_by_id('datatab').get_attribute('outerHTML')
    soup = BeautifulSoup(table, 'html.parser')
    dfData = pd.read_html(str(soup))[0]
    dfData['Commodity'] = commodity
    dfData['Geography'] = 'U.S.'
    data.append(dfData)

dfCombined = pd.concat(data)
dfCombined.to_excel(directory+ "\\" + "Commodities Share in Drought.xlsx", index=False)
browser.close()
endingTime = time.time()
 
timeElapsed = endingTime-beginningTime
print(timeElapsed)

