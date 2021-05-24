from datetime import datetime,timedelta
from peco_assistant.helpers import peco_dates, to_utc, Browser
from peco_assistant.core import Account
from peco_assistant.database import Database
from peco_assistant.config import get_config

config = get_config()

def test_browser():
    browser = Browser()

    browser.get('https://google.com')
    if browser.driver.title == 'Google':
        return True
    else:
        return False
        
def test_answer():
    assert test_browser() == True

