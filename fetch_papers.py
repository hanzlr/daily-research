import json
import requests
import random
import time
import xml.etree.ElementTree as ET

# Kategori ArXiv yang relevan ke IoT, Embedded, ML, Electrical
CATEGORY_QUERIES = [
    ("cat:eess.SY", "Systems & Control"),
    ("cat:eess.SP", "Signal Processing"),
    ("cat:cs.LG", "Machine Learning"),
    ("cat:cs.AI", "Artificial Intelligence"),
    ("cat:cs.RO", "Robotics"),
    ("cat:eess.SY+AND+all:IoT", "IoT Systems"),
    ("cat:eess.SY+AND+all:embedded", "Embedded Systems"),
    ("cat:cs.LG+AND+all:sensor", "ML Sensor"),
    ("cat:cs.RO+AND+all:automation", "Automation"),
    ("cat:eess.SP+AND+all:microcontroller", "Microcontroller"),
]

def fetch_arxiv(query, max_results=5):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
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

# Ambil dari 3 kategori random
selected = random.sample(CATEGORY_QUERIES, 3)
all_papers = []
seen_urls = set()

for query, label in selected:
    print(f"\n--- {label} ---")
    papers = fetch_arxiv(query, max_results=5)
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

print(f"\nTotal fetched: {len(all_papers)} papers")
