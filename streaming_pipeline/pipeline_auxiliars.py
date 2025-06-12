import apache_beam as beam
import json
from loguru import logger


class ParseMessage(beam.DoFn):
    def process(self, element: bytes):
        """
        Parses the incoming byte string from PubSub into a Python dictionary

        Args:
            element (bytes): The incoming byte string from PubSub

        Yields:
            dict: Parsed message as a dictionary
        """
        try:
            # PubSub messages are bytes, so we decode them to a UTF-8 string
            message_body = element.decode("utf-8")

            # Parse the string as JSON
            data = json.loads(message_body)

            # The output is a dictionary that will become a row in BigQuery
            yield data

        except Exception as e:
            logger.error(f"Failed to parse message:{e}")


class LogMessage(beam.DoFn):
    """
    Logs the incoming PubSub message
    """

    def process(self, element: bytes):
        message_body = element.decode("utf-8")
        logger.info(f"Received message: {message_body}")
        yield element
