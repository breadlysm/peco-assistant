from datetime import datetime,timedelta
from peco_spark.helpers import peco_dates, to_utc
from peco_spark.core import Account
from peco_spark.database import Database

#account = Account()
#data = account.get_data('2021/2/01')


# days = peco_dates(to_utc(datetime.now() - timedelta(days=10)))
# data = []
# for i in days:
#     d = account.get_data(i)
#     if d is not None:
#         data.append(d)
# write_data = []
# for day in data:
#     for hour in day:
#         write_data.append(hour)

db = Database()
print(db.last_write)
