"""Configuration file for managing environment variables."""
from pathlib import Path

from dotenv import load_dotenv

import environ


@environ.config(prefix="")
class AppConfig:
    """Application configuration object used for managing environment variables."""

    def __init__():
        """Load environment variables with dotenv."""
        load_dotenv()

    @environ.config
    class Log:
        """App configuration object used for managing logging settings."""

        level = environ.var("INFO", help="The log level of the service.")

        @level.validator
        def _ensure_level_is_valid(self, var, level):
            valid_options = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level not in valid_options:
                raise ValueError(
                    f"LOG_LEVEL of {level} is invalid.  "
                    f"Must be set to one of the following: {valid_options}"
                )

    log = environ.group(Log)

    @environ.config
    class Data:
        """App configuration for the data source."""

        file = environ.var(
            "../data/iris.csv",
            converter=Path,
            help="The file containing the data to load.",
        )

    @environ.config
    class Kafka:
        """App configuration object used for managing kafka settings."""

        bootstrap = environ.var(
            "http://kafka-bootstrap:9092", help="The kafka bootstrap server URL"
        )

        inference_topic = environ.var(
            "iris-inference",
            help="The topic to publish messages contain data to perform an inference on.",
        )

        real_results_topic = environ.var(
            "iris-real-results",
            help="The topic to publish messages container the real world classification data.",
        )

    kafka = environ.group(Kafka)

    @environ.config
    class Message:
        """App configuration object used for managing message generator"""

        wait_time = environ.var(
            10, help="The frequency in seconds that new messages will be generated."
        )

    message = environ.group(Message)


app_cfg = environ.to_config(AppConfig)

if __name__ == "__main__":
    print(environ.generate_help(AppConfig, display_defaults=True))
