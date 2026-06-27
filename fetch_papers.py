import json
import requests
import random
import time
import xml.etree.ElementTree as ET

QUERIES = [
    "IoT Internet of Things sensor",
    "embedded systems microcontroller",
    "ESP32 WiFi sensor",
    "Raspberry Pi automation",
    "machine learning IoT",
    "deep learning neural network embedded",
    "random forest classification sensor",
    "smart home automation control",
    "edge computing IoT device",
    "artificial intelligence embedded system",
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
            published = entry.find("atom:published", ns)
            link = entry.find("atom:id", ns)

            # Parse authors
            author_names = []
            for a in entry.findall("atom:author", ns):
                name_el = a.find("atom:name", ns)
                if name_el is not None and name_el.text:
                    author_names.append(name_el.text.strip())

            title_str = " ".join(title.text.split()) if title is not None else "—"
            if len(author_names) > 1:
                author_str = author_names[0] + " et al."
            elif len(author_names) == 1:
                author_str = author_names[0]
            else:
                author_str = "Unknown"

            year = published.text[:4] if published is not None else "—"
            url_str = link.text.strip() if link is not None else ""

            papers.append({
                "title": title_str,
                "author": author_str,
                "year": year,
                "url": url_str,
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
    time.sleep(3)

random.shuffle(all_papers)
all_papers = all_papers[:10]

with open("papers.json", "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(f"Total fetched: {len(all_papers)} papers")
