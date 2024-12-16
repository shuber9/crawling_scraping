# get the relevant info out of the html files
# the data is in the folder data

import os
import re
from bs4 import BeautifulSoup

# File paths
folder = "data"  # Folder containing the HTML files
output_folder = "data_cleaned"  # Output folder to save cleaned text files

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
with open("data_1.tsv", "w") as outfile:
    outfile.write("link\ttitle\tauthor\tcontent\tyour\tmetadata\there\n")
    # the extraction methods below are just examples

# Process each HTML file in the input folder
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            # what file is being processed
            print(f"Processing file: {filename}")
            input_file = os.path.join(folder, filename)
            output_file = os.path.join(output_folder, filename.replace(".html", ".txt"))

            with open(input_file, "r") as file:
                soup = BeautifulSoup(file, "html.parser")
                with open(input_file, "r") as file2:
                    full_html = file2.readlines()
                    full_html = "".join(full_html)
                    
                    # Extract the relevant text from the HTML
                    # text to extract is, for example, in div class ="bbWrapper"
                    content = soup.find_all("div", class_="bbWrapper")
                    # remove empty lines from the content
                    content_clean = " ".join([tag.get_text(strip=True) for tag in content if tag.get_text(strip=True)])
                    content_clean = re.sub(r'(?<=[.!?])(?=[^\s])', ' ', content_clean)
                    # get the link to the article
                    link = soup.find("link", rel="canonical")
                    link = link.get("href")

                    # get the title of the article
                    title_tag = soup.find("meta", property="og:title")
                    title = title_tag.get("content")

                    # get the author
                    author_tag = soup.find("span", class_="memberlinks-link username u-concealed")
                    if author_tag is None:
                        author = "Guest"
                    else:
                        author = author_tag.get_text(strip=True)

                    # save all of it to a tsv file
                    outfile.write(f"{link}\t{title}\t{author}\t{content_clean}\tyour\tmetadata\there\n")