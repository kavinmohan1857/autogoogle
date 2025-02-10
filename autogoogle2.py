import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search

def get_page_title(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string.strip() if soup.title else 'No Title Available'
    except requests.exceptions.RequestException:
        return "Error: Unable to retrieve title"

def is_sponsored(url):
    ad_keywords = ["adurl", "gclid", "utm_", "sponsored", "aff"]
    return any(keyword in url.lower() for keyword in ad_keywords)

def google_search_to_dataframe(query, num_results=10):
    print(f"Searching Google for: {query}")
    results_data = []
    for i, url in enumerate(search(query, num_results=num_results), start=1):
        if i > num_results:
            break
        title = get_page_title(url)
        sponsored = is_sponsored(url)
        results_data.append({"Title": title, "URL": url, "Sponsored": sponsored})
    return pd.DataFrame(results_data)

def save_to_downloads_folder(df, filename):
    downloads_folder = os.path.expanduser("~/Downloads")
    file_path = os.path.join(downloads_folder, f"{filename}.csv")
    df.to_csv(file_path, index=False)
    print(f"Results saved to '{file_path}'.")


if __name__ == "__main__":
    query = input("Enter your search query: ")
    df = google_search_to_dataframe(query, num_results=10)
    print(df)
    save_choice = input("Do you want to save the results to your Downloads folder? (yes/no): ").strip().lower()
    if save_choice == 'yes':
        save_to_downloads_folder(df, "Google_Search_Results")
