provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_pubsub_topic" "crypto_data" {
  name = var.pubsub_topic_name
}

resource "google_bigquery_dataset" "bq_crypto_data" {
  dataset_id = var.bq_dataset_name
  location   = var.gcp_region
}

resource "google_bigquery_table" "crypto_prices_table" {
  dataset_id = google_bigquery_dataset.bq_crypto_data.dataset_id
  table_id   = var.bq_crypto_prices_table

  schema = <<EOF
  [
    {
      "name": "event_timestamp",
      "type": "TIMESTAMP",
      "mode": "REQUIRED"
    },
    {
      "name": "symbol",
      "type": "STRING",
      "mode": "REQUIRED"
    },
    {
      "name": "price",
      "type": "FLOAT",
      "mode": "REQUIRED"
    }
  ]
  EOF
}