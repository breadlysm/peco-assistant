from datetime import datetime,timedelta
from peco_assistant.helpers import peco_dates, to_utc
from peco_assistant.core import Account
from peco_assistant.database import Database

account = Account()
#data = account.get_data('2021/2/01')

x = to_utc(datetime.now() - timedelta(days=10))
days = peco_dates(start=(x-timedelta(days=220)),end=x)
data = []
for i in days:
    d = account.get_data(i)
    if d is not None:
        data = data + d
# write_data = []
# for day in data:
#     for hour in day:
#         write_data.append(hour)

db = Database()
print(db.last_write)
data = db.influx_format(data)
db.influx_write(data)