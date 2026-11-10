#!/usr/bin/env python3
"""Baut aus rezepte.json eine statische Seite je Rezept.

Zweck: Die Bring-App liest Zutaten nur von öffentlichen Seiten, die das Rezept
fertig im Seitentext mitliefern (schema.org/Recipe). Jede Seite enthält deshalb
JSON-LD und Microdata. Aufruf: python3 build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
BASE = "https://nicbaba.github.io/rezepte"

CSS = """
:root{--bg:#EDF0EB;--card:#fff;--ink:#17211B;--ink2:#56635B;--accent:#2C6A4C}
@media (prefers-color-scheme:dark){:root{--bg:#0E1411;--card:#171F1A;--ink:#EDF2ED;--ink2:#A3B1A7;--accent:#6CC597}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.45 -apple-system,BlinkMacSystemFont,system-ui,"Segoe UI",Roboto,sans-serif;padding:24px 16px 40px}
main{max-width:620px;margin:0 auto;display:grid;gap:16px}
h1{font-size:30px;line-height:1.15;margin:0}
h2{font-size:19px;margin:0 0 8px}
p{margin:4px 0 0;color:var(--ink2);font-size:15px}
section{background:var(--card);border-radius:18px;padding:16px 18px}
ul{margin:0;padding-left:22px;display:grid;gap:6px}
a{color:var(--accent)}
a.btn{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:999px;background:var(--accent);color:var(--card);font-weight:600;text-decoration:none}
"""


def page(title, body, head=""):
    return (
        "<!doctype html>\n<html lang=\"de\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n{head}<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )


def recipe_page(r):
    url = f"{BASE}/{r['slug']}/"
    image = f"{BASE}/bild.png"
    ld = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": r["name"],
        "url": url,
        "image": [image],
        "author": {"@type": "Person", "name": "Familie"},
        "recipeYield": r.get("yield", "4 Portionen"),
        "recipeIngredient": r["ingredients"],
    }
    if r.get("minutes"):
        ld["totalTime"] = f"PT{int(r['minutes'])}M"
    head = (
        f"<link rel=\"canonical\" href=\"{url}\">\n"
        f"<meta property=\"og:title\" content=\"{html.escape(r['name'])}\">\n"
        f"<meta property=\"og:image\" content=\"{image}\">\n"
        "<script type=\"application/ld+json\">\n"
        + json.dumps(ld, ensure_ascii=False, indent=1)
        + "\n</script>\n"
    )
    items = "\n".join(
        f"      <li itemprop=\"recipeIngredient\">{html.escape(i)}</li>" for i in r["ingredients"]
    )
    bring = (
        "https://api.getbring.com/rest/bringrecipes/deeplink?url="
        + url.replace(":", "%3A").replace("/", "%2F")
        + "&source=web&baseQuantity=4&requestedQuantity=4"
    )
    meta = " · ".join(x for x in [r.get("yield", ""), f"{r['minutes']} Min." if r.get("minutes") else ""] if x)
    body = f"""<main itemscope itemtype="https://schema.org/Recipe">
  <header>
    <h1 itemprop="name">{html.escape(r['name'])}</h1>
    <p><span itemprop="recipeYield">{html.escape(meta)}</span></p>
    <meta itemprop="image" content="{image}">
  </header>
  <section>
    <h2>Zutaten</h2>
    <ul>
{items}
    </ul>
  </section>
  <a class="btn" href="{html.escape(bring)}">Zutaten nach Bring</a>
</main>"""
    return page(r["name"], body, head)


def main():
    recipes = json.loads((ROOT / "rezepte.json").read_text(encoding="utf-8"))
    for r in recipes:
        d = ROOT / r["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(recipe_page(r), encoding="utf-8")
    links = "\n".join(
        f"      <li><a href=\"{html.escape(r['slug'])}/\">{html.escape(r['name'])}</a></li>" for r in recipes
    )
    body = f"<main>\n  <h1>Rezepte</h1>\n  <section>\n    <ul>\n{links}\n    </ul>\n  </section>\n</main>"
    (ROOT / "index.html").write_text(page("Rezepte", body), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"{len(recipes)} Rezept(e) gebaut")


if __name__ == "__main__":
    main()
