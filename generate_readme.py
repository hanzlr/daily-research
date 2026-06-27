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
    authors = p.get("authors", [])
    author_str = esc_md(authors[0]["name"] + " et al." if len(authors) > 1 else authors[0]["name"] if authors else "—")
    year = p.get("year", "—")
    url = p.get("url", "")
    link = f"[📄 Baca]({url})" if url else "—"
    rows += f"| {title} | {author_str} | {year} | {link} |\n"

readme = f"""# 📚 Daily Research Feed

> Agregator otomatis paper & jurnal ilmiah seputar **IoT, Embedded Systems, Machine Learning, Deep Learning, dan Electrical Engineering.**
> Diperbarui otomatis setiap hari via [Semantic Scholar](https://www.semanticscholar.org/) API.

---

## ⚠️ Disclaimer

- Repo ini adalah agregator otomatis, **tidak berafiliasi** dengan institusi atau penerbit manapun
- Seluruh paper bersumber dari **[Semantic Scholar](https://www.semanticscholar.org/)** yang mengindeks ArXiv, IEEE, dan jurnal ilmiah lainnya
- Hak cipta paper sepenuhnya milik penulis & penerbit masing-masing
- Fokus topik: IoT, Embedded Systems, ESP32, Raspberry Pi, Sensor, Automation, ML, DL, AI

---

## 🗓️ {day_name}

| Judul | Author | Tahun | Link |
|:------|:-------|:-----:|:----:|
{rows}
---

## 📂 Data

| File | Deskripsi |
|:---|:---|
| 📄 [papers.json](./papers.json) | Raw data paper terbaru |
| 📁 [history/](./history) | Snapshot harian |

---

<sub>⚙️ Dijalankan otomatis oleh [GitHub Actions](../../actions) · Sumber: Semantic Scholar API · Diperbarui: {updated}</sub>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("README.md generated successfully")
