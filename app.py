import logging

from iris_message_generator import main

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    main.load_data()
    main.message_loop()
