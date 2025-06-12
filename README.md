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
