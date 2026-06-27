import json
from datetime import datetime, timezone, timedelta

wib = timezone(timedelta(hours=7))
updated = datetime.now(tz=wib).strftime("%d %B %Y, %H:%M WIB")
day_name = datetime.now(tz=wib).strftime("%A, %d %B %Y")

with open("papers.json", encoding="utf-8") as f:
    papers = json.load(f)

def esc_md(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()

rows = ""
for p in papers:
    title = esc_md(p.get("title", "—"))
    author = esc_md(p.get("author", "—"))
    year = p.get("year", "—")
    url = p.get("url", "")
    link = f"[📄 Read]({url})" if url else "—"
    rows += f"| {title} | {author} | {year} | {link} |\n"

readme = f"""# 📚 Daily Research Feed

> Automated aggregator of scientific papers on **IoT, Embedded Systems, Machine Learning, Deep Learning, and Electrical Engineering.**
> Auto-updated daily via [ArXiv](https://arxiv.org/) API.

---

## ⚠️ Disclaimer

- This repo is an automated aggregator, **not affiliated** with any institution or publisher
- All papers are sourced from **[ArXiv](https://arxiv.org/)**, an open-access repository of scientific preprints
- Copyright of each paper belongs to its respective authors and publishers
- Topics: IoT, Embedded Systems, ESP32, Raspberry Pi, Sensor, Automation, ML, DL, AI

---

## 🗓️ {day_name}

| Title | Author | Year | Link |
|:------|:-------|:----:|:----:|
{rows}
---

## 📂 Data

| File | Description |
|:---|:---|
| 📄 [papers.json](./papers.json) | Latest raw paper data |
| 📁 [history/](./history) | Daily snapshots |

---

<sub>⚙️ Automated by [GitHub Actions](../../actions) · Source: ArXiv API · Updated: {updated}</sub>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README.md generated successfully")
