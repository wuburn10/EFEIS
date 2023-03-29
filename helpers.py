import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.select import Select

def findClick(driver,name,n=False,wait=False):
    if n:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, name))
        )
    else:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, name))
        )
    if wait:
        time.sleep(0.5)
    element.click()

def clickSend(driver,name,data,wait=False):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, name))
    )
    if wait:
        time.sleep(0.5)
    element.clear()
    element.send_keys(data.strip())

def clickSelect(driver,name,data,wait=False):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, name))
    )
    if wait:
        time.sleep(0.5)
    Select(element).select_by_value(data)

def details(sn):
    m = sn[:2].upper()
    switch = {
        'AV': '1',
        'EE': '2',
        'FF': '3',
        'FM': '4',
        'GP': '10',
        'HN': '9',
        'PW': '8',
        'SR': '5',
        'UB': '6',
        'UF': '7'
    }
    if sn[8].upper() == 'Z':
        t, w, r = '2', '2', '9' 
    else:
        t, w, r = '1', '9', '5'  
    
    return switch[m], sn[2:4], sn[4:8], t, sn[9:], w, r
