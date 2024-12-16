# crawling_scraping
Some scripts I used to crawl and or scrape websites

## Scraping with Selenium (dynamic web-pages):
- using the script **tagi_comment_scraper.py**, the comments of articles from a swiss newspaper sites can be scraped.
- it clicks away the cookie consent button
- it clicks away some subscription popup, if it appears
- it clicks a button to display the comments and scrapes them to a html file.

- for your own page, the paths to the buttons will have to be adjusted, of course.

## Simpler crawling and scraping, for example for a static forum-style website

- using **simple_crawler_example.py**, you can search for all urls posessing a certain format.
- using **simple_scraper_example.py**, you can scrape the given pages, downloading the entire html.
- using **get_data_from_html.py**, you can adapt it to extract the metadata relevant to you.
