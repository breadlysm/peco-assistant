from peco_spark.helpers import Browser, eastern, peco_dates,to_datetime,log, two_years
from peco_spark.database import Database
from peco_spark.account import Account
#from utils.logger import info, error, debug
import json
import time
import os
from peco_spark.config import get_config


def main():
    run = True
    config = get_config()
    account = Account(config)
    db = Database(config)
    last_write = two_years()
    while run:
        start_date = db.last_write or two_years()
        if last_write < start_date:
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
            log.info("Usage succesfully collected. Sleeping for 6 hours")
        else: 
            log.info("No update needed. Sleeping for 6 hours")
            
        time.sleep(21600)

if __name__ == '__main__':
    main()

