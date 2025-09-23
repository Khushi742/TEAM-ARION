import requests
import nltk
nltk.download('vader_lexicon')
from bs4 import BeautifulSoup
from nltk.stem import RegexpStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import time

# Custom regex stemmer (basic rules for FS parts)
regexp_stemmer = RegexpStemmer(r'(ing$|ous$|s$)')
# Sentiment analyzer
sia = SentimentIntensityAnalyzer()
# Helper Functions
def stem_query(query: str) -> str:
    """
    Break query into words and apply regex stemming to normalize search.
    Example: 'brakes' -> 'brake'
    """
    words = query.split()
    return " ".join([regexp_stemmer.stem(w) for w in words])

def analyze_sentiment(text: str) -> dict:
    """
    Analyze text (usually product description) for sentiment polarity.
    Returns a dict with neg/neu/pos/compound scores.
    """
    return sia.polarity_scores(text)

def fetch_results(url: str) -> list:
    """
    Fetch product listings from a given supplier URL.
        """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f" Failed to fetch {url}, status {resp.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f" Request error: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # Rough placeholder selectors (to be adapted per supplier site)
    for item in soup.select(".product-item"):
        name = item.select_one(".product-title").get_text(strip=True) if item.select_one(".product-title") else "N/A"
        desc = item.select_one(".product-desc").get_text(strip=True) if item.select_one(".product-desc") else ""
        sentiment = analyze_sentiment(desc)

        results.append({
            "name": name,
            "description": desc,
            "sentiment": sentiment,
            "source": url
        })

    return results


def save_results(query: str, results: list) -> None:
    """
    Save all search results into a JSON file.
    """
    filename = f"fs_results_{query.replace(' ', '_')}.json"
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
print("Saved results to results.json")

# Main Flow

def main():
    query = input("Enter the FS part you’re searching for: ")
    stemmed_query = stem_query(query)

    suppliers = [
        f"https://altairone.com/Marketplace={stemmed_query}",
        f"https://www.vi-grade.com/en/products/vi-motorsport/={stemmed_query}"
    ]

    all_results = []
    for url in suppliers:
        print(f" Fetching from {url} ...")
        results = fetch_results(url)
        all_results.extend(results)
        time.sleep(1)  # respectful delay

    if all_results:
        save_results(stemmed_query, all_results)
    else:
        print("No results found.")


if __name__ == "__main__":
    main()
