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

def login(driver):
    # Access main login page. 
    try:
        driver.get(PECO_LOGIN_URL)
        debug('Opened login page successfully')
    except Exception as err:
        error('Unable to open login page. Exiting.')
        error(err)
        driver.save_screenshot('screenshots/error-opening-login.png')
        exit
    return driver
    # Username Input
    try:
        username = driver.find_elements_by_css_selector('#Username')[1]
        
        username.clear()
        username.send_keys(PECO_USERNAME)
        debug('input username successfully')
    except Exception as err:
        error('Error inputting username in.')
        error(err)
        error('screenshot of page saved')
        driver.save_screenshot("screenshots/username-error.png")
        exit

driver = browser()
info('Chrome driver initialized. Attempting Login')



# Username


# Password
try:
    #password = driver.find_element_by_css_selector('input[type=password')
    password = driver.find_element_by_xpath('//*[@id="SignInController"]/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/div[2]/div/div/input')
    password.clear()
    password.send_keys(PECO_PASSWORD)
    driver.save_screenshot("screenshots/password-input.png")
    debug('input password successfully')
except Exception as err:
    error('Error inputting password.')
    error(err)
    error('screenshot of page saved')

    driver.save_screenshot("screenshots/password-error.png")
    exit
        
signin = driver.find_element_by_xpath('//*[@id="SignInController"]/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button')
signin.click()
driver.save_screenshot("screenshots/submitted.png")
time.sleep(2)
info("Submitted login") 

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