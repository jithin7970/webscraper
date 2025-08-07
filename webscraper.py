import requests
from bs4 import BeautifulSoup
import sys
import re

def scrape_headlines(url: str) -> list:
    """
    Scrapes headlines and their associated URLs from a given webpage.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        A list of dictionaries, where each dictionary contains 'title' and 'url' of a headline.
        Returns an empty list if no headlines are found or an error occurs.
    """
    if not url.startswith("http"):
        print("Invalid URL. Please provide a complete URL including http:// or https://.")
        return []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # A more comprehensive selector for headlines that also finds the anchor tag (<a>)
    headline_elements = soup.select('h1 a, h2 a, h3 a, a[class*="headline"], a[class*="title"]')
    
    data = []
    seen_urls = set()

    for element in headline_elements:
        text = element.get_text(strip=True)
        link = element.get("href")
        
        # Check if the link is relative and make it absolute
        if link and not link.startswith("http"):
            link = requests.compat.urljoin(url, link)
            
        if text and link and link not in seen_urls:
            data.append({"title": text, "url": link})
            seen_urls.add(link)

    return data

def scrape_article_content(url: str) -> str:
    """
    Scrapes the main article content from a given article URL.

    Args:
        url: The URL of the article to scrape.

    Returns:
        The cleaned article content as a single string.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching article content: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Common selectors for article content
    content_selectors = [
        "div.article-content", "div.story-body", "div.entry-content", "div#main-content p"
    ]
    
    article_content = []
    for selector in content_selectors:
        paragraphs = soup.select(selector + " p")
        if paragraphs:
            article_content = [p.get_text(strip=True) for p in paragraphs]
            break
            
    if not article_content:
        return "Could not find article content."
    
    return "\n\n".join(article_content)

def main():
    """
    Main function to orchestrate the scraping process.
    """
    url = input("Enter or paste the URL of a news site: ").strip()
    if not url:
        print("No URL entered. Exiting.")
        sys.exit()

    print("Scraping headlines...")
    headlines_data = scrape_headlines(url)

    if not headlines_data:
        print("No headlines were found. Please check the URL or page structure.")
        return

    # Save headlines to one file
    with open("scraped_headlines.txt", "w", encoding="utf-8") as file:
        for item in headlines_data:
            file.write(f"Title: {item['title']}\nURL: {item['url']}\n\n")
    
    print(f"Successfully scraped {len(headlines_data)} headlines. They have been saved to 'scraped_headlines.txt'.")
    
    # Scrape and save content to a separate file
    print("Now scraping content for each article...")
    with open("scraped_content.txt", "w", encoding="utf-8") as file:
        for i, item in enumerate(headlines_data):
            print(f"Scraping content for: {item['title']} ({i+1}/{len(headlines_data)})")
            content = scrape_article_content(item['url'])
            file.write(f"--- Article: {item['title']} ---\n")
            file.write(content + "\n\n")
    
    print("\nAll article content has been saved to 'scraped_content.txt'.")

if __name__ == "__main__":
    main()