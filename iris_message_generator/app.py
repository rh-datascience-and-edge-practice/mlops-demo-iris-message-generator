import logging
import os
import time

from iris_message_generator.config import app_cfg

import pandas as pd

while app_cfg.message.wait_time != 0:
    logging.info("writing message.")

    time.sleep()

# Hack to keep container running even when no messages are being generated
os.system("tail -f /dev/null")
