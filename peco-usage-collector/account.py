from helpers import wait_until_exists
from utils.logger import info, error, debug
import json
import time
import os

PECO_USERNAME = os.environ.get('PECO_USERNAME')
PECO_PASSWORD = os.environ.get('PECO_PASSWORD')

def login(driver):
    # Access main login page.
    driver.get('https://secure.peco.com/Pages/Login.aspx')
    
    # Username Input
    
    username_xpath = "/html/body/form/div[3]/div[4]/main/div/div/section/div/div[1]/div/div[1]/div/div/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/div[1]/div/div/input"
    username = wait_until_exists(driver,username_xpath)
    username.clear()
    username.send_keys(PECO_USERNAME)
    info('input username successfully')
    # Password
    password_xpath="/html/body/form/div[3]/div[4]/main/div/div/section/div/div[1]/div/div[1]/div/div/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/div[2]/div/div/input"
    password = wait_until_exists(driver,password_xpath)
    password.clear()
    password.send_keys(PECO_PASSWORD)
    info('Input password successfully')
    # Click Signin
    # Add ability to check that the user is successsfully signed in. 
    info('Trying to submit sign in.')
    button_xpath = "//button[contains(@class,'btn-primary')]"
    #button_xpath = "/html/body/form/div[3]/div[4]/main/div/div/section/div/div[1]/div/div[1]/div/div/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button"
    signin = wait_until_exists(driver,button_xpath)
    signin.click()
    info("Signing in.")
    time.sleep(.5)
    dashboard_xpath = "/html/body/form/div[3]/div[4]/footer[1]/div/div/nav/ul/li[1]/a"
    dashboard = wait_until_exists(driver,dashboard_xpath)
    if dashboard.get_attribute("innerText") == 'About Us':
        info('Signed in successfully')
    else:
        debug('Inights element not located on Dashboard. Verify peco dashboard still shows an span element with inner text MY INSIGHTS. Element should be at xpath')
        info('Problem signing in')


    return driver


def get_account_id(driver):
    ''' The account id is slightly difficult to locate using selenium. I did find it within 
    an option element. This function finds that element, and extracts the UUID which is the
    needed account id.'''
    a_id = ''
    driver.get(
    'https://secure.peco.com/MyAccount/MyBillUsage/Pages/Secure/ViewMyUsage.aspx')
    info("Opening My usage homepage. Need to in order to achieve valid session")
    #time.sleep(sleep)
    # I found the accountid within an iframe, on an option element. 
    opower_iframe_xpath = "//iframe[contains(@id,'opower-embedded-iframe')]" 
    # Make sure iframe is loaded
    opower_iframe = wait_until_exists(driver,opower_iframe_xpath)
    # get the src url of the iframe due iframe selenium oddness. 
    opower_api_src = opower_iframe.get_property('src')
    # load iframe url independantly
    driver.get(opower_api_src)
    user_data_script_xpath = '/html/head/script[3]'
    user_data = wait_until_exists(driver,user_data_script_xpath)
    scripts = driver.find_elements_by_tag_name('script')
    for script in scripts: # have to loop because sometimes script is in different place
        if script.get_attribute('textContent').startswith('window'):
            user_data = script
            break
    user_text = user_data.get_attribute('textContent')
    user_json = user_text.split(' = ',1)[1].split(';')[0]
    user_json = json.loads(user_json)
    account_id = user_json['userData']['authorizedCustomers'][0]['utilityAccounts'][0]['uuid']
    return account_id
