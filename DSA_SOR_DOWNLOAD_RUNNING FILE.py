from datetime import datetime
from dsa_downloader import download_data

# Set your parameters here
start_date = datetime(0000, 00, 0)  # Change to your start date
end_date = datetime(0000, 00, 0)    # Change to your end date
platform = ["platform"]                # Add the platforms' name
folder = "" # specify your download folder


# Run the download
download_data(start_date, end_date, platform, folder)