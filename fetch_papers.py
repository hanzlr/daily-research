import json
import requests
import random
import time
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET

wib = timezone(timedelta(hours=7))

QUERIES = [
    "IoT sensor embedded",
    "machine learning classification",
    "deep learning neural network",
    "ESP32 microcontroller",
    "Raspberry Pi automation",
    "artificial intelligence",
    "random forest classification",
    "smart home automation",
    "edge computing embedded",
    "sensor fusion IoT",
]

def fetch_arxiv(query, max_results=5):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        print(f"Query '{query}': status {r.status_code}")
        if r.status_code != 200:
            return []

        root = ET.fromstring(r.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            authors = entry.findall("atom:author", ns)
            published = entry.find("atom:published", ns)
            link = entry.find("atom:id", ns)
            abstract = entry.find("atom:summary", ns)

            title_str = title.text.strip().replace("\n", " ") if title is not None else "—"
            author_list = [a.find("atom:name", ns).text for a in authors if a.find("atom:name", ns) is not None]
            author_str = author_list[0] + " et al." if len(author_list) > 1 else author_list[0] if author_list else "—"
            year = published.text[:4] if published is not None else "—"
            url_str = link.text.strip() if link is not None else ""
            abstract_str = abstract.text.strip().replace("\n", " ")[:200] + "..." if abstract is not None else "—"

            papers.append({
                "title": title_str,
                "author": author_str,
                "year": year,
                "url": url_str,
                "abstract": abstract_str,
            })

        print(f"  -> {len(papers)} papers")
        return papers

    except Exception as e:
        print(f"  -> Exception: {e}")
        return []

# Ambil dari 3 query random
selected_queries = random.sample(QUERIES, 3)
all_papers = []
seen_urls = set()

for q in selected_queries:
    papers = fetch_arxiv(q, max_results=5)
    for p in papers:
        url = p.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            all_papers.append(p)
    time.sleep(3)  # hindari rate limit

# Shuffle dan ambil max 10
random.shuffle(all_papers)
all_papers = all_papers[:10]

with open("papers.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(f"Total fetched: {len(all_papers)} papers")
