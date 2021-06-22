import pytz
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from seleniumwire import webdriver
from datetime import datetime, date, timedelta
from selenium.webdriver import DesiredCapabilities
from pytz import timezone,utc
import time
from base64 import b64decode, b64encode
from glob import glob

#import chromedriver_binary
import os


tz = timezone('US/Eastern')
class Browser:

    def __init__(self):
        self._driver = None
        
    def options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        print('chrome options loaded')
        return chrome_options
    
    def scopes(self):
        scopes = [
            'https:\/\/secure.peco.com\/.euapi\/mobile\/custom\/auth\/accounts\/[0-9]*\/billing\/[0-9]{4}-[0-9]{2}-[0-9]{2}\/pdf'
        ]
        return scopes

    @property
    def driver(self):
        if self._driver is None:
            options = self.options()
            scopes = self.scopes()
            self._driver = webdriver.Chrome(options=options)
            self._driver.scopes = scopes
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


def get_today():
    today = datetime.now().isoformat()
    return today

def to_unix(dt):
    return datetime.timestamp(dt)

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

def to_pdf_date(dt):
    return dt.strftime("%Y-%m-%d")

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
        main_path = 'peco_assistant/data/invoices'
        path = f'{main_path}/{y}/Peco {m}-{y} Invoice.pdf'
        data = (dt, path)
        paths.append((dt, path))
        year_folder = os.path.isdir(f'{main_path}/{y}')
        if not year_folder:
            os.makedirs(f'{main_path}/{y}')
    paths = check_if_exists(paths)
    return paths

def local_pdfs(path='peco_assistant/data/invoices'):
    pdfs = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.pdf'))]
    return pdfs


def check_if_exists(pdfs, path='peco_assistant/data/invoices'):
    to_get_pdfs = []
    existing_pdfs = local_pdfs(path)
    for row in pdfs:
        dt = row[0]
        path = row[1]
        if not path in existing_pdfs:
            to_get_pdfs.append((dt, path))
    return to_get_pdfs


def b64_to_pdf(b64, path):
    bytes = b64decode(b64, validate=True)

    # Write the PDF contents to a local file
    f = open(path, 'wb')
    f.write(bytes)
    f.close()


def pdf_to_b64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_string = b64encode(pdf_file.read())
    pdf_string = pdf_string.decode('utf-8')
    #pdf_string = pdf_string
    # Write the PDF contents to a local file
    return pdf_string

def parse_pdf(pdf_path):
    templates = read_templates('peco_assistant/data/templates')
    results = extract_data(pdf_path, templates=templates)
    return results