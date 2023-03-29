import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.select import Select
from helpers import *

try :
    if sys.argv[2].upper() == "OLD":
        stat = 'Renewed'
except :
    stat = 'NEW'

with open("csv/address.csv") as add:
    read = csv.reader(add, delimiter=',')
    for j in read:
        level = j[0]
        block = j[1]
        unitNo = j[2]
        lotNo = j[3]
        state = j[4]
        street = j[5]
        building = j[6]
        locality = j[7]
        city = j[8]
        postcode = j[9]
        break

driver = webdriver.Chrome("D:\Program Files (x86)\chromedriver.exe")

driver.get("https://efeis1.bomba.gov.my/portal/index.php")

clickSend(driver, 'bemail', 'reginald')
clickSend(driver, 'bpswd', 'genesis9891') 

findClick(driver, 'submit')

driver.get("https://efeis1.bomba.gov.my/new/tbl_apaadd.php")

n = 1

csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    for i in number_reader:
        if n != 1:
            driver.get("https://efeis1.bomba.gov.my/new/tbl_apaadd.php")

        print(f'{n}) Doing {i[0]}')
        manufacturer, month, year, apaType, number, weight, rating= details(i[0])
        # Serial Number
        clickSend(driver,'x_Serial_Number',number)
        # APA Status
        clickSelect(driver,'x_APA_Status',stat)
        # APA Type
        clickSelect(driver,'x_Apa_Type',apaType)
        # Manufacturer
        clickSelect(driver,'x_Manuacturer',manufacturer)
        # Weight
        clickSend(driver,'x_Weight', weight)
        # Rating
        clickSelect(driver,'x_Rating',rating)
        # Month
        clickSelect(driver,'x_Manufacturing_Month', month)
        # Year
        clickSelect(driver,'x_Year_Of_Manufacturing', year)

        # Add new location (open new window)
        driver.execute_script("window.open('https://efeis1.bomba.gov.my/v2/c_ref_location2.php','_blank')")

        driver.switch_to_window(driver.window_handles[1])

        # Room *
        clickSend(driver,"tbl_ref_locations1Room",i[1])
        # Level
        clickSend(driver,"tbl_ref_locations1Level",level)
        # Block
        if block:
            clickSend(driver,"tbl_ref_locations1Block",block)
        # Unit No
        clickSend(driver,"tbl_ref_locations1Lot",unitNo)
        # Lot no*
        if lotNo:
            clickSend(driver,"tbl_ref_locations1Building_No",lotNo)
        # State*
        if state.upper() == "SEL":
            clickSelect(driver,"tbl_ref_locations1State","6")
        elif state.upper() == "KL":
            clickSelect(driver,"tbl_ref_locations1State","2")
        # Road/Street*
        clickSend(driver,"tbl_ref_locations1Location",street)
        # Building name
        if building:
            clickSend(driver,"tbl_ref_locations1Building_Name",building)
        # Locality*
        clickSend(driver,"tbl_ref_locations1Address",locality)
        # City*
        clickSelect(driver,"tbl_ref_locations1City",city)
        # Postcode*
        clickSend(driver,"tbl_ref_locations1Postcode",postcode)

        # Submit
        findClick(driver,'tbl_ref_locations1Button_Insert')

        alert = driver.switch_to.alert
        alert.accept()

        # Find ID
        r = 2
        found = False
        while not(found):
            if i[1].upper() == driver.find_element_by_xpath('/html/body/p/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr['+ str(r) + ']/td[3]').text.strip() :
                roomId = driver.find_element_by_xpath('/html/body/p/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr['+ str(r) +']/td[2]').text
                found = True
            r += 1

        # Switching window
        driver.execute_script("window.close()")
        driver.switch_to_window(driver.window_handles[0])

        # Entering Location ID
        clickSend(driver,'locid',roomId)
        findClick(driver,'btn',True)
        alert.accept()

        input("Next? ")

        #Submit
        findClick(driver,'btnAction')

        n += 1
        