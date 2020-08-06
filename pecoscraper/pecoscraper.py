from selenium import webdriver
import json
from utils.logger import info, error, debug
from helpers import api_url, get_uuid,hours_to_seconds
from account import get_account_id, login
from export import init_db, influx_write, infux_format, get_data
import time
import os

TEST_INTERVAL = int(os.environ.get('SCRAPE_INTERVAL'))
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

init_db()  # Setup the database if it does not already exist.

while(1): # Run until manually stopped
    driver = browser()
    info('Chrome driver initialized. Attempting Login')
    driver = login(driver)
    # for some reason session doesn't initiate until this page.
    account_id = get_account_id(driver)
    data = get_data(account_id,driver)
    influx_data = infux_format(data)
    influx_write(influx_data)
    
    with open('hourly_usage.txt', 'w') as f:
        for item in influx_data:
            f.write("%s\n" % item)
    time.sleep(hours_to_seconds(TEST_INTERVAL))