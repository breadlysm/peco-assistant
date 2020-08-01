import os
from helpers import find_inputs, wait_until_exists
from utils.logger import info, error, debug
import time


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
    button_xpath = "/html/body/form/div[3]/div[4]/main/div/div/section/div/div[1]/div/div[1]/div/div/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button"
    signin = wait_until_exists(driver,button_xpath)
    signin.click()
    info("Signing in.")
    time.sleep(.5)
    dashboard_xpath = "/html/body/app-root/app-accounts/main/article/section/div/div[2]/app-card-common[1]/section/header/div/span/span[2]"
    dashboard = wait_until_exists(driver,dashboard_xpath)
    if dashboard.get_attribute("innerText") == 'MY INSIGHTS':
        info('Signed in successfully')
    else:
        debug('Inights element not located on Dashboard. Verify peco dashboard still shows an span element with inner text MY INSIGHTS. Element should be at xpath')
        info('Problem signing in')


    return driver
