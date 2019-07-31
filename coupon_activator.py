from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Edge()

driver.get('https://www.payback.de')
ec.presence_of_element_located((By.LINK_TEXT, "Login"))
login = driver.find_element_by_link_text("Login")
login.click()
time.sleep(5)
name = driver.find_element_by_id("aliasInputSecure")
pwd = driver.find_element_by_id("passwordInput")
login = driver.find_element_by_id("loginSubmitButtonSecure")
name.send_keys("")
pwd.send_keys("")
login.click()
time.sleep(5)
link = driver.find_element_by_link_text("eCoupons")
link.click()
time.sleep(10)
coupons = driver.find_elements_by_class_name("col-xs-11 teaser js-coupon-teaser margin-left-xs-2 clickable not-activated")
for i in coupons:
    attribute = i.get_attribute('data-shop-url')
    if attribute == '':
        i.click()
