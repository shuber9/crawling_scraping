# this is a webscraper that scrapes the websites you provide in a txt file (tested on a static forum) and saves 
# the contents to a html file each. Not the most memory-efficient way to do it, but you have all the data and can 
# decide how to proceed from there.

import requests
from bs4 import BeautifulSoup

# File paths
input_file = "urls.txt"  # Input file containing the list of start URLs
output_folder = "data"       # Output folder to save scraped HTML files

# Read URLs from the input file
with open(input_file, "r") as file:
    start_urls = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace

# Process each URL in the input file
for start_url in start_urls:
    print(f"Processing URL: {start_url}")
    
    try:
        response = requests.get(start_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        #print(f"Successfully fetched {start_url}")

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        output_file = f"{output_folder}/{title}.html"
        
        # Save the HTML content to a file
        try:
            with open(output_file, "w") as file:
                file.write(str(soup))
        except FileNotFoundError:
            print(f"File {output_file} does not exist. Skipping...")
            continue

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {start_url}: {e}")

print("Finished processing all URLs.")