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
        str, Field(description="GCP Pub/Sub topic name", default="crypto-data-stream")
    ]
