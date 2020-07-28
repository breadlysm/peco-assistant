from helpers import get_uuid
from utils.logger import info, error, debug

def get_account_id(driver):
    ''' The account id is slightly difficult to locate using selenium. I did find it within 
    an option element. This function finds that element, and extracts the UUID which is the
    needed account id.'''
    iframe = driver.find_element_by_tag_name('iframe')
    usage_src = iframe.get_property('src')
    driver.get(usage_src)
    options = driver.find_elements_by_tag_name('option')
    account_id = ''
    for element in options:
        if element.get_property('label') == 'Electricity':
            info('Found account ID. Pulling data.')
            account_id = element.get_property('value')
            account_id = get_uuid(account_id)
    return account_id