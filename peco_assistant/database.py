from influxdb import InfluxDBClient
from pytz import utc
from peco_assistant.helpers import log,get_today, sub_days, to_utc,two_years
import json
import time
from datetime import datetime

class Database:
    def __init__(self,config):
        self.db_user = config['database']['user']
        self.db_pass = config['database']['pass']
        self.db_type = config['database']['type']
        self.db_host = config['database']['host']
        self.db_port = config['database']['port']
        self.db_name = config['database']['name']
        self._client = None
        self.init_db()
        self._last_write = None
            
    def init_db(self):
        databases = self.client.get_list_database()

        if len(list(filter(lambda x: x['name'] == self.db_name, databases))) == 0:
            self.client.create_database(
                self.db_name)  # Create if does not exist.
            log.info(f'Created database {self.db_name}')
        else:
            # Switch to if does exist.
            self.client.switch_database(self.db_name)

    @property
    def client(self):
        if self._client is not None:
            return self._client
        else:
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

    @property
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