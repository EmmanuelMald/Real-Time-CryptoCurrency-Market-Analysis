import json
from datetime import datetime, timezone
import time
from loguru import logger
import requests
from streaming_pipeline.utils.gcp.pubsub import publish_message
from streaming_pipeline.config import GCPConfig, CryptoConfig

gcp_config = GCPConfig()
crypto_config = CryptoConfig()


def main():
    try:
        response = requests.get(crypto_config.CRYPTO_API_URL)
        # raise an exception if the request was unsuccessful
        response.raise_for_status()

        price_data = response.json()

        logger.info(f"Data obtained from API: {crypto_config.CRYPTO_API_URL}")

        for symbol, data in price_data.items():
            data_to_publish = {
                "symbol": symbol,
                "price": data["usd"],
                "event_timestamp": datetime.now(timezone.utc).isoformat(),
            }

            message_bytes = json.dumps(data_to_publish)

            publish_message(
                project_id=gcp_config.PROJECT_ID,
                topic_name=gcp_config.PUBSUB_TOPIC_CRYPTO,
                message=message_bytes,
            )

            logger.info(f"Published message to Pub/Sub topic: {message_bytes}")

    except Exception as e:
        logger.error(f"Error occurred: {e}")


if __name__ == "__main__":
    logger.info("Starting the crypto price publisher...")
    logger.info(f"Using API URL: {crypto_config.CRYPTO_API_URL}")
    logger.info(f"Using Pub/Sub topic: {gcp_config.PUBSUB_TOPIC_CRYPTO}")
    while True:
        main()
        time.sleep(crypto_config.PUBLISH_INTERVAL_SECONDS)
