import os
from utils.logger import info, error, debug
from influxdb import InfluxDBClient

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