import os
from google.cloud import bigquery
import config


def run():
    print("---------- Running transform_and_load.py ----------")
    try:
        check_environment_variables()
    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}")
        return

    load_to_staging_table()
    load_to_cleaned_table()


def check_environment_variables():
    if not config.API:
        raise ValueError("Environment variable 'API_KEY' is not set or is empty.")

    if not config.CREDENTIALS_PATH:
        raise ValueError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set or is empty.")

    if not os.path.isfile(config.CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"The file specified by 'GOOGLE_APPLICATION_CREDENTIALS' does not exist: {config.CREDENTIALS_PATH}")


def load_to_staging_table():
    # Loads data from Google Cloud Storage to the BigQuery table
    try:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # First row = header
            autodetect=True)

        load_job = config.BQ_CLIENT.load_table_from_uri(
            config.GCS_URI,
            f'{config.BQ_STAGING_DATASET_ID}.{config.BQ_STAGING_TABLE_ID}',
            job_config=job_config
        )

        load_job.result()
        print(f"Loaded data into {config.BQ_STAGING_DATASET_ID}.{config.BQ_STAGING_TABLE_ID}.")
    except Exception as error:
        print(f"Error loading data into BigQuery staging table: {error}")


def load_to_cleaned_table():
    # Loads data from the staging table to the cleaned table, the WHERE clause is to prevent duplicate records
    try:
        sql = f'''
        INSERT INTO {config.BQ_CLEANED_DATASET_ID}.{config.BQ_CLEANED_TABLE_ID} (location, country, longitude, latitude,
            weather_description, temperature, feels_like, humidity, wind_speed, clouds, date, time)
        
        SELECT s.location, s.country, s.longitude, s.latitude, 
            COALESCE(s.weather_description, 'Missing') as weather_description,
            s.temperature,
            COALESCE(s.feels_like, s.temperature) as feels_like,
            s.humidity, s.wind_speed, s.clouds,
            s.date, s.time
        FROM {config.BQ_STAGING_DATASET_ID}.{config.BQ_STAGING_TABLE_ID} s
        LEFT JOIN {config.BQ_CLEANED_DATASET_ID}.{config.BQ_CLEANED_TABLE_ID} c
            ON s.location = c.location
            and s.country = c.country
            and s.longitude = c.longitude
            and s.latitude = c.latitude
            and s.weather_description = c.weather_description
            and s.temperature = c.temperature
            and s.feels_like = c.feels_like
            and s.humidity = c.humidity
            and s.wind_speed = c.wind_speed
            and s.clouds = c.clouds
            and s.date = c.date
            and s.time = c.time
        WHERE c.location IS NULL
        '''

        query_job = config.BQ_CLIENT.query(sql)
        query_job.result()
        print(f'Loaded data into cleaned table {config.BQ_CLEANED_DATASET_ID}.{config.BQ_CLEANED_TABLE_ID}.')
    except Exception as error:
        print(f"Error loading data into BigQuery cleaned table: {error}")
