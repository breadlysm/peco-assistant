import confuse
import os
from dotenv import load_dotenv

def get_config():
    pass

def env_config():
    load_dotenv()
    config = {
        "login": {
        "email": os.environ.get('PECO_USERNAME'),
        "password": os.environ.get('PECO_PASSWORD')
        },
        "database": {
            "type": os.getenv("DB_TYPE","influxdb"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "name": os.getenv("DB_NAME")
        },
        "peco": {
            "user": os.getenv("PECO_USER"),
            "pass": os.getenv("PECO_PASS")
        },
        "settings":{
            "interval": os.getenv("GRAB_INTERVAL"),
            "fail_interval": os.getenv("FAIL_INTERVAL")
        }
    }

class Config(confuse.Configuration):
    def config_dir(self):
        return './'

def yaml_config():
    return Config('peco_spark')

