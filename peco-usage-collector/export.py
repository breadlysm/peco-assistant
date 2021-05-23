import os
from utils.logger import info, error, debug
from influxdb import InfluxDBClient
from helpers import get_today,to_timestamp,timestamp_to_iso,days_to_seconds,api_url,START_DATE,iso_to_timestamp
import json
import time
import datetime

DB_ADDRESS = os.environ.get('INFLUX_HOST')
DB_PORT = os.environ.get('INFLUX_PORT')
DB_USER = os.environ.get('INFLUX_USER')
DB_PASSWORD = os.environ.get('INFLUX_PASSWORD')
DB_DATABASE = os.environ.get('INFLUX_DBNAME')

influxdb_client = InfluxDBClient(host=DB_ADDRESS, port=DB_PORT, username=DB_USER, password=DB_PASSWORD)

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


def get_last_write():
    try:
        last_write = influxdb_client.query('SELECT last("kwh")  FROM "autogen"."enery_use"')
        last_write = last_write.raw['series'][0]['values'][0][0]
        last_write = datetime.datetime.strptime(last_write,"%Y-%m-%dT%H:%M:%SZ")
        debug(f'last_write is {last_write}')
    except:
        debug('Problem returning query or other issue. Returning start date as last write')
        last_write = iso_to_timestamp(to_timestamp(START_DATE))
    return last_write


def get_first_write():
    try:
        first_write = influxdb_client.query('SELECT first("kwh")  FROM "autogen"."enery_use"')
        first_write = first_write.raw['series'][0]['values'][0][0]
        first_write = datetime.datetime.strptime(first_write,"%Y-%m-%dT%H:%M:%SZ")
        first_write += datetime.timedelta(days=-1)
        debug(f'first write is {first_write}')
    except:
        debug('Problem returning query or other issue. Returning start date as first write')
        first_write = iso_to_timestamp(to_timestamp(START_DATE))
    return first_write


def init_db():
    databases = influxdb_client.get_list_database()

    if len(list(filter(lambda x: x['name'] == DB_DATABASE, databases))) == 0:
        influxdb_client.create_database(
            DB_DATABASE)  # Create if does not exist.
        info(f'Created database {DB_DATABASE}')
    else:
        # Switch to if does exist.
        influxdb_client.switch_database(DB_DATABASE)


def influx_write(points):
    if influxdb_client.write_points(points,batch_size=200,protocol='json',database=DB_DATABASE) == True:
        print("Data written to DB successfully")
    else:  # Speedtest failed.
        error("Write failed")

def usage_urls(account_id, days_per_range,start,end=iso_to_timestamp(get_today())):
    ranges = []
    usage_urls = []
    if (end.timestamp() - start.timestamp()) > days_to_seconds(days_per_range):
        range_end = end.timestamp()
        range_start = (end.timestamp() - days_to_seconds(days_per_range))
        while (range_end - start.timestamp()) > days_to_seconds(days_per_range):
            ranges.append({
                'end': timestamp_to_iso(range_end), 'start': timestamp_to_iso(range_start)
            })
            range_end = (range_end - days_to_seconds(days_per_range))
            range_start = (range_start-days_to_seconds(days_per_range))
        diff = range_end - start.timestamp()
        ranges.append({'end':timestamp_to_iso(range_end),'start':timestamp_to_iso(range_end-diff)})
    for range in ranges:
        usage_urls.append(
            api_url(account_id, start=range['start'], end=range['end']))
    return usage_urls


def process_urls(urls,driver):
    usage = []
    length = len(urls)
    for url in urls:
        info(f"Making request to {url}.")
        driver.get(url)
        data = driver.find_elements_by_xpath("//pre")[0].text
        data = json.loads(data)
        data = data['reads']
        for line in data:
            usage.append(line)
        index = urls.index(url) + 1
        info(f'Processed {index} of {length} urls')
        time.sleep(.5)
    return(usage)


def get_data(account_id,driver):
    start = iso_to_timestamp(to_timestamp(START_DATE))
    if get_last_write() > start and start > get_first_write():
        start = get_last_write()
    data = process_urls(usage_urls(account_id,10,start),driver)
    return data
last = get_last_write()
