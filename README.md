TEAM-ARION Webscraper
=> A Python-based tool that fetches FS car part data from multiple e-commerce websites.
 It lets users search for parts (e.g., “brake pads”), splits queries into keywords, and scrapes results into a single JSON file for easier access.

Tech Stack & Tools
Python → Core language for building the scraper
Requests → Sending HTTP requests to websites
BeautifulSoup (bs4) → Parsing and extracting product names, links, and prices
JSON → Exporting search results in a structured format
Git & GitHub → Version control and collaboration
Command Line / Terminal → Running the scraper



How to Run
1. Clone the repo:

 git clone https://github.com/Khushi742/TEAM-ARION.git
cd TEAM-ARION
Create a virtual environment (optional but recommended):

 python -m venv .venv
            .venv\Scripts\activate      # Windows
2.
Install dependencies:

 pip install -r requirements.txt

3. Run the scraper:

 python webscraper.py

4. Enter the part name (e.g., brake pads).

5. Results will be saved in results.json.
   <img width="888" height="444" alt="image" src="https://github.com/user-attachments/assets/a704af7d-2140-4d18-9fe2-b3165116d948" />


Features Implemented
Multi-site scraping → Requests + BeautifulSoup extract results from:
1. PartFinder
2. MotrParts
3. Carorbis

Keyword-based search mapping → Splits queries ("brake pads") into separate terms ("brake", "pads") and searches each word individually.
404 handling & robust requests → Fixed broken URLs by correcting query parameters.
Data persistence → Results saved into JSON using Python’s json library.
Error handling → Clean messages when no results are found.



Work in Progress / Next Steps
Add support for more FS-related e-commerce websites.
Implement caching to avoid repeated requests for the same query.
Build a lightweight UI (Flask or Streamlit) instead of CLI.
Add pagination handling for deeper search results.



--Design & Tech Decisions--
BeautifulSoup chosen over Scrapy → Lightweight, faster to implement, less overhead.
Requests chosen over Selenium → Simple and efficient since sites didn’t require heavy JS rendering.
Saved JSON output → Chose JSON instead of CSV for easier integration with future apps/APIs.
Query splitting → Added to make searches broader and catch results even if exact phrases don’t match.



Testing
Manual testing: Ran queries like brake, pads, suspension. Verified that results were parsed and stored correctly.
404 test: Entered invalid URLs to check error handling (returns clean error message).
Edge cases: Tested empty input, invalid words (e.g., “abcdef”), ensured no crashes.
<img width="1004" height="247" alt="image" src="https://github.com/user-attachments/assets/6e68d210-7475-4e88-8283-e894d464f2ed" />




Demo
CLI Example:

 Enter the FS part you’re searching for: brake pads
Fetching from https://www.partfinder.in/search?query=brake ...
Fetching from https://www.motrparts.com/?s=brake&post_type=product ...
Fetching from https://carorbis.com/tools-and-garage/?s=brake ...
Results saved to results.json

–Example JSON output:--

 [
  {
    "site": "PartFinder",
    "name": "Brake Pad Set",
    "link": "https://www.partfinder.in/product/123",
    "price": "₹1200"
  }
]



--Reflections & Learnings--
Learned how to build a robust scraper using Requests + BeautifulSoup.
Learned about query parameter structures (?s=keyword&post_type=product) and fixing 404s.
Learned how to save results in JSON for integration with future projects.



--Stretch Goals--
Add search ranking/weightage to prioritise best matches.
Deploy on cloud (Heroku/Render) for remote usage.




