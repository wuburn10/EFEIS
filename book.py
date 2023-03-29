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

# Open Efeis
driver = webdriver.Chrome("D:\Program Files (x86)\chromedriver.exe")

driver.get("https://efeis1.bomba.gov.my/portal/index.php")


# Log In
clickSend(driver, "bemail", "reginald")
clickSend(driver, "bpswd", "genesis9891")
findClick(driver, "submit")

try :
    if sys.argv[2].upper() == "NEW":
        # New
        driver.get("https://efeis1.bomba.gov.my/view_apa_not_bookedlist.php?nav=0&tp=1")
    elif sys.argv[2].upper() == 'GOV':
        # Government
        driver.get("https://efeis1.bomba.gov.my/view_apa_not_bookedlist.php?nav=0&tp=4")   
except:
    # Renew
    driver.get("https://efeis1.bomba.gov.my/view_apa_not_bookedlist.php?nav=0&tp=2")

csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    n = 1
    for i in number_reader:
        # Stop if reach more than 30
        if n == 31:
            input("Finish 30 pcs.")
            break
        print(f"{n}) Doing {i[0]} ...")
        n += 1

        # Search serial number
        findClick(driver,"view_apa_not_booked_list_SearchImage")
        clickSend(driver, "x_Serial_Number",i[0])
        findClick(driver,"Submit")

        # Check if more than 1 result is returned
        try:
            extra = driver.find_element_by_id("view_apa_not_booked_list_row_2")
            input("There is an extra serial number result. Select the right one and press ENTER.")
            # TODO: Pick most accurate OR pause and wait for user input
            # while sn != row sn:
        except:
            findClick(driver, "input", True)


# Select State and Zone
clickSelect(driver,"state","15")
time.sleep(1)
clickSelect(driver,"zone","101")

# Book Batch
findClick(driver,"createb")
input("Create?")
findClick(driver,"addb2")