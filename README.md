Hi!
This is my personal ETL/weather data pipeline project:
- Retrieves weather data from OpenWeatherMap's free API
- Creates a local .csv file with weather data
- Uploads the .csv file to Google Cloud Storage (GCS)
- Loads a BigQuery staging table with data from GCS
- Transform data into a cleaned BigQuery table

**Pre-requisites:**
1. Install the required packages from requirements.txt file. 
This can be done using "pip install -r requirements.txt" in a terminal.
2. Sign up on OpenWeatherMap.org to retrieve your free API key.
3. Google Cloud Setup
   - Set up a Google Cloud Storage bucket.
   - Create a Google Cloud service account and download the JSON key file.
   - Set up Google Cloud BigQuery datasets and tables:
     - Create one dataset and table for staging.
     - Create another dataset and table for cleaned data, you also need set a schema for the cleaned table:
       - Column names and Data Types:
        location: STRING
        country: STRING
        longitude: FLOAT
        latitude: FLOAT
        weather_description: STRING
        temperature: FLOAT
        feels_like: FLOAT
        humidity: FLOAT
        wind_speed: FLOAT
        clouds: FLOAT
        date: DATE
        time: TIME
4. Set the following environment variables:
   - **API Key**
     - On Windows: set API_KEY=value
     - On macOS/Linux: export API_KEY=value
   - **Google Application Credentials**
     - On Windows: set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\service-account-file.json
     - On macOS/Linux: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
5. Update the config.py file included so that it matches your settings for the PI key, Google Cloud Storage bucket, and BigQuery datasets/tables.
- config.py is also where you set locations used

**How to use the script:**

After setting up the environment, run the Main.py file to execute the entire pipeline.


**Screenshots**

Screenshots of a successful run can be found in the folder "demo screenshots"