import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
import time
import argparse
import re
import os

# Function to create a safe filename from a URL
def url_to_filename(url):
    return re.sub(r'\W+', '_', url)  # Replace non-alphanumeric characters with underscores

# Function to process a single URL
def process_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)
    time.sleep(2)

    try:
        # Handle the cookie consent button if present
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
        )
        cookie_button.click()
        print("Cookie consent accepted.")
    except Exception as e:
        print("[Info] No cookie consent button found or click failed:", e)

    # Scroll halfway down the page initially
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)

    try:
        # Handle any intercepting modal/button if present
        intercepting_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="tp-close tp-active"]'))
        )
        intercepting_button.click()
        print("Intercepting button clicked.")
        time.sleep(5)
    except Exception as e:
        print("[Info] No intercepting button found or click failed:", e)

    # Generate all possible button XPaths within divs 5 to 50
    button_xpaths = [f'//*[@id="main"]/article/div[{i}]/button' for i in range(5, 51)]

    # Scrolling and clicking parameters
    scroll_increment = 1500
    current_position = 0
    end_of_page = driver.execute_script("return document.body.scrollHeight")
    max_scroll_attempts = 20
    scroll_pause_time = 0.05  # Very short pause between scrolls to speed up

    button_clicked = False

    # Try each button XPath in the specified range
    for xpath in button_xpaths:
        try:
            # Locate the button with the current XPath
            button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # Attempt to click the button
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.1)  # Minimal delay to ensure the button scrolls into view
            button.click()
            print(f"Target button clicked with XPath: {xpath}")
            time.sleep(0.2)  # Short pause to ensure the click registers
            button_clicked = True
            break  # Exit the loop if the button was clicked successfully
        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException):
            continue  # If this XPath didn't work or button not found, try the next one

    # Handle case where no button was found
    if not button_clicked:
        print("No target button found within the specified div range.")

    # Extract and save the "comments" div content
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    comments_div = soup.find("div", id="comments")

    filename = f"{url_to_filename(url)}_comments_section.html"
    if comments_div:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(comments_div.prettify())
        print(f"Comments section downloaded and saved as '{filename}'")
    else:
        print("[Warning] No div with id='comments' found.")

    driver.quit()

# Main function to parse arguments and process each URL in the file
def main():
    parser = argparse.ArgumentParser(description="Process a list of URLs and download specific div content.")
    parser.add_argument("url_file", help="Path to the text file containing a list of URLs")
    args = parser.parse_args()

    # Check if the file exists
    if not os.path.isfile(args.url_file):
        print(f"[Error] File '{args.url_file}' does not exist.")
        return

    # Open the file and process each URL
    with open(args.url_file, "r") as file:
        for line in file:
            url = line.strip()
            if url:
                print(f"Processing URL: {url}")
                process_url(url)
            else:
                print("[Warning] Empty line in URL file, skipping.")

if __name__ == "__main__":
    main()
