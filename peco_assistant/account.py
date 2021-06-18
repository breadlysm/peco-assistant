from peco_assistant import helpers 
from peco_assistant.config import log

class Account:

    def __init__(self, config):
        self.browser = helpers.Browser()
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
                row = {'startDate':helpers.to_datetime(weather[hour]['startDate'],local_tz=helpers.eastern()),
                    'endDate':helpers.to_datetime(weather[hour]['endDate'],local_tz=helpers.eastern()),
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

    def get_bill_dates(self):
        self.browser.get('https://secure.peco.com/MyAccount/MyBillUsage/Pages/Secure/AccountHistory.aspx')
        timeFrame_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[1]/div/duration-dropdown/div/div/a'
        timeFrame_dropdown = self.browser.get_element_at_xpath(timeFrame_xpath)
        timeFrame_dropdown.click()

        two_year_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[1]/div/duration-dropdown/div/ul/li[4]'
        twoYearOption = self.browser.get_element_at_xpath(two_year_xpath)
        twoYearOption.click()

        bills_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[3]/div/div[1]/ul/li[2]/a'
        billsTab = self.browser.get_element_at_xpath(bills_xpath)
        billsTab.click()

        active_table_xpath = "//*[contains(@class,' active')]//*[contains(@class,'accordion-heading ng-scope')]"
        test = self.browser.wait_for_xpath(active_table_xpath)
        history = self.driver.find_elements_by_xpath(active_table_xpath)

        bills = []
        for element in range(len(history)):
            date = history[element].find_elements_by_xpath("//*[contains(@class,'md-4')]")[element].get_attribute('innerHTML').strip()
            bills.append(date)
        return bills

    def get_pdf_js(self, date):
        js_command = \
            "return angular.element(document.getElementsByClassName"\
            "('panel-group')[1]).injector().get('billingAndPaymentHistoryCloudService"\
            f"').downloadPDFBillImage({date})"

    def export_ebills(self):
        available_ebills = self.get_bill_dates()
        needed_ebills = helpers.pdf_file_names(available_ebills)
        if len(needed_ebills) > 0:
            for ebill in needed_ebills:
                date = helpers.to_pdf_date(ebill[0])
                pdf_bytes = self.driver.execute_script(self.get_pdf_js(date))
                helpers.b64_to_pdf(pdf_bytes, ebill[1])


