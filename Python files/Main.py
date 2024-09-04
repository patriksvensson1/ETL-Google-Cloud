import config
import os
import extract_data
import transform_and_load


def main():
    try:
        check_environment_variables()
        extract_data.run()
        transform_and_load.run()
    except Exception as error:
        print(f"Error: {error}")
        return


def check_environment_variables():
    if not config.API:
        raise ValueError("Environment variable 'API_KEY' is not set or is empty.")

    if not config.CREDENTIALS_PATH:
        raise ValueError("Environment variable 'GOOGLE_APPLICATION_CREDENTIALS' is not set or is empty.")

    if not os.path.isfile(config.CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"The file specified by 'GOOGLE_APPLICATION_CREDENTIALS' does not exist: {config.CREDENTIALS_PATH}")


if __name__ == "__main__":
    main()
