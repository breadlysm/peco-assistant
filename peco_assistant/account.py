from peco_assistant import helpers
from peco_assistant.config import log, get_config
from time import sleep
import json


class Account:

    def __init__(self, config):
        self.browser = helpers.Browser()
        self.driver = self.browser.driver
        self.driver.scopes = ['https:\/\/secure.peco.com\/.euapi\/mobile\/custom\/auth\/accounts\/[0-9]*\/billing\/[0-9]{4}-[0-9]{2}-[0-9]{2}\/pdf']
        self.username = config['peco']['user']
        self.password = config['peco']['pass']
        self._account_number = None
        self.login()
        self._kwh_cost = None
        self.kwh_cost = self.get_kwh_cost()
        
    def login(self):

        self.driver.get('https://secure.peco.com/accounts/login')
        sleep(3)
        email = self.driver.find_element_by_xpath("//input[@aria-label='Email']")
        email.clear()
        email.send_keys(self.username)
        sleep(1)
        password = self.driver.find_element_by_xpath("//input[@aria-label='Password']")
        password.clear()
        password.send_keys(self.password)
        sleep(1)
        submit = self.driver.find_element_by_xpath("//*/button[@class='btn btn-primary fixed-width']")
        submit.click()
        sleep(3)
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
        sleep(5)
        cost = self.driver.find_element_by_xpath(xpath)
        cost = cost.text
        cost = cost.strip("$")
        cost = float(cost)
        self._kwh_cost = cost
        return self._kwh_cost

    def get_bill_dates(self):
        self.browser.get('https://secure.peco.com/MyAccount/MyBillUsage/Pages/Secure/AccountHistory.aspx')
        sleep(6)
        timeFrame_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[1]/div/duration-dropdown/div/div/a'
        timeFrame_dropdown = self.browser.get_element_at_xpath(timeFrame_xpath)
        sleep(3)
        timeFrame_dropdown.click()

        two_year_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[1]/div/duration-dropdown/div/ul/li[4]'
        twoYearOption = self.browser.get_element_at_xpath(two_year_xpath)
        sleep(4)
        twoYearOption.click()

        bills_xpath = '//*[@id="BillingAndPaymentHistoryController"]/div[3]/div/div[1]/ul/li[2]/a'
        billsTab = self.browser.get_element_at_xpath(bills_xpath)
        sleep(4)
        billsTab.click()

        active_table_xpath = "//*[contains(@class,' active')]//*[contains(@class,'accordion-heading ng-scope')]"
        test = self.browser.wait_for_xpath(active_table_xpath)
        history = self.driver.find_elements_by_xpath(active_table_xpath)

        bills = []
        for element in range(len(history)):
            date = history[element].find_elements_by_xpath("//*[contains(@class,'md-4')]")[element].get_attribute('innerHTML').strip()
            bills.append(date)
        return bills
    
    @property
    def account_number(self):
        if self._account_number is None:
            num = self.driver.find_element_by_xpath("//*/p[text() = 'Account #: ']/span")
            self._account_number = int(num.text)
        return self._account_number

    def get_pdf_js(self, date):
        js_command = \
            "angular.element(document.getElementsByClassName"\
            "('panel-group')[1]).injector().get('billingAndPaymentHistoryCloudService"\
            f"').downloadPDFBillImage('{date}')"
        return js_command
    
    def get_pdf_response(self, date, account_number):
        pdf_url = f"https://secure.peco.com/.euapi/mobile/custom/auth/accounts/{account_number}/billing/{date}/pdf"
        request = self.driver.wait_for_request(pdf_url, timeout=120)
        while request.response is None:
            print(f'waiting for the {date} pdf to download')
            sleep(1)
        return request        

    def export_ebills(self):
        try:
            available_ebills = self.get_bill_dates()
            needed_ebills = helpers.pdf_file_names(available_ebills)
            if len(needed_ebills) > 0:
                for ebill in needed_ebills:
                    date = helpers.to_pdf_date(ebill[0])
                    folder = ebill[1]
                    pdf_bytes = self.driver.execute_script(self.get_pdf_js(date))
                    pdf_bytes = self.get_pdf_response(date, self.account_number)
                    pdf_bytes = json.loads(pdf_bytes.response.body)['data']['billImageData']
                    helpers.b64_to_pdf(pdf_bytes,folder)
                    print(f"Downloaded {date} E-Bill")
                    sleep(5)
        except Exception as exc:
            print("Failed to export invoices")
            print(exc)


def process_pdfs():
    pdfs = helpers.local_pdfs()
    pdf_data = []
    for pdf in pdfs:
        b64_string = helpers.pdf_to_b64(pdf)
        data = helpers.parse_pdf(pdf)
        data['bill_image'] = b64_string
        pdf_data.append(data)
    return pdf_data


