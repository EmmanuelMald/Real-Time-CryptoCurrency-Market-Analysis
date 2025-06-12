# Real Time Cryptocurrency Market Analysis

In this project, an streaming ETL pipeline is developed to analyse the crypto data. The project is built using Google Cloud tools such as PubSub, Dataform, and BigQuery.

## High Level Description of the project:

1. **Data Ingestion**: Capture Real-time cryptocurrency data from a public API
2. **Straming with Pub/Sub**:The data will be sent to a Pub/Sub topic, which acts as a messaging service.
3. **Data Transformation with Dataform**: Using Apache Beam in Python, the pipeline will continously:

    - Read messages directly from the crypto-stream Pub/Sub topic as they arrive. 
    
    - Parse the incoming json message in-flight, and transform the data (extract fields and convert data types)
    
    - Store the structured data directly into a BigQuery table.
4. **Data Warehousing**: Use BigQuery for analysis.


## How PubSub works

PubSub is a message system that decouples the apps that send events/messages (publishers) from the ones who receives them (subscribers). 

The publisher sends the message to a topic, and each listener subscribes to the topic to receive the message.


## PubSub Subscriber

In this project, the subscriber will be Dataflow, which will get the message obtained from PubSub, make some transformations to the data, and then will be stored directly into BigQuery. All of this in a streaming way.

## PubSub Publisher

In order to PubSub to publish data to the topic, it is required to create a publisher, in this case, will be a CloudRun service that will be sending the crypto data to PubSub infinitely in a time interval of 1 minute. 

The crypto data is obtained from the [**coingecko API**](https://docs.coingecko.com/v3.0.1/reference/introduction)

## **Important Notes when deploying the Dataflow Job**

- It is required to create python packages on each folder that contains custom code (add empty __init__.py files)

- **pyproject.toml file has preference over requirements.txt**

- The dependencies in pyproject.toml must be written in the dependencies list, **not being stored in *extras* nor *groups***

- If custom packages were created, it is required to create a setup.py file in the root of the directoy in order to tell Dataflow how to build the project

- When creating the dataflow job, the whole project is store in GCS as a package, so dataflow can read it.