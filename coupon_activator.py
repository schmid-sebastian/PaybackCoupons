from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Activator:
    """Payback eCoupons are a nice way to collect more payback points (=money!). 
    However, for them to be active, you need to login regularly and activate them 
    one by one. By doing so, you come in contact with the marketing campaign 
    connected to the eCoupon, which in turn might affect your shopping behaviour.
    This library aims to automate the eCoupon activation process so you can 
    collect more payback points without the drawback of being manipulated. 
    
    Attributes:
        - browser: "Edge", "Chrome", or "Firefox". This is going the be the browser
                   that will be used when automating. More browsers will be added.
        - login_style: "password", "pin" or "plz". Your way of logging into your
                   payback account. 
        - username: provide your username like "kundennummer" or "mail@mail.de".
        - password: provide your password like "12345". ATTENTION: When using
                   "plz" as your login_style, please provide your date of birth
                   and plz in the following format: "DD/MM/YYYY/PLZ"
    """
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
            switch = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "toggleSecureLogin")))
            switch.click()
            switch = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "tabclassicLoginPin")))
            switch.click()
            name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cardnumberInputClassicPin")))
            pwd  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "pinInput")))
            name.send_keys(self.username)
            pwd.send_keys(self.password)
        elif self.login_style == "plz":
            switch = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "toggleSecureLogin")))
            switch.click()
            day, month, year, plz = self.credentials_plz()
            name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cardnumberInputClassicDobZip")))
            dob = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dob")))
            dob.click()
            dayfield = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dobDayName")))
            monthfield = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dobMonthName")))
            yearfield = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dobYearName")))
            plzfield = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "zipName")))
            name.send_keys(self.username)
            dayfield.send_keys(day)
            monthfield.send_keys(month)
            yearfield.send_keys(year)
            plzfield.send_keys(plz)
        else:
            print("when instantiating the object set login_style as password, pin or plz")
            
    def credentials_plz(self):
        pwd = self.password
        pwd = pwd.split("/")
        day = pwd[0]
        month = pwd[1]
        year = pwd[2]
        plz = pwd[3]
        return day, month, year, plz
