from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_binary  # Adds chromedriver binary to path
#from dateutil.parser import parse
#from influxdb import InfluxDBClient
import json
from utils.logger import info, error, debug
from helpers import api_url, get_uuid, usage_urls
from signin import login
from account import get_account_id
import time


def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    caps = DesiredCapabilities.CHROME
    caps['logPrefs'] = {'performance': 'ALL', 'enable_network': 'true'}
    return webdriver.Chrome(options=chrome_options, desired_capabilities=caps)


driver = browser()
info('Chrome driver initialized. Attempting Login')
driver = login(driver)
time.sleep(1)
# for some reason session doesn't initiate until this page.
driver.get(
    'https://secure.peco.com/MyAccount/MyBillUsage/pages/secure/ViewMyUsage.aspx')
info("Opening My usage homepage. Need to in order to achieve valid session")
time.sleep(2)
account_id = get_account_id(driver)
driver.get(api_url(account_id))
data = driver.find_elements_by_xpath("//pre")[0].text
driver.quit()
usage = json.loads(data)
usage = usage['reads']


print(usage)
