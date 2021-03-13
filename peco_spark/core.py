from peco_spark.helpers import Browser, eastern, peco_dates,to_datetime,log, two_years
from peco_spark.database import Database
#from utils.logger import info, error, debug
import json
import time
import os
from peco_spark.config import get_config

  # Adds chromedriver binary to path

#from utils.dates import date_string
config = get_config()
class Account:

    def __init__(self):
        self.browser = Browser()
        self.driver = self.browser.driver
        self.username = config['peco']['user']
        self.password = config['peco']['pass']
        self.login()
        self._kwh_cost = None
        self.kwh_cost = self.get_kwh_cost()
        


    def login(self):
        self.browser.get('https://secure.peco.com/accounts/login')
        email = self.browser.get_element_at_xpath("//input[@aria-label='Email']")
        email.send_keys(self.username)
        password = self.browser.get_element_at_xpath("//input[@aria-label='Password']")
        password.send_keys(self.password)
        submit = self.browser.get_element_at_xpath("//*/button[@class='btn btn-primary fixed-width']")
        submit.click()

    def get_data(self,date):
        """Retrieves power usage data and weather data from your Peco Account. 
        Args:
            date (str): date in the format "2001/2/20"
        Returns:
            dict: dictionary by hour of the day with temperate and usage integers
        """
        try:
            url = F"https://peco.opower.com/ei/app/myEnergyUse/weather/day/{date}"
            self.driver.get(url)
            usage = self.driver.execute_script('return window.seriesDTO')['series'][0]['data']
            weather = self.driver.execute_script('return window.weatherDTO')['series'][0]['data']
            data = self.clean_data(usage,weather)
            if data is None:
                raise Exception(F"No values found for {date}")
        except:
            data = None
        return data
    
    def calc_cost(self,kwh):
        cost = self.kwh_cost * kwh
        return cost

    def clean_data(self,usage,weather):
        data = []
        try:
            for hour in range(len(weather)):
                row = {'startDate':to_datetime(weather[hour]['startDate'],local_tz=eastern()),
                    'endDate':to_datetime(weather[hour]['endDate'],local_tz=eastern()),
                    'temperature':weather[hour]['value'],
                    'kwh':usage[hour]['value'],
                    'usage_cost': self.calc_cost(usage[hour]['value']),
                    'current_price': self.kwh_cost}
                data.append(row)
            return data
        except IndexError as err:
            log.error(F"No values available for {weather['hour']['startDate']}")
            return None

    def get_kwh_cost(self):
        xpath = '//*[@id="ctl00_PlaceHolderMain_ctl14__ControlWrapper_RichHtmlField"]/table/tbody/tr[3]/td[2]/div'
        self.driver.get("https://www.peco.com/MyAccount/MyService/Pages/ElectricPricetoCompare.aspx")
        cost = self.browser.get_element_at_xpath(xpath)
        cost = cost.text
        cost = cost.strip("$")
        cost = float(cost)
        self._kwh_cost = cost
        return self._kwh_cost

def main():
    run = True
    account = Account()
    db = Database()
    last_write = two_years()
    while run:
        start_date = db.last_write or two_years()
        if last_write < start_date:
            log.debug("The last data written is over 1 day old, starting update")
            dates = peco_dates(start_date)
            data = []
            for day in dates:
                usage = account.get_data(day)
                usage = db.influx_format(usage)
                data = data + usage
            last_write = start_date
            log.info("Usage succesfully collected. Sleeping for 6 hours")
        else: 
            log.info("No update needed. Sleeping for 6 hours")
            
        time.sleep(21600)

if __name__ == '__main__':
    main()

