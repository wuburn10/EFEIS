import csv
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.select import Select

'''
if input("Manual? (y/n)") == "y":
    manual = True
else:
    manual = False 
'''

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

driver.get("https://efeis1.bomba.gov.my/new/tbl_apaadd.php")

csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    n = 1
    for i in number_reader:
        print(f"{n}) Doing {i[0]} ...")
        n += 1

        s = driver.find_element_by_id("view_apa_not_booked_list_SearchImage")
        s.click()

        serial = driver.find_element_by_id("x_Serial_Number")
        serial.clear()
        serial.send_keys(i[0])

        submit = driver.find_element_by_id("Submit")
        submit.click()

        select = driver.find_element_by_name("input")
        select.click()

        #input("Press ENTER to continue. ")
        time.sleep(1)


input("Done")