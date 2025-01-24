The DSA Transparency Database Analysis Tools provide researchers with the ability to analyze content moderation data from the Digital Services Act Transparency Database (https://transparency.dsa.ec.europa.eu/). 
The tools consist of three Python scripts that work together to download and filter Statements of Reasons (SORs) issued by online platforms.


The first script, dsa_downloader.py, provides core functionality for downloading SOR data files from the database. 
The second script, DSA_SOR_DOWNLOAD_RUNNING FILE.py, serves as a runner to execute downloads with specified parameters like date ranges and platforms. 
The third script, dsa_filtering.py, rely on keywords to filter the SORs.

To use these tools, Python 3.7+ is required along with the pandas, requests, tqdm and pathlib libraries. 
The workflow involves first configuring and running the download script to obtain SOR data for specific platforms and date ranges. 
This data can then be analyzed using the filtering script to search for specific keywords and export matching results.

The code was developed with the assistance of Claude 3.5 Sonnet. It is released under the European Union Public License 1.2 (EUPL-1.2).
The tools were used to write the paper : "Empty Transparency?  Assessing Platform Content Moderation of False Information Through the DSA Transparency Database", to be published. 
