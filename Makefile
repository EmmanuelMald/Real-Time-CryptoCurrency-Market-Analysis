GCP_PROJECT_ID=learned-stone-454021-c8
GCP_SA=dev-service-account@learned-stone-454021-c8.iam.gserviceaccount.com
GCP_REGION=northamerica-south1
DATAFLOWRUNNER=DataflowRunner
BUCKET_NAME=real_time_crypto_pipeline

gcloud-auth:
	gcloud config unset auth/impersonate_service_account 
	gcloud auth application-default login --impersonate-service-account $(GCP_SA)
	
uv-sync:
	uv sync --all-groups

install-git-hooks: 
	uv run pre-commit install
	uv run pre-commit install-hooks

run-dataflow-pipeline:
	uv run python -m streaming_pipeline.dataflow_pipeline \
	--project $(GCP_PROJECT_ID) \
	--region $(GCP_REGION) \
	--runner $(DATAFLOWRUNNER) \
	--staging_location gs://$(BUCKET_NAME)/staging \
	--temp_location gs://$(BUCKET_NAME)/temp \
	--setup_file=./setup.py \
	--job_name "crypto-streaming" \
	--streaming
