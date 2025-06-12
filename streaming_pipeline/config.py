from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Annotated


class GCPConfig(BaseSettings):
    PROJECT_ID: Annotated[
        str, Field(description="GCP Project ID", default="learned-stone-454021-c8")
    ]
    REGION: Annotated[
        str,
        Field(
            description="GCP main region where all the resources are created",
            default="northamerica-south1",
        ),
    ]
    PUBSUB_TOPIC_CRYPTO: Annotated[
        str, Field(description="GCP Pub/Sub topic name", default="crypto-data-topic")
    ]
    BUCKET_NAME: Annotated[
        str,
        Field(
            description="Main GCP bucket of the project",
            default="real_time_crypto_pipeline",
        ),
    ]
    DATASET_NAME: Annotated[
        str, Field(description="BigQuery dataset name", default="crypto_data")
    ]
    TABLE_NAME: Annotated[
        str, Field(description="BigQuery table name", default="crypto_prices")
    ]


class CryptoConfig(BaseSettings):
    CRYPTO_API_URL: Annotated[
        str,
        Field(
            description="Crypto API URL",
            default="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd",
        ),
    ]
    PUBLISH_INTERVAL_SECONDS: Annotated[
        int,
        Field(
            description="Interval in seconds between API calls to publish data",
            default=60,
        ),
    ]
