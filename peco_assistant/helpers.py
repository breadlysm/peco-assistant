import pytz
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium import webdriver
from datetime import datetime, date, timedelta
from pytz import timezone,utc
import time

#import chromedriver_binary
import os


tz = timezone('US/Eastern')
class Browser:

    def __init__(self):
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
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

def to_utc(dt,current_tz=eastern()):
    dt = current_tz.localize(dt, is_dst=None)
    dt = dt.astimezone(utc)
    return dt

def date_to_dt(date):
    "


def get_today():
    today = datetime.now().isoformat()
    return today

def day(timestamp):
    return timestamp.strftime("%d")

def month(timestamp):
    return timestamp.strftime("%m")


def month_name(dt):
    return dt.strftime("%b")


def year(timestamp):
    return timestamp.strftime("%Y")

def add_days(dt,days):
    return dt + timedelta(days=days)

def sub_days(dt,days):
    return dt - timedelta(days=days)

def peco_date(dt):
    return dt.astimezone(eastern()).strftime("%Y/%-m/%d")

def peco_dates(start,end=datetime.now(utc)):
    """"returns list of days to get metrics for in peco accepted format
    Args:
        start (datetime): where list of dates should start, must be utc
        end (datetime, optional): UTC datetime on end of range. Defaults to datetime.now(utc).
    """
    day = start
    days = []
    while day < end:
        days.append(peco_date(day))
        day = add_days(day,1)
    return days


def two_years():
    return datetime.now(utc) - timedelta(days=2*365)


def date_to_dt(date, fmt='%m/%d/%Y'):
    return datetime.strptime(date,fmt)


def pdf_file_names(dates):
    paths = []
    for day in dates:
        dt = date_to_dt(day)
        y = year(dt)
        m = month_name(dt)
        path = f'peco_assistant/data/invoices/{y}/Peco {m}-{y} Invoice.pdf'
        paths.append(path)
    return paths


def check_if_exists(pdfs,path='peco_assistant/data/invoices'):
    to_get_pdfs = []
    existing_pdfs = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.pdf'))]
    for row in pdfs:
        if not row in existing_pdfs:
            to_get_pdfs.append(row)
    return to_get_pdfs
