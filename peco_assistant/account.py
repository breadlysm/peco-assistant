from peco_assistant.helpers import Browser, eastern, peco_dates,to_datetime,log, two_years

class Account:

    def __init__(self, config):
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
        log.debug("Logged in to account.")

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
            log.info(F"No values available for {weather['hour']['startDate']}")
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
