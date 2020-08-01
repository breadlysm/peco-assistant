from helpers import get_uuid,wait_until_exists
from utils.logger import info, error, debug
import json
import time


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
    opower_iframe_xpath = "/html/body/form/div[3]/div[4]/main/div/div/section[2]/div[2]/div/div[1]/div/div/div[2]/iframe" 
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
    # options = driver.find_elements_by_tag_name('option')
    # account_id = ''
    # for element in options:
    #     if element.get_property('label') == 'Electricity':
    #         account_id = element.get_property('value')
    #         account_id = get_uuid(account_id)
    #         if len(account_id) < 5 & sleep <5:
    #             info('Invalid Account ID. Retry')
    #             get_account_id(driver,sleep=5)
    #         elif sleep == 5 and len(account_id) < 5:
    #             info('Still couldn\'t retrieve the account id. Exiting')
    #             exit
    #         else:
    #             info('Found account ID.')
    #             break
    return account_id
