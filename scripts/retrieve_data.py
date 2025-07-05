import os
import requests
from time import sleep

from constants import (
    BASE_URL,
    DATA_DIR,
    START_YEAR,
    END_YEAR,
    MAX_RETRIES,
    RETRY_DELAY,
)

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def download_with_retries(url: str, file_path: str) -> bool:
    """
    Attempt to download a file with retry logic on failure.
    Saves the file to file_path if successful.

    Args:
        url (str): The URL to download from.
        file_path (str): Local path to save the file.

    Returns:
        bool: True if successful, False if all retries failed.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Saved to: {file_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt} failed for {url}: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                sleep(RETRY_DELAY)
    print(f"❌ Failed after {MAX_RETRIES} attempts: {url}")
    return False


def retrieve_data(start_year: int = START_YEAR, end_year: int = END_YEAR) -> None:
    """
    Iterates over all months between start_year and end_year (inclusive)
    Downloads ZIP files containing flight data to the local data directory.

    Args:
        start_year (int): Starting year (inclusive)
        end_year (int): Ending year (inclusive)
    """
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # Build download URL and local file path
            url = BASE_URL.format(year=year, month=month)
            file_name = f"{year}_{month}.zip"
            file_path = os.path.join(DATA_DIR, file_name)

            # Skip if file already exists locally
            if os.path.exists(file_path):
                print(f"✅ Already downloaded: {file_name}")
                continue

            print(f"⬇️ Downloading: {url}")
            success = download_with_retries(url, file_path)

            # Sleep between downloads to avoid overloading the server
            if success:
                sleep(1)


if __name__ == "__main__":
    retrieve_data()
