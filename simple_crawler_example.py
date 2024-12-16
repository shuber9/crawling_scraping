import requests
from bs4 import BeautifulSoup

# File paths
input_file = "input_urls.txt"  # Input file containing the list of start URLs
output_file = "urls.txt"       # Output file to append discovered URLs

# Read URLs from the input file
with open(input_file, "r") as file:
    start_urls = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace

# Process each URL in the input file
for start_url in start_urls:
    print(f"Processing URL: {start_url}")

    try:
        response = requests.get(start_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        print(f"Successfully fetched {start_url}")

        soup = BeautifulSoup(response.content, "html.parser")
        link_elements = soup.select("a[href]")

        discovered_urls = []

        for link_element in link_elements:
            url = link_element['href']
            # some custom logic, adapt to your needs
            if "url_part_2" in url:
                if not "url_unwanted_filter" in url:
                    if not url == "/url_part_2/":
                        discovered_urls.append(url)
            else:
                #print(f"Ignored external link: {url}")
                continue

        # Append the discovered URLs to the output file
        with open(output_file, "a") as outfile:
            for url in discovered_urls:
                outfile.write("https://www.your_url.com" + url + "\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {start_url}: {e}")

print("Finished processing all URLs.")
