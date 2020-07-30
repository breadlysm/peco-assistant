import os
from helpers import find_inputs
from utils.logger import info, error, debug
import time


PECO_USERNAME = os.environ.get('PECO_USERNAME')
PECO_PASSWORD = os.environ.get('PECO_PASSWORD')


def login(driver):
    # Access main login page.
    driver.get('https://secure.peco.com/Pages/Login.aspx')
    if driver.title == 'Login | PECO - An Exelon Company':
        info('Opened Peco Login page')
    else:
        error('Unknown problem opening login page. Screenshot saved. Exiting')
        exit
    # Username Input
    try:
        username = find_inputs(driver, 'Username')
    except NoSuchElementException:
        error("Username Element doesn't exist. Exiting")
        exit
    username.clear()
    username.send_keys(PECO_USERNAME)
    info('input username successfully')
    time.sleep(1)
    # Password
    try:
        password = find_inputs(driver, 'Password')
    except NoSuchElementException:
        error("Password Element doesn't exist. Exiting")
        exit
    password.clear()
    password.send_keys(PECO_PASSWORD)
    time.sleep(1)
    info('Input password successfully')

    # Click Signin
    # Add ability to check that the user is successsfully signed in. 
    info('Trying to submit sign in.')
    signin = driver.find_element_by_xpath(
        '//*[@id="SignInController"]/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button')
    signin.click()
    info("Signing in.")

    return driver
