import logging

from iris_message_generator.config import app_cfg

from iris_message_generator import main

if __name__ == "__main__":

    logging.basicConfig(level=app_cfg.log.level)
    main.main()
