from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium import webdriver
from datetime import datetime, date
import time
import chromedriver_binary
import os

class Browser:

    def __init__(self):
        self.driver = self.get_driver()
        self._driver = None

    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self._driver = webdriver.Chrome(options=chrome_options)
        return self._driver
    
    def get(self,url):
        return self.driver.get(url)

    def wait_for_xpath(self,element):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, element)))
        finally:
            return self.driver.find_element_by_xpath(element)
    
    def get_element_at_xpath(self,xpath):
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException as err:
            time.sleep(2)
            try:  
                element = self.driver.find_element_by_xpath(xpath)
            except NoSuchElementException as err:
                try:
                    element = self.wait_for_xpath(xpath)
                except Exception as err:
                    element = None
        return element



def day(timestamp):
    return timestamp.strftime("%d")

def month(timestamp):
    return timestamp.strftime("%m")

def year(timestamp):
    return timestamp.strftime("%Y")

def peco_date(timestamp):
    return timestamp.strftime("%Y/%m/%d")