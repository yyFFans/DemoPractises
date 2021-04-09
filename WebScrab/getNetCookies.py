# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def safeClickElemnt(driver, type, elem):
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located(
        (type, elem)))
    driver.find_element(type, elem).click()

def safeSendkeys(driver, type, elem, keys):
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located(
        (type, elem)))
    driver.find_element(type, elem).send_keys(keys)

driver = webdriver.Chrome()
driver.get("https://www.shiyanlou.com/")
safeClickElemnt(driver, By.LINK_TEXT, "登录")

# 4 | click | id=__BVID__365 |  |
safeClickElemnt(driver, By.XPATH, "//div/input")
# 6 | type | id=__BVID__365 | thyy529205430@126.com |
safeSendkeys(driver, By.XPATH, "//div/input", "thyy529205430@126.com")

# 7 | click | id=__BVID__366 |  |
safeClickElemnt(driver, By.XPATH, "//div[2]/input")

# 8 | type | id=__BVID__366 | thyy4831997 |
safeSendkeys(driver, By.XPATH, "//div[2]/input", "thyy4831997")

# 13 | click | xpath=//button[contains(.,'进入实验楼')] |  |
safeClickElemnt(driver, By.XPATH, "//button[contains(.,\'进入实验楼\')]")

WebDriverWait(driver,5)
time.sleep(50)
cookies = driver.get_cookies()
print(type(cookies))
print(cookies)

# print ("".join(cookies))
f = open('shiyanloucookie.txt', 'w')
f.write(json.dumps(cookies))
f.close()

WebDriverWait(driver, 10)
