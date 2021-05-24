import confuse
import os
from peco_assistant.logs import Log
from dotenv import load_dotenv
import chromedriver_autoinstaller
import subprocess

log = None
def get_config():
    return env_config()

def is_docker():
    docker = os.getenv("IS_DOCKER", False)
    if docker == 'yes':
        docker = True
    else:
        docker = False
    return docker

def env_config():
    load_dotenv()
    config = {
        "peco": {
            "user": os.getenv("PECO_USER"),
            "pass": os.getenv("PECO_PASS")
        },
        "database": {
            "type": os.getenv("DB_TYPE","influxdb"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "pass": os.getenv("DB_PASS"),
            "name": os.getenv("DB_NAME")
        },
        "settings":{
            "sleep_hours": int(os.getenv("SLEEP_INTERVAL", 24)),
            "sleep_interval": hours_to_seconds(int(os.getenv("SLEEP_INTERVAL", 24))),
            "log_level": os.getenv("LOG_TYPE", 'info')
        },
        "passive_settings": {
            "running_in_docker": is_docker()
        }
    }

    return config

def passive_settings():
    config = get_config()
    if not config['passive_settings']['running_in_docker']:
        log.info("App is not running in Docker. Configuring Chrome Driver.")
        chromedriver_autoinstaller.install()
        log.info("Driver Configured.")
class Config(confuse.Configuration):
    def config_dir(self):
        return './'

def yaml_config():
    return Config('peco_assistant')

def hours_to_seconds(hours):
    return hours * 60 * 60

def is_docker():
    docker = os.getenv("IS_DOCKER", False)
    if docker == 'yes':
        docker = True
    else:
        docker = False
    return docker

log = Log(get_config())
passive_settings()