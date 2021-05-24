import confuse
import os
from dotenv import load_dotenv

def get_config():
    return env_config()

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
            "pass": os.getenv("DB_PASS"),
            "name": os.getenv("DB_NAME")
        },
        "peco": {
            "user": os.getenv("PECO_USER"),
            "pass": os.getenv("PECO_PASS")
        },
        "settings":{
            "sleep_interval": hours_to_seconds(int(os.getenv("SLEEP_INTERVAL", 6)))
        }
    }
    
    return config

class Config(confuse.Configuration):
    def config_dir(self):
        return './'

def yaml_config():
    return Config('peco_assistant')

def hours_to_seconds(hours):
    return hours * 60 * 60