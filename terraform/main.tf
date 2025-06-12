provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_pubsub_topic" "crypto_data" {
  name = var.pubsub_topic_name
}

