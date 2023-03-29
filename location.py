import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.select import Select


# Location Details
block_bool = False
if block_bool:
    block = input("Block : ")
level_bool = False
if level_bool:
    level = input("Level : ")
no = input("Building/Lot No* : ")
state = input("State(sel/kl)* : ")
if state == "sel":
    state = "6"
elif state == "kl":
    state = "2"
else :
    state = input("state value in source code : ")
street = input("Road/Street *: ")
locality = input("Locality *: ")
city = input("City *: ")
postcode = input("Postcode *: ")

failed = []
successed = []
fail = 0
success = 0

# Open Efeis
PATH = "D:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://efeis1.bomba.gov.my/portal/index.php")

email = driver.find_element_by_id("bemail")
password = driver.find_element_by_id("bpswd")
submit = driver.find_element_by_id("submit")

# Log In
email.send_keys("reginald")
password.send_keys("genesis9891")

submit.click()

# APA List
driver.get('https://efeis1.bomba.gov.my/new/tbl_apalist.php')

search = driver.find_element_by_xpath("//*[@id='ewContentColumn']/div[1]/div[2]/div/button")
search.click()
time.sleep(1)

csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    n = 1
    for i in number_reader:
        print(f"{n}) Doing '{i[0]}' + '{i[1]}'")
        n += 1

        serial = driver.find_element_by_id("x_Serial_Number")
        serial.clear()
        serial.send_keys(i[0])
        time.sleep(1)

        submit = driver.find_element_by_id("btnsubmit")
        submit.click()
        time.sleep(1)

        try:
            edit = driver.find_element_by_link_text("Edit")
            edit.click()
            time.sleep(1)
        except:
            fail += 1
            failed.append(i)
            continue

        # Specific page for serial number
        time.sleep(1)
        search_address = driver.find_element_by_link_text("Search Address")
        search_address.click()
        time.sleep(1)

        # Switch to adding address window
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[1])


        if input("Correct address") == "y":

            add = driver.find_element_by_link_text("Add New Address")
            add.click()
            time.sleep(1)

            # room*
            r = driver.find_element_by_id("tbl_ref_locations1Room")
            r.send_keys(i[1])

            #block
            if block_bool:
                blck = driver.find_element_by_id("tbl_ref_locations1Block")
                blck.send_keys(block)

            # level
            if level_bool:
                lvl = driver.find_element_by_id("tbl_ref_locations1Level")
                lvl.send_keys(level)

            # lot no.*
            lot = driver.find_element_by_id("tbl_ref_locations1Building_No")
            lot.send_keys(no)

            # state*
            st = Select(driver.find_element_by_id("tbl_ref_locations1State"))
            st.select_by_value(state)

            # road/street*
            ro = driver.find_element_by_id("tbl_ref_locations1Location")
            ro.send_keys(street)

            # locality*
            loc = driver.find_element_by_id("tbl_ref_locations1Address")
            loc.send_keys(locality)

            # city*
            ci = Select(driver.find_element_by_id("tbl_ref_locations1City"))
            ci.select_by_value(city)

            # postcode*
            pos = driver.find_element_by_id("tbl_ref_locations1Postcode")
            pos.send_keys(postcode)

            submit_add = driver.find_element_by_id("tbl_ref_locations1Button_Insert")
            submit_add.click()

        input("finish.")
        driver.switch_to_window(driver.window_handles[0])
        
# Stats
if failed:
    print("Failed :")
    n = 1
    for i in failed:
        print("    " + i[0] + " -> " + i[1])
        n += 1
else:
    print("Success")
input('done. ')

driver.quit()