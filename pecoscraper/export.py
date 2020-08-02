import os
from utils.logger import info, error, debug
from influxdb import InfluxDBClient
from helpers import get_today,to_timestamp,timestamp_to_iso,days_to_seconds,api_url,START_DATE
import datetime
import json
import time

DB_ADDRESS = os.environ.get('INFLUX_HOST')
DB_PORT = os.environ.get('INFLUX_PORT')
DB_USER = os.environ.get('INFLUX_USER')
DB_PASSWORD = os.environ.get('INFLUX_PASSWORD')
DB_DATABASE = os.environ.get('INFLUX_DBNAME')

influxdb_client = InfluxDBClient(
    DB_ADDRESS, DB_PORT, DB_USER, DB_PASSWORD, None)

def infux_format(data):
    points = []
    for point in data:
        use_data = {
                'measurement': 'enery_use',
                'time': point['endTime'],
                'fields': {
                    'kwh': point['value']
                }
            }
        cost_data = {
                'measurement': 'energy_cost',
                'time': point['endTime'],
                'fields': {
                    'cost': point['providedCost']
                }
            }
        points.append(use_data)
        points.append(cost_data)
    return points



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
    if influxdb_client.write_points(points) == True:
        print("Data written to DB successfully")
    else:  # Speedtest failed.
        error("Write failed")

def usage_urls(account_id, days_per_range, end=get_today(), start=START_DATE):
    dt = datetime.datetime
    end = dt.fromisoformat(end)
    start = dt.fromisoformat(start)
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
    data = process_urls(usage_urls(account_id,10),driver)
    return data