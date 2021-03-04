import pytz
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium import webdriver
from datetime import datetime, date
from pytz import timezone,utc
import time
import logging
import sys
import chromedriver_binary
import os

tz = timezone('US/Eastern')

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

def to_datetime(str,tz=utc,local_tz=None,fmt="%a, %d %b %Y %H:%M:%S"):
    """Returns datetime object from string

    Args:
        str (str): string representing a time, needs to be in valid format
        tz (timezone, optional): pytz timezone obj to convert to. Defaults to None.
        local_tz (timezone, optional): pytz tz obj string is in. Defaults to None
        fmt (str, optional): Pass format for your str. Defaults to "%a, %d %b %Y %H:%M:%S".
    Returns:
        datetime: returns datetime obj
    """
    dt = datetime.strptime(str,fmt)
    if tz == None or local_tz == None:
        return dt
    else:
        dt = local_tz.localize(dt, is_dst=None)
        dt = dt.astimezone(tz)
        return dt

def eastern():
    return timezone('US/Eastern')


def get_today():
    today = datetime.datetime.now().isoformat()
    return today

def day(timestamp):
    return timestamp.strftime("%d")

def month(timestamp):
    return timestamp.strftime("%m")

def year(timestamp):
    return timestamp.strftime("%Y")

def peco_date(timestamp):
    return timestamp.strftime("%Y/%m/%d")

log_format = "%(asctime)s [%(levelname)s] %(message)s"

def two_years():
    return datetime.datetime.now() - datetime.timedelta(days=2*365)

class Log:
    def info(msg):
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                #logging.FileHandler("log.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info(msg)

    def debug(msg):
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[
                #logging.FileHandler("debug.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        print(msg)
        logging.debug(msg)

    def error(msg):
        logging.basicConfig(
            level=logging.ERROR,
            format=log_format,
            handlers=[
                #logging.FileHandler("log.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.error(msg)
log = Log()

