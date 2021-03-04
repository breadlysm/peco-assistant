from peco_spark.core import Account

account = Account()
data = account.get_data('2021/2/01')
print(data)
