import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(BASE, "index.json")
MIN = os.path.join(BASE, "index.min.json")
HTML = os.path.join(BASE, "index.html")

KEEP = {
    "eu.kanade.tachiyomi.extension.en.asurascans",
    "eu.kanade.tachiyomi.extension.all.mangafire",
    "eu.kanade.tachiyomi.extension.en.mangareadorg",
    "eu.kanade.tachiyomi.extension.en.mangatellers",
}

with open(INDEX, "r", encoding="utf-8") as f:
    items = json.load(f)

filtered = []
for e in items:
    if e.get("pkg") in KEEP:
        e["lang"] = "en"
        e["sources"] = [s for s in e.get("sources", []) if s.get("lang") == "en"]
        if e["pkg"] == "eu.kanade.tachiyomi.extension.en.asurascans":
            e["name"] = "Tachiyomi: Asura Scans US (unoriginal)"
            for s in e["sources"]:
                s["name"] = "Asura Scans US (unoriginal)"
                s["baseUrl"] = "https://asurascans.us"
        filtered.append(e)

with open(INDEX, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

with open(MIN, "w", encoding="utf-8") as f:
    json.dump(filtered, f, separators=(",", ":"))

html = [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "<meta charset=\"UTF-8\">",
    "<title>apks</title>",
    "</head>",
    "<body>",
    "<pre>",
]
for ext in filtered:
    apk = ext.get("apk")
    name = ext.get("name")
    if apk and name:
        html.append(f"<a href=\"apk/{apk}\">{name}</a>")
html += ["</pre>", "</body>", "</html>"]
with open(HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html))
print(f"Wrote {len(filtered)} extensions to index files and HTML")

