from .helpers import Browser
#from utils.logger import info, error, debug
import json
import time
import os

  # Adds chromedriver binary to path

#from utils.dates import date_string

class Account:

    def __init__(self):
        self.driver = None
        self.browser = Browser()
        self.account_id = None
        self.username = os.environ.get('PECO_USERNAME')
        self.password = os.environ.get('PECO_PASSWORD')
        self.get_driver()
        self.login()
        self.data = self.get_data()
        self._data = None

    def login(self):
        self.browser.get('https://secure.peco.com/accounts/login')
        email = self.browser.get_element_at_xpath("//input[@aria-label='Email']")
        email.send_keys(self.username)
        password = self.browser.get_element_at_xpath("//input[@aria-label='Password']")
        password.send_keys(self.password)
        submit = self.browser.get_element_at_xpath("//*/button[@class='btn btn-primary fixed-width']")
        submit.click()

    def get_data(self):
        # url = F"https://peco.opower.com/ei/app/myEnergyUse/weather/day/2021/2/20"
        # self.driver.get(url)
        # usage = self.driver.execute_script('return window.seriesDTO')['series'][0]['data']
        # weather = self.driver.execute_script('return window.weatherDTO')['series'][0]['data']
        # data = self.clean_data(usage,weather)
        # self._data = data
        # return self._data
        return Browser()
    
    def clean_data(self,usage,weather):
        data = []
        for hour in range(len(weather)):
            row = {'startDate':weather[hour]['startDate'],
                'endDate':weather[hour]['endDate'],
                'temperature':weather[hour]['value'],
                'kwh':usage[hour]['value']}
            data.append(row)
        return data
