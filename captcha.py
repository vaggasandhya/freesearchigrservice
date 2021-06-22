import re
import time, datetime
import os
import sys
from selenium import webdriver                                      
import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
# from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib
import pytesseract
from PIL import Image
import pytesseract as pyt
    

import http.client 
http.client._MAXHEADERS = 10000




# load the websites
url = "https://freesearchigrservice.maharashtra.gov.in/"

import json
with open('config.json') as config_file:
    data = json.load(config_file)
    # print(data)


fp = webdriver.FirefoxProfile()
capabilities = DesiredCapabilities().FIREFOX    
capabilities["marionette"] = True
fp.set_preference("browser.cache.disk.enable", False)
fp.set_preference("browser.cache.memory.enable", False)
fp.set_preference("browser.cache.offline.enable", False)    
fp.set_preference("network.http.use-cache", False) 
# options = Options()
# options.add_argument("-headless")
driver = webdriver.Firefox(desired_capabilities=capabilities, firefox_profile=fp)#, options=options)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

driver.get(url)
time.sleep(5)


def scan(registration_type,district,sro,year,doc_no):

    try:
        driver.find_element_by_xpath('/html/body/center/div/div/a').click() # ad close button
        print("Ad button")
    except:
        print(" no Ad button could not found")
    try:
        driver.find_element_by_xpath('/html/body/center/form/div[3]/div/div/div[1]/div[2]/table/tbody/tr/td[4]/table/tbody/tr/td/a').click() #Document Number
        print("Document Number present")
    except:
        print("no document number")

    #parameter01:finding the radio button
    try:
        time.sleep(2)
        if(registration_type == 'eFiling'):
            print("1")
            registration_type
            driver.find_element_by_xpath('//*[@id="rblDocType_0"]').click()
        elif(registration_type =='eRegistration'):
            driver.find_element_by_xpath('//*[@id="rblDocType_1"]').click()
            print(2)
        elif(registration_type =='Regular'):
            r = driver.find_element_by_xpath('//*[@id="rblDocType_2"]').click()
            print("3")
        print("The Registration type is:",registration_type, type(registration_type))
    except:
        print("please selecte the proper registration types")

    #parameter02: finding the district
    time.sleep(4)
    driver.find_element_by_css_selector('#ddldistrictfordoc').click() # dropdown button
    try:
        time.sleep(4)
        dist_v = driver.find_element_by_xpath("//option[contains(text(),"+'"'+str(district)+'"'+")]")
        dist_v.click()
        print("pune district selected",district)
    except:
        print("no pune district selected")


   #parameter03:finding the sro
    try:
        driver.find_element_by_css_selector('#ddlSROName').click() #SRO Dropdown
        time.sleep(3)
        sro_v = driver.find_element_by_xpath("//option[contains(text(),"+'"'+str(sro)+'"'+")]")
        sro_v.click() #haveli 1
        print("haveli 1 selected")
    except:
        print("no sro selected ")
 
    #parameter04:finding the year
    try:
        driver.find_element_by_css_selector("#ddlYearForDoc").click() 
        time.sleep(3)
        year_v=  driver.find_element_by_xpath("//option[contains(text(),"+year+")]")
        year_v.click()
    except:
        print("no year selected")

    #parameter05:finding the docno
    driver.find_element_by_css_selector('#txtDocumentNo').send_keys(doc_no)

    driver.find_element_by_xpath('//*[@id="TextBox1"]').send_keys("134")
    driver.find_element_by_xpath('//*[@id="btnSearchDoc"]').click()
    time.sleep(3)



    #captch identified
    img= driver.find_element_by_id("imgCaptcha1").screenshot('bimg.png')#.get_screenshot_as_file("screenshot.png")
    # src1 = img.get_attribute('src')
    image_file = r'C:\Users\pichain\Desktop\work\sample\Pune\bimg.png'
    im = Image.open(image_file)
    text = pyt.image_to_string(image_file)
    t = re.sub(r'[^a-zA-Z0-9]', '', text)
    print(t, len(t),type(t))
  
    driver.find_element_by_xpath('//*[@id="TextBox1"]').send_keys(t)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="btnSearchDoc"]').click()

    time.sleep(20)
    # driver.close()

    # table extraction 
    driver.switch_to.window(driver.window_handles[0])
    # r = requests.get(url,verify=False)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reginfo = soup.find('table', class_='table table-responsive')
    print("The extracion of Registrated Details as below:",reginfo)
    from table import TableExtraction
    x = TableExtraction(reginfo)
    return x
    

# passing sample values to scan function
# registration_type = "'Regular'"
# district = "'सातारा'"
# sro = "'Karad 1'"
#scan(registration_type =registration_type,district=district,sro=sro,year=year,doc_no=doc_no)