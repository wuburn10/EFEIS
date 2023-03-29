from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import csv
import sys

# Get csv file name from command line
if len(sys.argv) != 2:
    input("Usage : python python_file.py csv_file.csv")
    exit()

failed = []
successed = []
fail = 0
success = 0

# Reading serial number into memory first
sn = []
csv_file = "csv/" + sys.argv[1]
with open(csv_file, newline="") as file:
    number_reader = csv.reader(file)
    for i in number_reader:
        sn.append(i[0].strip())

l = len(sn)
print(l)
if l != len(set(sn)):
    input("Duplicated serial numbers!")
    exit()
else:
    print("All Good!")

# Open Efeis
driver = webdriver.Chrome("D:\Program Files (x86)\chromedriver.exe")

driver.get("https://efeis1.bomba.gov.my/portal/index.php")

email = driver.find_element_by_id("bemail")
password = driver.find_element_by_id("bpswd")
submit = driver.find_element_by_id("submit")

# Log In
email.send_keys("reginald")
password.send_keys("genesis9891")

submit.click()

# Transfer APA
driver.get('https://efeis1.bomba.gov.my/apa_endorse.php')

current = 1
for i in sn:
    apaid = driver.find_element_by_id('apaid')
    apaid.clear()
    apaid.send_keys(i)

    submit = driver.find_element_by_name('button')
    submit.click()


    a = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/span").text

    if not(a) :
        print(f"Failed  : Serial Number '{i}' Does Not Exist")
        fail += 1
        failed.append(f"no.{current} Failed  : Serial Number '{i}' Does Not Exist")
    else :
        try:
            transfer = driver.find_element_by_id('button2')
            transfer.click()

            print(f"{current:.2f}) Success : Serial Number '{i}' Entered")
            success += 1
            successed.append(i)
        except :
            print(f"{current:.2f}) Failed  : Serial Number '{i}' Not Expired Yet")
            fail += 1
            failed.append(f"no.{current} Failed  : Serial Number '{i}' Not Expired Yet")
    current += 1
    time.sleep(1)

# Stats
print("\n===== DONE =====")
print(f"SUCCESS : {success}/{l}")
i = 1
for s in successed :
    print(f"    {i}) {s}") 
    i += 1
print(f"FAILED : {fail}/{l}")

i = 1
for f in failed :
    print(f"    {i}) {f}") 
    i += 1

input('Done. ')


driver.quit()