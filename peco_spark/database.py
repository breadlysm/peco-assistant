from influxdb import InfluxDBClient
from pytz import utc
from .helpers import log,get_today, sub_days, to_utc,two_years
from .config import get_config
import json
import time
from datetime import datetime

config = get_config()

class Database:
    def __init__(self):
        self.db_user = self.config()['database']['user']
        self.db_pass = self.config()['database']['pass']
        self.db_type = self.config()['database']['type']
        self.db_host = self.config()['database']['host']
        self.db_port = self.config()['database']['port']
        self.db_name = self.config()['database']['name']
        self._client = None
        self.client = self.get_db_client()
        self.init_db()
        self._last_write = None
        self.last_write = self.last_write()
        

    def config(self):
        return get_config()
    
    def init_db(self):
        databases = self.client.get_list_database()

        if len(list(filter(lambda x: x['name'] == self.db_name, databases))) == 0:
            self.client.create_database(
                self.db_name)  # Create if does not exist.
            log.info(f'Created database {self.db_name}')
        else:
            # Switch to if does exist.
            self.client.switch_database(self.db_name)

    def get_db_client(self):
        if self.db_type == 'influxdb':
            self._client = InfluxDBClient(host=self.db_host,
                                    port=self.db_port,
                                    username=self.db_user,
                                    password=self.db_pass)
        else:
            log.error("No client type or incompatibile DB Client type. Closing")
        return self._client
        
    def influx_write(self,points):
        """Writes list of influx_format points to specific named DB. 

        Args:
            points (influx_format): List of points formatted to match influx json protocol
        """
        if self.client.write_points(points,batch_size=200,protocol='json',database=self.db_name) == True:
            print("Data written to DB successfully")
        else:  # Speedtest failed.
            log.error("Write failed")

    def last_write(self):
        get_last_write = False
        if self._last_write is None:
            get_last_write = True
        elif self._last_write < sub_days(datetime.now(utc),1):
            get_last_write = True
        if get_last_write:
            self.get_last_write_influx()
            return self._last_write
        else:
            return self._last_write


    def get_last_write_influx(self):
        """retrieves the last data point recorded on the objects client's db

        Returns:
            datetime: last write point in python datetime
        """
        try:
            last_write = self.client.query('SELECT last("kwh")  FROM "autogen"."enery_use"')
            last_write = last_write.raw['series'][0]['values'][0][0]
            last_write = datetime.strptime(last_write,"%Y-%m-%dT%H:%M:%SZ")
            log.debug(f"last_write is {last_write}")
        except Exception as err:
            print(err)
            log.debug("Problem returning query or other issue.")
            last_write = None
        self._last_write = to_utc(last_write)
        return self._last_write
    
    def influx_format(self,data):
        """Formats the data points retrieved to the appropriate influx format. 


        Args:
            data (list): list of dictionaries that contain the hours of the day usage metrics. 

        Returns:
            list: same data formatted for influx. 
        """
        points = []
        for point in data:
            body = {
                    'measurement': 'enery_use',
                    'time': point['endDate'],
                    'fields': {
                        'kwh': float(point['kwh']),
                        'cost': point['usage_cost'],
                        'temperature': point['temperature'],
                        'current_price': point['current_price']
                    }
                }
            points.append(body)
        return points