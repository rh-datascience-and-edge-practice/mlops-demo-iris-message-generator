import logging
import os
import time

from iris_message_generator.config import app_cfg

import pandas as pd


def load_data(datafile=app_cfg.data.file):
    data = pd.read_csv(datafile)
    return data


def message_loop(wait_time=app_cfg.message.wait_time):

    while wait_time != 0:
        logging.info("writing message")
        time.sleep(wait_time)

    # Hack to keep container running even when no messages are being generated
    os.system("tail -f /dev/null")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    load_data()
    message_loop()
