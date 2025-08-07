News Headlines & Article Content Scraper
A Python script that scrapes headlines and their associated URLs from a news website's homepage or section page, then scrapes and saves the main article content for each headline. This tool supports many news sites by targeting common headline and content HTML patterns.

Features
Scrapes multiple headline titles and URLs from a given news website URL.

Handles both absolute and relative URLs automatically.

Scrapes main article content text from the linked pages.

Saves all headlines and their URLs to scraped_headlines.txt.

Saves full article content to scraped_content.txt.

Robust error handling with user-friendly messages.

Uses HTTP headers (User-Agent) to mimic a regular browser.

Timeout and request error handling for reliability.

Requirements
Python 3.6+

Libraries: requests, beautifulsoup4

Install dependencies using:

bash
pip install requests beautifulsoup4
Usage
Run the script:

bash
python your_script_name.py
Enter the full URL of the news site homepage or a news section page when prompted (including http:// or https://).

The script will scrape headlines and save them to scraped_headlines.txt.

Then it will automatically scrape the content of each article linked by those headlines and save them to scraped_content.txt.