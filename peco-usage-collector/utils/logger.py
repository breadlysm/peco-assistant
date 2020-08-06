import logging
import sys

log_format = "%(asctime)s [%(levelname)s] %(message)s"

def info(msg):
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            #logging.FileHandler("log.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(msg)


def debug(msg):
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            #logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    print(msg)
    logging.debug(msg)


def error(msg):
    logging.basicConfig(
        level=logging.ERROR,
        format=log_format,
        handlers=[
            #logging.FileHandler("log.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.error(msg)
