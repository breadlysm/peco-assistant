from peco_assistant.helpers import Browser, eastern, peco_dates,to_datetime,two_years,sub_days,get_today
from peco_assistant.database import Database
from peco_assistant.account import Account, process_pdfs
#from utils.logger import info, error, debug
import json
import time
import os
from peco_assistant.config import get_config, log


def main():
    run = True
    config = get_config()
    account = Account(config)
    db = Database(config)
    while run:
        start_date = db.last_write or two_years()
        #if db.last_write < sub_days(get_today,2):
        if db.last_write <= start_date:
            log.info("The last data written is over 1 day old, starting update")
            dates = peco_dates(start_date)
            data = []
            for day in dates:
                usage = account.get_data(day)
                if usage is None:
                    continue
                usage = db.influx_format(usage)
                data = data + usage
            db.influx_write(data)
            last_write = start_date
            log.info(F"Usage succesfully collected. Sleeping for {config['settings']['sleep_hours']} hours")
            try:
                account.export_ebills()
            except:
                log.info("Failed to export ebills")
            pdf_data = process_pdfs()
            if pdf_data:
                db.write_ebills(pdf_data)
        else: 
            log.info(F"No update needed. Sleeping for {config['settings']['sleep_hours']} hours")
        time.sleep(config['settings']['sleep_interval'])

if __name__ == '__main__':
    main()

