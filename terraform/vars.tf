# To check data types: https://developer.hashicorp.com/terraform/language/expressions/types

variable "gcp_project_id" {
  type        = string
  description = "GCP project id"
  default     = "learned-stone-454021-c8"
}

variable "gcp_region" {
  type        = string
  description = "GCP region where the resources will be stored"
  default     = "northamerica-south1"
}

variable "gcp_zone" {
  type        = string
  description = "GCP zone within the gcp_region"
  default     = "northamerica-south1-a"
}

variable "gcp_dev_sa" {
  type        = string
  description = "GCP Service Account that CloudRun will use to authenticate"
  default     = "dev-service-account@learned-stone-454021-c8.iam.gserviceaccount.com"
}

variable "pubsub_topic_name" {
  type        = string
  description = "Name of the Pub/Sub topic to be created"
  default     = "crypto-data-topic"
}