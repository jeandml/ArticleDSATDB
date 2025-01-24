# dsa_downloader.py
import requests
from tqdm import tqdm
from datetime import datetime, timedelta
from pathlib import Path
import time


def download_data(start_date, end_date, platforms, folder="downloads", max_retries=3, retry_delay=5):
    """Download DSA data files with retry mechanism"""
    Path(folder).mkdir(exist_ok=True)
    base_url = "https://dsa-sor-data-dumps.s3.eu-central-1.amazonaws.com"

    for platform in platforms:
        current = start_date
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            url = f"{base_url}/sor-{platform}-{date_str}-full.zip"

            print(f"\nDownloading {platform} data for {date_str}")

            # Try multiple times if needed
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))

                    file_path = Path(folder) / f"{platform}_{date_str}.zip"
                    with open(file_path, 'wb') as f, tqdm(
                            desc="Downloading",
                            total=total_size,
                            unit='iB',
                            unit_scale=True
                    ) as pbar:
                        for data in response.iter_content(chunk_size=1024):
                            size = f.write(data)
                            pbar.update(size)

                    print(f"✓ Downloaded {file_path.name}")
                    break  # Success, no need to retry

                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        print(f"✗ Error downloading {platform} data for {date_str}: {e}")

            current += timedelta(days=1)