from helpers import get_uuid
from utils.logger import info, error, debug
import time


def get_account_id(driver,sleep=2):
    ''' The account id is slightly difficult to locate using selenium. I did find it within 
    an option element. This function finds that element, and extracts the UUID which is the
    needed account id.'''
    a_id = ''
    driver.get(
    'https://secure.peco.com/MyAccount/MyBillUsage/Pages/Secure/ViewMyUsage.aspx')
    info("Opening My usage homepage. Need to in order to achieve valid session")
    time.sleep(sleep)
    for iframe in driver.find_elements_by_tag_name('iframe'):
        if iframe.get_property('id').startswith('opower',0,6): 
            a_id = iframe.get_property('src')
    driver.get(a_id)
    time.sleep(sleep)
    options = driver.find_elements_by_tag_name('option')
    account_id = ''
    for element in options:
        if element.get_property('label') == 'Electricity':
            account_id = element.get_property('value')
            account_id = get_uuid(account_id)
            if len(account_id) < 5 & sleep <5:
                info('Invalid Account ID. Retry')
                get_account_id(driver,sleep=5)
            elif sleep == 5 and len(account_id) < 5:
                info('Still couldn\'t retrieve the account id. Exiting')
                exit
            else:
                info('Found account ID.')
                break
    return account_id
