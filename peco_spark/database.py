import 
from influxdb import InfluxDBClient
from .helpers import log,get_today,two_years
from .config import get_config
import json
import time
import datetime

config = get_config()

class Database:
    def __init__(self):
        self.db_user = self.config()['database']['user']
        self.db_pass = self.config()['database']['pass']
        self.db_type = self.config()['database']['type']
        self.db_host = self.config()['database']['host']
        self.db_port = self.config()['database']['port']
        self.db_name = self.config()['database']['name']
        self.client = self.get_db_client()
        self._client = None
        self.last_write = self.get_last_write()
        self._last_write = None

    def config(self):
        return get_config()

    def get_db_client(self):
        if self.db_type == 'influxdb':
            self._client = InfluxDBClient(host=self.db_host,
                                    port=self.db_host,
                                    username=self.db_user,
                                    password=self.db_pass)
        else:
            log.error("No client type or incompatibile DB Client type. Closing")
        return self._client



    def get_last_write_influx(self):
        try:
            last_write = self.client.query('SELECT last("kwh")  FROM "autogen"."enery_use"')
            last_write = last_write.raw['series'][0]['values'][0][0]
            last_write = datetime.datetime.strptime(last_write,"%Y-%m-%dT%H:%M:%SZ")
            log.debug(f'last_write is {last_write}')
        except:
            log.debug('Problem returning query or other issue.')
            last_write = None
        self.last_write = last_write
        return self.last_write
    
    def infux_format(data):
        points = []
        for point in data:
            use_data = {
                    'measurement': 'enery_use',
                    'time': iso_to_timestamp(point['endTime']),
                    'fields': {
                        'kwh': float(point['value'])
                    }
                }
            cost_data = {
                    'measurement': 'energy_cost',
                    'time': iso_to_timestamp(point['endTime']),
                    'fields': {
                        'cost': float(point['providedCost'])
                    }
                }
            points.append(use_data)
            points.append(cost_data)
        return points