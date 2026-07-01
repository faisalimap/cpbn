import os
import requests
import json
from datetime import datetime

# CPBN Network Configurations
CHANNEL_NAME = "CPBN"
CATEGORY = "business"
LANGUAGE = "en"

# Fetching token from secure GitHub environment secret
API_KEY = os.environ.get("NEWS_API_KEY")

def fetch_business_news():
    # Utilizing GNews or standard top-headline API streams
    url = f"https://gnews.io/api/v4/top-headlines?category={CATEGORY}&lang={LANGUAGE}&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        articles_list = []
        
        if "articles" in data:
            for item in data["articles"][:12]:  # Keep the top 12 fresh business stories
                articles_list.append({
                    "title": item.get("title"),
                    "desc": item.get("description"),
                    "image": item.get("image") or "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=800",
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("name", "ISBC Wire"),
                    "date": item.get("publishedAt")[:10] if item.get("publishedAt") else str(datetime.now().date())
                })
            return articles_list
        else:
            print("API Response status error or quota limit reached.")
            return []
    except Exception as e:
        print(f"Network exceptions encountered during compilation: {e}")
        return []

def main():
    print(f"Initializing {CHANNEL_NAME} automated collection engine...")
    articles = fetch_business_news()
    
    # Structure data file mapping
    payload = {
        "channel": CHANNEL_NAME,
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M Local"),
        "en": articles
    }
    
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)
    print("Database news.json successfully rewritten.")

if __name__ == "__main__":
    main()
