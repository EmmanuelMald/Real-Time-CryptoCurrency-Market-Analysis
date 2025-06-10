from google.cloud import pubsub_v1
from loguru import logger
from concurrent import futures
from typing import Callable, Optional

# Create a publisher client for Google Cloud Pub/Sub
publisher = pubsub_v1.PublisherClient()


def topic_exists(project_id: str, topic_name: str) -> bool:
    """
    Check if a Pub/Sub topic exists in the specified GCP project.

    Args:
        project_id (str): The GCP project ID where the topic is located.
        topic_name (str): The name of the Pub/Sub topic to check.

    Returns:
        bool: True if the topic exists, False otherwise.
    """
    # Validate input parameters
    if not all([isinstance(x, str) and x != "" for x in [project_id, topic_name]]):
        raise ValueError("Both project_id and topic_name must be not null strings.")

    topic_path = publisher.topic_path(project_id, topic_name)
    try:
        publisher.get_topic(request={"topic": topic_path})
        return True
    except Exception:
        return False


def list_topics(project_id: str) -> list[str]:
    """
    List all the Pub/Sub topics in the specified GCP project.

    Args:
        project_id (str): The GCP project ID to list topics from.

    Returns:
        list[str]: A list of topic names in the format "projects/{project_id}/topics/{topic_name}".
    """
    # Validate input parameter
    if not isinstance(project_id, str) or project_id == "":
        raise ValueError("project_id must be a non-empty string.")

    topics = publisher.list_topics(request={"project": f"projects/{project_id}"})
    return [topic.name for topic in topics]


def create_topic(project_id: str, topic_name: str) -> None:
    """
    Create a Pub/Sub topic in the specified GCP project.

    Args:
        project_id (str): The GCP project ID where the topic will be created.
        topic_name (str): The name of the Pub/Sub topic to create.
    """
    # topic_exists already has input validation
    if topic_exists(project_id, topic_name):
        raise ValueError(
            f"Topic '{topic_name}' already exists in project '{project_id}'."
        )

    # Generate the path for the topic
    topic_path = publisher.topic_path(project_id, topic_name)

    # Create the topic
    topic = publisher.create_topic(request={"name": topic_path})

    logger.info(
        f"Pub/Sub topic '{topic.name}' created successfully in project '{project_id}'."
    )


def delete_topic(project_id: str, topic_name: str) -> None:
    """
    Delete a Pub/Sub topic in the specified GCP project.
    Args:
        project_id (str): The GCP project ID where the topic is located.
        topic_name (str): The name of the Pub/Sub topic to delete.
    Returns:
        None
    """
    # topic_exists already has input validation
    if not topic_exists(project_id, topic_name):
        raise ValueError(
            f"Topic '{topic_name}' does not exist in project '{project_id}'."
        )

    # Generate the path for the topic
    topic_path = publisher.topic_path(project_id, topic_name)

    # Delete the topic
    publisher.delete_topic(request={"topic": topic_path})

    logger.info(
        f"Pub/Sub topic '{topic_name}' deleted successfully from project '{project_id}'."
    )


def publish_message(
    project_id: str,
    topic_name: str,
    message: str,
    callback: Optional[Callable[[futures.Future], None]] = None,
) -> None:
    """
    Publish a message to a Pub/Sub topic in the specified GCP project.
    The code was adapted from: https://cloud.google.com/pubsub/docs/publisher

    Args:
        project_id (str): The GCP project ID where the topic is located.
        topic_name (str): The name of the Pub/Sub topic to publish to.
        message (str): The message to publish.
        callback (Callable[[futures.Future], None], optional): A callback function to handle the result of the publish operation.
    """
    # Validate input parameters
    if not all(
        [isinstance(x, str) and x != "" for x in [project_id, topic_name, message]]
    ):
        raise ValueError(
            "project_id, topic_name, and message must be non-empty strings."
        )

    # Generate the path for the topic
    topic_path = publisher.topic_path(project_id, topic_name)

    # Publish the message
    publish_future = publisher.publish(topic_path, data=message.encode("utf-8"))
    logger.info(f"Publishing message to Pub/Sub topic {topic_name}")

    if callback:
        publish_future.add_done_callback(callback)
