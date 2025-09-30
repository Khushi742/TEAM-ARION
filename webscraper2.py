import requests
import nltk
from bs4 import BeautifulSoup
from nltk.stem import RegexpStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import time

# Check if vader_lexicon is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Error: vader_lexicon not found. Run 'import nltk; nltk.download(\"vader_lexicon\")' once before using this script.")
    exit(1)

# Custom regex stemmer (basic rules for FS parts)
regexp_stemmer = RegexpStemmer(r'(ing$|ous$|s$)')
# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

# ---------------------- Helper Functions ----------------------

def stem_query(query: str) -> str:
    """Stem a single query word."""
    return regexp_stemmer.stem(query)

def analyze_sentiment(text: str) -> dict:
    """Analyze text for sentiment polarity."""
    return sia.polarity_scores(text)

def fetch_reviews(item) -> list:
    """
    Fetch and analyze reviews for a product item element.
    Assumes reviews are under .review selector.
    """
    reviews = []
    for rev in item.select(".review"):
        text = rev.get_text(strip=True)
        sentiment = analyze_sentiment(text)
        reviews.append({
            "text": text,
            "sentiment": sentiment
        })
    return reviews

def fetch_results(url: str, site: str) -> list:
    """Fetch product listings from a given supplier URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"  Failed to fetch {url}, status {resp.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"  Request error for {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # --- Scraper rules per supplier ---
    if site == "motrparts":
        for item in soup.select("li.product"):
            name = item.select_one("h2.woocommerce-loop-product__title")
            desc = item.select_one("span.price")
            reviews = fetch_reviews(item)
            results.append({
                "name": name.get_text(strip=True) if name else "N/A",
                "description": desc.get_text(strip=True) if desc else "",
                "sentiment": analyze_sentiment(desc.get_text(strip=True) if desc else ""),
                "reviews": reviews,
                "source": url
            })

    elif site == "partfinder":
        for item in soup.select(".product-card"):
            name = item.select_one(".product-title")
            desc = item.select_one(".product-description")
            reviews = fetch_reviews(item)
            results.append({
                "name": name.get_text(strip=True) if name else "N/A",
                "description": desc.get_text(strip=True) if desc else "",
                "sentiment": analyze_sentiment(desc.get_text(strip=True) if desc else ""),
                "reviews": reviews,
                "source": url
            })

    elif site == "carorbis":
        for item in soup.select("li.product"):
            name = item.select_one("h2.woocommerce-loop-product__title")
            desc = item.select_one("span.price")
            reviews = fetch_reviews(item)
            results.append({
                "name": name.get_text(strip=True) if name else "N/A",
                "description": desc.get_text(strip=True) if desc else "",
                "sentiment": analyze_sentiment(desc.get_text(strip=True) if desc else ""),
                "reviews": reviews,
                "source": url
            })

    return results


def save_results(query: str, results: list) -> None:
    """
    Save all search results into a JSON file, sorted by most positive review.
    """
    # Sort products by highest review compound score (descending)
    def max_review_score(product):
        if product.get("reviews"):
            return max((r["sentiment"]["compound"] for r in product["reviews"]), default=product["sentiment"]["compound"])
        return product["sentiment"]["compound"]

    sorted_results = sorted(results, key=max_review_score, reverse=True)
    filename = f"fs_results_{query.replace(' ', '_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(sorted_results, f, indent=4, ensure_ascii=False)
    print(f" Saved results to {filename}")

# ---------------------- Main Flow ----------------------

def main():
    query = input("Enter the FS part you’re searching for: ").strip()
    if not query:
        print("No query entered.")
        return

    # Split into words and stem them
    words = query.split()
    stemmed_words = [stem_query(w) for w in words]

    # Build queries: original full phrase + individual keywords
    queries_to_run = [query] + stemmed_words

    suppliers = {
        "motrparts": "https://www.motrparts.com/?s={}&post_type=product",
        "partfinder": "https://www.partfinder.in/search?q={}",
        "carorbis": "https://www.carorbis.com/tools-and-garage/?s={}"
    }

    all_results = []
    for q in queries_to_run:
        print(f"\n Running sub-search for: {q}")
        for site, url_template in suppliers.items():
            url = url_template.format(q)
            print(f" Fetching from {site}: {url}")
            res = fetch_results(url, site)
            if res:
                print(f"  → Found {len(res)} items on {site}")
            else:
                print(f"  → No items on {site}")
            all_results.extend(res)
            time.sleep(1.0)

    if all_results:
        save_results(query, all_results)
    else:
        print("No results found across all suppliers.")


if __name__ == "__main__":
    main()
