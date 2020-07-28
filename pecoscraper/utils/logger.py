import logging
import sys

def info(msg):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("log.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(msg)
def debug(msg):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("log.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.debug(msg)
def error(msg):
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("log.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.error(msg)