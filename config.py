import os
from google.cloud import storage, bigquery
from google.oauth2 import service_account
from datetime import datetime

# datetime for file generation and BigQuery:
TIME_NOW = datetime.now()
DATE = TIME_NOW.strftime("%Y-%m-%d")
TIME = TIME_NOW.strftime("%H:%M:%S")

# OpenWeatherMap API Key:
API = os.getenv('API_KEY')

# Generated file settings:
FILENAME_DATE = TIME_NOW.strftime("%Y%m%d_%H%M%S")
FILENAME = f'weather_data_{FILENAME_DATE}.csv'  # Change name if you want to

# Google Cloud Platform service account settings:
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
CREDENTIALS = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# Google Cloud Storage settings:
STORAGE_CLIENT = storage.Client(credentials=CREDENTIALS)
GCS_BUCKET = STORAGE_CLIENT.bucket('your_bucket_name_here')
GCS_BLOB = GCS_BUCKET.blob(f'eventual_folder_if_needed/{FILENAME}')
GCS_URI = f'gs://{GCS_BUCKET.name}/{GCS_BLOB.name}'

# Google BigQuery settings:
BQ_CLIENT = bigquery.Client(credentials=CREDENTIALS)
BQ_STAGING_DATASET_ID = 'staging_dataset_id_here'
BQ_STAGING_TABLE_ID = 'staging_table_id_here'
BQ_CLEANED_DATASET_ID = 'cleaned_dataset_id_here'
BQ_CLEANED_TABLE_ID = 'cleaned_table_id_here'
