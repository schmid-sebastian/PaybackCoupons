from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Activator:
    
    def __init__(self, browser, login_style, username, password):
        self.browser = browser
        self.login_style = login_style
        self.username = username
        self.password = password
        
    def activate_coupons(self):
        driver = self.load_driver()
        self.login(driver)
        coupon = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "eCoupons")))
        coupon.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "col-xs-11 teaser js-coupon-teaser margin-left-xs-2 clickable not-activated")))
        coupons = driver.find_elements_by_class_name("col-xs-11 teaser js-coupon-teaser margin-left-xs-2 clickable not-activated")
        for i in coupons:
            attribute = i.get_attribute('data-shop-url')
            if attribute == '':
                i.click()
        
    def load_driver(self):
        if self.browser == "Edge":
            driver = webdriver.Edge()
        elif self.browser == "Chrome":
            driver = webdriver.Chrome()
        elif self.browser == "Firefox":
            driver = webdriver.Firefox()
        else:
            print("Only Edge, Chrome and Firefox supported.")
        return driver
    
    def login(self, driver):
        driver.get("https://www.payback.de")
        login = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Login")))
        login.click()
        self.enter_credentials(driver)
        loginbtn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginSubmitButtonSecure")))
        loginbtn.click()
        
    def enter_credentials(self, driver):
        if self.login_style == "password":
            name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "aliasInputSecure")))
            pwd  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "passwordInput")))
            name.send_keys(self.username)
            pwd.send_keys(self.password)
            return None
        elif self.login_style == "pin":
            pass
        elif self.login_style == "plz":
            pass
        else:
            print("when instantiating the object set login_style as password, pin or plz")
