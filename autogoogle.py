from googlesearch import search
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_page_title(url):
    # I found that using a fake header is able to dodge bot detection a little better!
    # instantiates a fake user agent for each script call
    ua = UserAgent()
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua.random
    }
    #feeds urls into beautifulsoup to get webpage titles...
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No Title Available'
        return title
    #TODO: Figure out ways to make sense of the timeout errors as well as 403 Errors (most of which are likely bot-detection)
    #use some kind of logging api to track the process before the error is hit
    except requests.exceptions.Timeout:
        return "Error fetching Website Title: Request timed out"
    except requests.exceptions.RequestException as e:
        return f"Error fetching Website Title: {e}"

def is_sponsored(url):
    ad_keywords = ["adurl", "gclid", "utm_source", "utm_campaign", "sponsored", "aff"]
    return any(keyword in url.lower() for keyword in ad_keywords)

def google_search(query, num_results):
    print(f"Searching Google For : {query}")
    results = search(query, num_results)
    for i, url in enumerate(results, start=1):
        title = get_page_title(url)
        sponsored = " (Sponsored)" if is_sponsored(url) else ""
        print(f"{i}. {title} | {url}")
    #TODO: Figure out how to flag Ads?

if __name__ == "__main__":
    query = input("Enter your search query: ")
    num_results = input("Enter the desired number of results to fetch: ")
    try:
        num_results = int(num_results)
    except ValueError:
        print("Invalid input for number of results. Using default value (10).")
        num_results = 10
    google_search(query, num_results)

