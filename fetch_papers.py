import json
import requests
from datetime import datetime, timezone, timedelta
import random
import time

wib = timezone(timedelta(hours=7))

QUERIES = [
    "IoT sensor",
    "machine learning",
    "deep learning",
    "embedded systems",
    "microcontroller",
    "artificial intelligence",
    "neural network",
    "automation control",
    "smart sensor",
    "edge computing",
]

def fetch_papers(query, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,url",
    }
    headers = {
        "User-Agent": "daily-research-bot/1.0"
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        print(f"Query '{query}': status {r.status_code}")
        if r.status_code == 200:
            data = r.json().get("data", [])
            print(f"  -> {len(data)} papers")
            return data
        else:
            print(f"  -> Error: {r.text[:200]}")
            return []
    except Exception as e:
        print(f"  -> Exception: {e}")
        return []

# Ambil dari 3 query random
selected_queries = random.sample(QUERIES, 3)
all_papers = []
seen_ids = set()

for q in selected_queries:
    papers = fetch_papers(q, limit=5)
    for p in papers:
        pid = p.get("paperId", "")
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            all_papers.append(p)
    time.sleep(1)  # hindari rate limit

# Shuffle dan ambil max 10
random.shuffle(all_papers)
all_papers = all_papers[:10]

with open("papers.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(f"Total fetched: {len(all_papers)} papers")
