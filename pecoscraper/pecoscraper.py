from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary  # Adds chromedriver binary to path
#from dateutil.parser import parse
#from influxdb import InfluxDBClient
import json
from utils.logger import info, error, debug
from helpers import api_url, get_uuid
import time
import os


PECO_LOGIN_URL = os.environ.get('PECO_LOGIN_URL')
PECO_USERNAME = os.environ.get('PECO_USERNAME')
PECO_PASSWORD = os.environ.get('PECO_PASSWORD')


def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless') 
    caps = DesiredCapabilities.CHROME
    caps['logPrefs'] = {'performance': 'ALL','enable_network': 'true'}
    return webdriver.Chrome(options = chrome_options, desired_capabilities=caps) 

def find_inputs(driver,name):
    for input in driver.find_elements_by_tag_name('input'):
        if input.get_property('name') == name:
            return input
            pass

def login(driver):
    # Access main login page. 
    driver.get(PECO_LOGIN_URL)
    if driver.title == 'Login | PECO - An Exelon Company':
        info('Opened Peco Login page')
    else:
        error('Unknown problem opening login page. Screenshot saved. Exiting')
        driver.save_screenshot('screenshots/error-opening-login.png')
        exit
    # Username Input
    try:
        username = find_inputs(driver,'Username')
    except NoSuchElementException:
        error("Username Element doesn't exist. Exiting")
        driver.save_screenshot("screenshots/username-error.png")
        exit
    username.clear()
    username.send_keys(PECO_USERNAME)
    input('input username successfully')

    # Password
    try:
        password = find_inputs(driver,'Password')
    except NoSuchElementException:
        error("Password Element doesn't exist. Exiting")
        driver.save_screenshot("screenshots/password-error.png")
        exit
    password.clear()
    password.send_keys(PECO_PASSWORD)

    # Click Signin 
    signin = driver.find_element_by_xpath('//*[@id="SignInController"]/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button')
    signin.click()
    driver.save_screenshot("screenshots/submitted.png")
    time.sleep(2)
    info("Submitted login") 

    return driver
    

driver = browser()
info('Chrome driver initialized. Attempting Login')
driver = login(driver)

driver.save_screenshot("screenshots/login-submitted.png")
driver.get('https://secure.peco.com/MyAccount/MyBillUsage/pages/secure/ViewMyUsage.aspx') # for some reason session doesn't initiate until this page.
info("Gaining session cookies") 
time.sleep(2)
driver.save_screenshot("screenshots/get-usage-page.png")
iframe = driver.find_element_by_tag_name('iframe')
usage_src = iframe.get_property('src')
driver.get(usage_src)
time.sleep(2)
options = driver.find_elements_by_tag_name('option')
account_id = ''
for element in options:
    if element.get_property('label') == 'Electricity':
        account_id = element.get_property('value')
account_id = get_uuid(account_id)
driver.get(api_url(account_id))
data = driver.find_elements_by_xpath("//pre")[0].text
driver.quit()
usage = json.loads(data)
usage = usage['reads']
print(usage)