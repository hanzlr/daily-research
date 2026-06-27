import json
import requests
from datetime import datetime, timezone, timedelta
import random

wib = timezone(timedelta(hours=7))

QUERIES = [
    "IoT Internet of Things",
    "Embedded Systems microcontroller",
    "ESP32 Arduino sensor",
    "Raspberry Pi automation",
    "Machine Learning deep learning",
    "Neural Network AI artificial intelligence",
    "Random Forest classification",
    "sensor fusion data acquisition",
    "smart home automation",
    "edge computing IoT",
]

def fetch_papers(query, limit=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,externalIds,abstract,url,publicationTypes,journal",
        "sort": "relevance",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("data", [])
    except:
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

# Shuffle dan ambil max 10
random.shuffle(all_papers)
all_papers = all_papers[:10]

with open("papers.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(f"Fetched {len(all_papers)} papers")
