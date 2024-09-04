import os
import requests
import certifi
import ssl
import geopy
import csv
from geopy.geocoders import Nominatim
import config

# Set SSL context so that geopy works as intended
ssl_context = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ssl_context
geolocator = Nominatim(user_agent="weather_script")


def run():
    try:
        print("---------- Running extract_data.py ----------")
        all_locations = get_locations()

        if not all_locations:
            print("No valid locations were entered.")
            return

        weather_data_list = get_weather_data(all_locations)

        if not weather_data_list:
            print("No weather data was retrieved.")
            return

        create_local_file(weather_data_list)
        upload_file_to_gcs()
        remove_local_file()
    except Exception as error:
        print(f'Error: {error}')


def get_locations():
    location_names = [location.strip() for location in config.LOCATIONS.split(',')]

    all_locations = []
    for name in location_names:
        location = geolocator.geocode(name)

        if location is None:
            print(f"{name} could not be found.")
        else:
            all_locations.append((location.longitude, location.latitude, name))

    return all_locations


def get_weather_data(locations):
    # Retrieves weather data using the API
    weather_data_list = []

    for lon, lat, location_name in locations:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.API}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:  # If the request was successful
            print(f"API request for {location_name} was successful.")
            data = response.json()  # Parse the JSON response
            weather_data = extract_weather_data(data, location_name)
            weather_data_list.append(weather_data)
        else:
            print(f"Error: {response.status_code} - {response.reason} for location {location_name}")

    return weather_data_list


def extract_weather_data(weather_data, location_name):
    return {
        "location": location_name,
        "country": weather_data['sys']['country'],
        "longitude": weather_data['coord']['lon'],
        "latitude": weather_data['coord']['lat'],
        "weather_description": weather_data['weather'][0]['description'],
        "temperature": weather_data['main']['temp'],
        "feels_like": weather_data['main']['feels_like'],
        "humidity": weather_data['main']['humidity'],
        "wind_speed": weather_data['wind']['speed'],
        "clouds": weather_data['clouds']['all'],
        "date": config.DATE,
        "time": config.TIME
    }


def create_local_file(weather_data_list):
    # Creates a local .csv file with the data from the API
    try:
        with open(config.FILENAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "location", "country", "longitude", "latitude", "weather_description",
                "temperature", "humidity", "feels_like", "wind_speed", "clouds", "date", "time"
            ])
            writer.writeheader()
            for weather_data in weather_data_list:
                writer.writerow(weather_data)

        print(f"Local file {config.FILENAME} was created.")

    except IOError as e:
        print(f"File I/O error: {e}")


def upload_file_to_gcs():
    # Uploads the file to Google Cloud Storage
    try:
        config.GCS_BLOB.upload_from_filename(config.FILENAME)
        print(f'{config.FILENAME} was uploaded to Google Cloud Storage.')

    except Exception as e:
        print(f"Error uploading to Google Cloud Storage: {e}")


def remove_local_file():
    os.remove(config.FILENAME)
    print(f"Local file {config.FILENAME} has been deleted.")
