import argparse
import apache_beam as beam
from loguru import logger
from apache_beam.options.pipeline_options import PipelineOptions
from streaming_pipeline.config import GCPConfig
from streaming_pipeline.pipeline_auxiliars import ParseMessage, LogMessage

gcp_config = GCPConfig()


def run():
    # Set up command line argument parsing
    logger.info("Setting up command line arguments")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_table",
        required=False,
        help='The BigQuery table to write to in the format "project:dataset.table"',
        default=f"{gcp_config.PROJECT_ID}.{gcp_config.DATASET_NAME}.{gcp_config.TABLE_NAME}",
    )

    # Parse known arguments and pipeline options
    known_args, pipeline_args = parser.parse_known_args()
    logger.info(f"Parsed arguments: {known_args}")
    logger.info(f"Pipeline arguments: {pipeline_args}")

    pipeline_options = PipelineOptions(pipeline_args)

    # Set up the pipeline
    with beam.Pipeline(options=pipeline_options) as p:
        # Step 1: Read messages from the PubSub topic
        # This uses the dataflow-managed subscription for the PubSub topic
        messages = (
            p  # Start of the pipeline
            | "ReadFromPubSub"
            >> beam.io.ReadFromPubSub(
                topic=f"projects/{gcp_config.PROJECT_ID}/topics/{gcp_config.PUBSUB_TOPIC_CRYPTO}"
            )
        )
        # Step 1.1: Log the incoming messages
        _ = messages | "LogMessages" >> beam.ParDo(LogMessage())

        # Step 2: Prase the JSON message
        parsed_data = messages | "ParseMessages" >> beam.ParDo(ParseMessage())

        # Step 3: Write the parsed data to BigQuery
        _ = (
            parsed_data
            | "WriteToBigQuery"
            >> beam.io.WriteToBigQuery(
                known_args.output_table,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,  # because the table is handled by terraform
            )
        )


if __name__ == "__main__":
    run()
