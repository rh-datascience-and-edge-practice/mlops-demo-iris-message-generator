"""Main entrypoint for starting container."""
import logging

from iris_message_generator import main
from iris_message_generator.config import app_cfg


if __name__ == "__main__":

    logging.basicConfig(level=app_cfg.log.level)
    main.main()
