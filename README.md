**Pre-requisites:**
1. Install the required packages from requirements.txt file, e.g. "pip install -r requirements.txt" in a terminal.
2. Sign up on OpenWeatherMap.org for free API key.
3. Set up a Google Cloud Storage bucket.
4. Create a Google Cloud service account
5. Set up Google Cloud BigQuery with two datasets and tables (1 each for staging and cleaned data)
- Schema for the cleaned table:
    - location: STRING 
    - country: STRING
    - longitude: FLOAT 
    - latitude: FLOAT 
    - weather_description: STRING 
    - temperature: FLOAT 
    - feels_like: FLOAT 
    - humidity: FLOAT 
    - wind_speed: FLOAT 
    - clouds: FLOAT 
    - date: DATE 
    - time: TIME
4. Set the following environment variables:
   - **API Key**
     - On Windows: set API_KEY=value
     - On macOS/Linux: export API_KEY=value
   - **Google Application Credentials**
     - On Windows: set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\service-account-file.json
     - On macOS/Linux: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
5. Update the config.py file so that it matches API, GCP settings and locations used.

**How to use:**
Run the Main.py file to execute the entire pipeline.
