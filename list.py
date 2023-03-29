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

driver.get("https://efeis1.bomba.gov.my/new/tbl_apalist.php")

n = 1

csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    for i in number_reader:
        print(f"{n}) Doing {i[0]} ...")

        # Check if csv includes level
        try:
            if i[2].upper() == 'G':
                level = 'GROUND FLOOR'
            else:
                level = 'FLOOR ' + i[2]
        except:
            pass

        # First in List Search
        if n == 1:
            # Search Button
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"ewContentColumn\"]/div[1]/div[2]/div/button"))
                )
                element.click()
            except:
                input("Error1: Search Button")
                driver.quit()

        # Search Input (serial number)
        try:
            clickSend(driver,"x_Serial_Number",i[0],True)
            submit = driver.find_element_by_id("btnsubmit")
            submit.click()
        except:
            input("Error2: Search Input")
            driver.quit()
        
        # Check how many results given
        record = driver.find_element_by_xpath("//*[@id=\"ewContentColumn\"]/div[3]/div/form/div[2]/span").text
        if int(record[18:]) != 1:
            # TODO : SEARCH THE ACTUAL COMPLETE SN FROM TABLE
            # Check for no results
            r = 1
            # 'r'+ r + '_tbl_apa'
            print("Many Results")

        # Get Serial number's ID
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "el1_tbl_apa_ID"))
        )

        driver.get("https://efeis1.bomba.gov.my/new/tbl_apaedit.php?ID=" + element.text)

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
            if i[1].strip().upper() == driver.find_element_by_xpath('/html/body/p/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[' + str(r) + ']/td[3]').text.strip() :
                roomId = driver.find_element_by_xpath('/html/body/p/table/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[' + str(r) + ']/td[2]').text
                found = True
            r += 1

        # Switching window
        driver.execute_script("window.close()")
        driver.switch_to_window(driver.window_handles[0])

        # Entering Location ID
        clickSend(driver,'locid',roomId)
        findClick(driver,'btn',True)
        alert.accept()
        findClick(driver,'btnAction',False,True)



        n += 1
        



input("Done")