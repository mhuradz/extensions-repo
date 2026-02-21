import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APK_DIR = os.path.join(BASE, "apk")
INDEX = os.path.join(BASE, "index.json")
MIN = os.path.join(BASE, "index.min.json")
HTML = os.path.join(BASE, "index.html")

candidates = [n for n in os.listdir(APK_DIR) if n.lower().endswith(".apk") and ("vortex" in n.lower() or "votex" in n.lower())]
if not candidates:
    raise SystemExit("No vortex APK found in apk/")
apk = candidates[0]

m = re.match(r"tachiyomi-([a-z-]+)\.([^.]+)-v(.+)\.apk", apk)
if not m:
    raise SystemExit(f"Unexpected APK filename format: {apk}")
lang, name, version = m.group(1), m.group(2), m.group(3)
try:
    code = int(version.split(".")[-1])
except Exception:
    code = 1

pkg = f"eu.kanade.tachiyomi.extension.{lang}.{name}"
entry = {
    "name": f"Tachiyomi: {name.capitalize()}",
    "pkg": pkg,
    "apk": apk,
    "lang": "en",
    "code": code,
    "version": version,
    "nsfw": 0,
    "sources": [
        {
            "name": name.capitalize(),
            "lang": "en",
            "id": 1000000000000000001,
            "baseUrl": "",
            "versionId": 1
        }
    ],
}

with open(INDEX, "r", encoding="utf-8") as f:
    items = json.load(f)

items = [e for e in items if e.get("pkg") != "eu.kanade.tachiyomi.extension.en.mangatellers"]
items = [e for e in items if e.get("pkg") != pkg]
items.append(entry)

keep = {
    "eu.kanade.tachiyomi.extension.en.asurascans",
    "eu.kanade.tachiyomi.extension.all.mangafire",
    "eu.kanade.tachiyomi.extension.en.mangareadorg",
    pkg,
}

filtered = []
for e in items:
    if e.get("pkg") in keep:
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
    html.append(f"<a href=\"apk/{ext['apk']}\">{ext['name']}</a>")
html += ["</pre>", "</body>", "</html>"]
with open(HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(html))
print("Swapped Mangatellers ->", name, "and updated index files")

