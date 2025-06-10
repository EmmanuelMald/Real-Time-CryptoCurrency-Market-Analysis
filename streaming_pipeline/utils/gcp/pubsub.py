from google.cloud import pubsub_v1
from loguru import logger
from concurrent import futures
from typing import Callable, Optional

# Create a publisher client for Google Cloud Pub/Sub
publisher = pubsub_v1.PublisherClient()

# Create a subscriber client for Google Cloud Pub/Sub
subscriber = pubsub_v1.SubscriberClient()


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


def subscription_exists(project_id: str, subscription_name: str) -> bool:
    """
    Check if a Pub/Sub subscription exists in the specified GCP project.

    Args:
        project_id (str): The GCP project ID where the subscription is located.
        subscription_name (str): The name of the Pub/Sub subscription to check.

    Returns:
        bool: True if the subscription exists, False otherwise.
    """
    # Validate input parameters
    if not all(
        [isinstance(x, str) and x != "" for x in [project_id, subscription_name]]
    ):
        raise ValueError(
            "Both project_id and subscription_name must be not null strings."
        )

    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    try:
        subscriber.get_subscription(request={"subscription": subscription_path})
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


def list_subscriptions(project_id: str, topic_name: Optional[str] = None) -> list[str]:
    """
    List all the Pub/Sub subscriptions in the specified GCP project.
    If a topic_name is provided, list subscriptions for that specific topic.

    Args:
        project_id (str): The GCP project ID to list subscriptions from.
        topic_name (Optional[str]): The name of the Pub/Sub topic to filter subscriptions by.

    Returns:
        list[str]: A list of subscription names in the format "projects/{project_id}/subscriptions/{subscription_name}".
    """
    # Validate input parameter
    if not isinstance(project_id, str) or project_id == "":
        raise ValueError("project_id must be a non-empty string.")

    if topic_name:
        if not isinstance(topic_name, str) or topic_name == "":
            raise ValueError("topic_name must be a non-empty string.")
        topic_path = publisher.topic_path(project_id, topic_name)
        subscriptions = publisher.list_topic_subscriptions(
            request={"topic": topic_path}
        )

        return [subscription_name for subscription_name in subscriptions]

    else:
        subscriptions = subscriber.list_subscriptions(
            request={"project": f"projects/{project_id}"}
        )

        return [subscription.name for subscription in subscriptions]


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


def create_subscription(
    project_id: str,
    topic_name: str,
    subscription_name: str,
) -> None:
    """
    Create a Pub/Sub subscription for a specified topic in the GCP project.

    Args:
        project_id (str): The GCP project ID where the topic is located.
        topic_name (str): The name of the Pub/Sub topic to subscribe to.
        subscription_name (str): The name of the Pub/Sub subscription to create.
    """
    if not topic_exists(project_id, topic_name):
        raise ValueError(
            f"Topic '{topic_name}' does not exist in project '{project_id}'."
        )

    elif subscription_exists(project_id, subscription_name):
        raise ValueError(
            f"Subscription '{subscription_name}' already exists in project '{project_id}'."
        )
    # Validate input parameters
    elif not isinstance(subscription_name, str) or subscription_name == "":
        raise ValueError("subscription_name must be non-empty strings.")

    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Create the subscription
    subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )

    logger.info(
        f"Subscription '{subscription_name}' created successfully for topic '{topic_name}' in project '{project_id}'."
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


def delete_subscription(
    project_id: str,
    subscription_name: str,
) -> None:
    """
    Delete a Pub/Sub subscription in the specified GCP project.

    Args:
        project_id (str): The GCP project ID where the subscription is located.
        subscription_name (str): The name of the Pub/Sub subscription to delete.
    """
    if not subscription_exists(project_id, subscription_name):
        raise ValueError(
            f"Subscription '{subscription_name}' does not exist in project '{project_id}'."
        )

    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Delete the subscription
    subscriber.delete_subscription(request={"subscription": subscription_path})

    logger.info(
        f"Subscription '{subscription_name}' deleted successfully from project '{project_id}'."
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


def pull_messages(
    project_id: str, subscription_name: str, max_messages: int = 10
) -> list[str]:
    """
    Pull messages from a Pub/Sub subscription in the specified GCP project.

    Args:
        project_id (str): The GCP project ID where the subscription is located.
        subscription_name (str): The name of the Pub/Sub subscription to pull messages from.
        max_messages (int): The maximum number of messages to pull. Default is 10.

    Returns:
        list[str]: A list of messages pulled from the subscription.
    """
    if not subscription_exists(project_id, subscription_name):
        raise ValueError(
            f"Subscription '{subscription_name}' does not exist in project '{project_id}'."
        )

    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Pull messages
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": max_messages,
        }
    )

    messages = [msg.message.data.decode("utf-8") for msg in response.received_messages]

    # Acknowledge the received messages
    ack_ids = [msg.ack_id for msg in response.received_messages]
    if ack_ids:
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

    return messages
