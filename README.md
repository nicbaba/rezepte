# rezepte

Öffentliche Zutatenlisten für das Familienbrett, damit die Bring-App sie einlesen kann.

Bring liest Zutaten nur von öffentlichen Seiten, die das Rezept fertig im Seitentext
mitliefern. Für Gerichte ohne eigenen Rezept-Link (z. B. aus einem Kochbuch) liegt hier
deshalb je Gericht eine kleine Seite mit Titel und Zutaten. Anleitungen stehen nur im Brett.

- `rezepte.json` – die Rezepte (Titel, Menge, Zutaten)
- `build.py` – baut daraus die Seiten: `python3 build.py`
- Veröffentlicht über GitHub Pages vom Zweig `gh-pages`:
  `https://nicbaba.github.io/rezepte/<slug>/`

Neues Rezept: Eintrag in `rezepte.json` ergänzen, `python3 build.py` ausführen, committen
und pushen. Im Brett die Seiten-Adresse als Rezept-Link beim Gericht eintragen.
