import copy
import logging
import os
import time
import typing

from iris_message_generator.config import app_cfg

import json

import pandas as pd

from pathlib import Path

from kafka import KafkaProducer


def load_data(datafile: typing.Union[str, Path] = app_cfg.data.file):
    logging.info(f"Loading data from csv: {datafile}")
    data = pd.read_csv(datafile)
    return data


def kafka_producer(bootstrap: str = app_cfg.kafka.bootstrap):
    logging.info(f"Connecting to bootstrap server: {bootstrap}")
    producer = KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    return producer


def write_message(producer: KafkaProducer, topic: str, message: str):
    logging.info(f"Publishing message: {message} on Topic: {topic}")
    producer.send(topic = topic, value=message)


def iris_messages(data: pd.DataFrame, row: int):
    classification_data = data.drop(
        ["sepalLength", "sepalWidth", "petalLength", "petalWidth"], axis=1
    )
    inference_data = data.drop("species", axis=1)

    iris_message = {}
    iris_message["iris"] = inference_data.loc[row].to_dict()

    results_message = copy.copy(iris_message)
    results_message["classification"] = classification_data.loc[row].to_dict()

    logging.info(iris_message)
    logging.info(results_message)

    return iris_message, results_message


def message_loop(
    data: pd.DataFrame,
    producer: KafkaProducer,
    wait_time: int = app_cfg.message.wait_time,
):

    # repeat the loop forever
    while wait_time != 0:
        # loop through all of the data
        for index, row in data.iterrows():
            logging.info("writing message")
            iris_message, results_message = iris_messages(data, index)
            write_message(producer, app_cfg.kafka.inference_topic, iris_message)
            write_message(producer, app_cfg.kafka.real_results_topic, results_message)
            time.sleep(wait_time)

    # Hack to keep container running even when no messages are being generated
    os.system("tail -f /dev/null")


def main():
    data = load_data()
    producer = kafka_producer()
    message_loop(data, producer)


if __name__ == "__main__":
    main()
