import os
from helpers import find_inputs
from utils.logger import info, error, debug

PECO_LOGIN_URL = os.environ.get('PECO_LOGIN_URL')
PECO_USERNAME = os.environ.get('PECO_USERNAME')
PECO_PASSWORD = os.environ.get('PECO_PASSWORD')

def login(driver):
    # Access main login page. 
    driver.get(PECO_LOGIN_URL)
    if driver.title == 'Login | PECO - An Exelon Company':
        info('Opened Peco Login page')
    else:
        error('Unknown problem opening login page. Screenshot saved. Exiting')
        driver.save_screenshot('screenshots/error-opening-login.png')
        exit
    # Username Input
    try:
        username = find_inputs(driver,'Username')
    except NoSuchElementException:
        error("Username Element doesn't exist. Exiting")
        driver.save_screenshot("screenshots/username-error.png")
        exit
    username.clear()
    username.send_keys(PECO_USERNAME)
    info('input username successfully')

    # Password
    try:
        password = find_inputs(driver,'Password')
    except NoSuchElementException:
        error("Password Element doesn't exist. Exiting")
        driver.save_screenshot("screenshots/password-error.png")
        exit
    password.clear()
    password.send_keys(PECO_PASSWORD)

    # Click Signin 
    signin = driver.find_element_by_xpath('//*[@id="SignInController"]/ng-form/div/exelon-decorator-simple/div/div/div/div[1]/button')
    signin.click()
    driver.save_screenshot("screenshots/submitted.png")
    info("Submitted login") 

    return driver