#!/usr/bin/env python3
"""
gladi.de - erzeugt die statische Website (Englisch + Deutsch) nach public/.

    python3 build.py              # -> public/
    python3 build.py --out DIR    # z. B. für eine Vorschau

Keine Abhängigkeiten, keine externen Ressourcen, keine Cookies. Texte stehen unten in TEXT; Projekte in PROJECTS.
"""
import argparse
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://gladi.de"
KOFI = "https://ko-fi.com/gladi099"
GITHUB = "https://github.com/Gladi"
SOURCE = "https://github.com/Gladi/gladi.de"
YEAR = 2026
INDEX = False          # erst mit Impressum für Suchmaschinen freigeben

# Projekte: Status "live" oder "wip"; Links (Text-Schlüssel, URL)
PROJECTS = [
    {"name": "YATB", "icon": "yatb", "status": "live", "sub": "yatb_sub", "text": "yatb_text",
     "tags": ["Discord", "tag_translation", "AGPL-3.0"],
     "links": [("website", "https://yatb.gladi.de"), ("github", "https://github.com/Gladi/yatb")]},
    {"name": "GFK-Bot", "icon": "gfk-bot", "status": "live", "sub": "gfk_sub", "text": "gfk_text",
     "tags": ["Discord", "Star Trek Fleet Command", "AGPL-3.0"],
     "links": [("github", "https://github.com/Gladi/gfk-bot")]},
    {"name": "401-Bot", "icon": "401-bot", "status": "wip", "sub": "b401_sub", "text": "b401_text",
     "tags": ["Discord", "Star Trek Fleet Command"], "links": []},
]

TEXT = {
    "en": {
        "lang_name": "English", "title": "Gladi - bots and tools for online communities",
        "description": "Gladi builds bots and tools for online communities, mostly for Discord: YATB, GFK-Bot and more.",
        "tagline": "I build bots and tools for online communities - mostly for Discord. Self-hosted, privacy-friendly "
                   "and open source wherever possible.",
        "projects": "Projects", "live": "Live", "wip": "In development", "tag_translation": "translation",
        "website": "Website", "github": "Source code",
        "yatb_sub": "Yet Another Translation Bot",
        "yatb_text": "Links Discord channels in different languages and translates every message under the author's "
                     "name - with AI, Google, Azure or the self-hosted LibreTranslate. Threads, forums and reactions "
                     "included.",
        "gfk_sub": "Alliance bot",
        "gfk_text": "Runs the Discord server of a Star Trek Fleet Command alliance: onboarding with a roster check, "
                    "status roles, incident reports with statistics, event planning with voice channels, and server "
                    "logs.",
        "b401_sub": "Server bot",
        "b401_text": "Coordination across the alliances of a Star Trek Fleet Command server. Currently being planned.",
        "support": "Support",
        "support_text": "My projects are free. Tips go straight into server hosting, translation and API costs - "
                        "thank you!",
        "kofi": "Support on Ko-fi",
        "privacy": "Privacy", "source": "Source of this site", "contact": "Contact: GitHub",
        "theme": {"title": "Theme", "system": "System", "light": "Light", "dark": "Dark"},
        "privacy_title": "Privacy policy",
        "privacy_note": "Translation for convenience - the German version applies.",
        "privacy_body": [
            ("1. Controller", "The operator's contact details will be added here."),
            ("2. This website", "This website uses no cookies, no tracking, no analytics and no external fonts or "
                                "scripts. To deliver the pages, the web server briefly processes your IP address and "
                                "your browser's request; it does not keep access logs. The site runs on an Oracle "
                                "Cloud server in Frankfurt (Germany). HTTPS certificates come from Let's Encrypt; no "
                                "visitor data is passed on for this."),
            ("3. Light/dark setting", "If you choose light or dark with the switch, your browser stores this choice "
                                      "locally (localStorage). It never leaves your device and you can delete it at "
                                      "any time in your browser settings."),
            ("4. Links", "Links to other sites (GitHub, Ko-fi, yatb.gladi.de) are normal links; the privacy policies "
                         "of those sites apply there. The bots have their own privacy information, e.g. "
                         "yatb.gladi.de/en/privacy/."),
            ("5. Your rights", "You have the right to access, rectification, erasure, restriction of processing, data "
                               "portability and objection, and you can lodge a complaint with a data protection "
                               "supervisory authority. Contact the operator (section 1) to exercise your rights."),
        ],
        "back": "Back to the start page", "not_found": "Page not found",
    },
    "de": {
        "lang_name": "Deutsch", "title": "Gladi - Bots und Werkzeuge für Online-Communities",
        "description": "Gladi baut Bots und Werkzeuge für Online-Communities, vor allem für Discord: YATB, GFK-Bot "
                       "und mehr.",
        "tagline": "Ich baue Bots und Werkzeuge für Online-Communities - vor allem für Discord. Selbst gehostet, "
                   "datensparsam und wo immer möglich Open Source.",
        "projects": "Projekte", "live": "Live", "wip": "In Arbeit", "tag_translation": "Übersetzung",
        "website": "Website", "github": "Quellcode",
        "yatb_sub": "Yet Another Translation Bot",
        "yatb_text": "Verbindet Discord-Kanäle in verschiedenen Sprachen und übersetzt jede Nachricht unter dem Namen "
                     "der Person - mit KI, Google, Azure oder dem selbst gehosteten LibreTranslate. Threads, Foren "
                     "und Reaktionen inklusive.",
        "gfk_sub": "Allianz-Bot",
        "gfk_text": "Betreut den Discord-Server einer Star Trek Fleet Command-Allianz: Eingangskontrolle mit "
                    "Mitgliederabgleich, Status-Rollen, Vorfallmeldungen mit Statistik, Eventplanung mit "
                    "Sprachkanälen und Server-Logs.",
        "b401_sub": "Server-Bot",
        "b401_text": "Abstimmung zwischen den Allianzen eines Star Trek Fleet Command-Servers. Gerade in Planung.",
        "support": "Unterstützen",
        "support_text": "Meine Projekte sind kostenlos. Spenden fließen direkt in Server, Übersetzungs- und "
                        "API-Kosten - danke!",
        "kofi": "Auf Ko-fi unterstützen",
        "privacy": "Datenschutz", "source": "Quellcode dieser Seite", "contact": "Kontakt: GitHub",
        "theme": {"title": "Darstellung", "system": "System", "light": "Hell", "dark": "Dunkel"},
        "privacy_title": "Datenschutzerklärung",
        "privacy_note": "",
        "privacy_body": [
            ("1. Verantwortlich", "Die Kontaktdaten des Betreibers werden hier ergänzt."),
            ("2. Diese Website", "Die Website nutzt keine Cookies, kein Tracking, keine Statistik und keine externen "
                                 "Schriften oder Skripte. Um die Seiten auszuliefern, verarbeitet der Webserver kurz "
                                 "die IP-Adresse und die Anfrage deines Browsers; er speichert keine "
                                 "Zugriffsprotokolle. Die Website läuft auf einem Server von Oracle Cloud in Frankfurt "
                                 "(Deutschland). Die HTTPS-Zertifikate stammen von Let's Encrypt; dafür werden keine "
                                 "Besucherdaten weitergegeben."),
            ("3. Hell/Dunkel-Einstellung", "Wählst du mit dem Schalter Hell oder Dunkel, speichert dein Browser diese "
                                           "Wahl lokal (localStorage). Sie verlässt dein Gerät nicht und lässt sich "
                                           "jederzeit in den Browser-Einstellungen löschen."),
            ("4. Links", "Links zu anderen Seiten (GitHub, Ko-fi, yatb.gladi.de) sind normale Links; dort gelten deren "
                         "Datenschutzerklärungen. Die Bots haben eigene Datenschutzhinweise, z. B. "
                         "yatb.gladi.de/de/privacy/."),
            ("5. Deine Rechte", "Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der "
                                "Verarbeitung, Datenübertragbarkeit und Widerspruch, und du kannst dich bei einer "
                                "Datenschutz-Aufsichtsbehörde beschweren. Für deine Rechte wende dich an den Betreiber "
                                "(Abschnitt 1)."),
        ],
        "back": "Zurück zur Startseite", "not_found": "Seite nicht gefunden",
    },
}
LANGS = ["en", "de"]
e = html.escape


def page(lang: str, path: str, title: str, body: str, description: str = "") -> str:
    """Gerüst einer Seite; path = Pfad ohne Sprache, z. B. "" oder "privacy/"."""
    t = TEXT[lang]
    other = [l for l in LANGS if l != lang]
    switch = "".join(f'<span aria-current="true">{l.upper()}</span>' if l == lang else
                     f'<a href="/{l}/{path}" hreflang="{l}" lang="{l}">{l.upper()}</a>' for l in LANGS)
    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{path}">' for l in LANGS)
    robots = "" if INDEX else '<meta name="robots" content="noindex, nofollow">'
    labels = e(json.dumps(t["theme"], ensure_ascii=False), quote=True)
    return f"""<!doctype html>
<html lang="{lang}" data-theme-labels="{labels}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{e(title)}</title>
<meta name="description" content="{e(description or t['description'])}">
{robots}
<link rel="canonical" href="{SITE}/{lang}/{path}">
{alternates}
<link rel="icon" href="/static/img/favicon.ico" sizes="any">
<link rel="icon" href="/static/img/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/static/img/apple-touch-icon.png">
<link rel="stylesheet" href="/static/style.css">
<script src="/static/theme.js"></script>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/{lang}/"><img src="/static/img/avatar-96.webp" alt="" width="34" height="34">Gladi</a>
  <div class="tools">
    <nav class="lang" aria-label="Language">{switch}</nav>
    <button class="theme-toggle" type="button" hidden></button>
  </div>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
  <span>© {YEAR} Gladi</span>
  <a href="/{lang}/privacy/">{e(t['privacy'])}</a>
  <a href="{GITHUB}">{e(t['contact'])}</a>
  <a href="{SOURCE}">{e(t['source'])}</a>
</div></footer>
</body>
</html>
"""


def home(lang: str) -> str:
    t = TEXT[lang]
    cards = []
    for p in PROJECTS:
        links = "".join(f'<a href="{url}">{e(t[key])}</a>' for key, url in p["links"])
        tags = "".join(f"<span>{e(t.get(tag, tag))}</span>" for tag in p["tags"])
        icon = (f'<img class="icon" src="/static/img/project-{p["icon"]}-64.webp" '
                f'srcset="/static/img/project-{p["icon"]}-64.webp 1x, /static/img/project-{p["icon"]}-128.webp 2x" '
                f'alt="" width="56" height="56">')
        cards.append(f"""<article class="card">
  <div class="card-head">{icon}<div><h3>{e(p['name'])}</h3><div class="sub">{e(t[p['sub']])}</div></div>
    <span class="badge {p['status']}">{e(t[p['status']])}</span></div>
  <p>{e(t[p['text']])}</p>
  <div class="tags">{tags}</div>
  {f'<div class="links">{links}</div>' if links else ''}
</article>""")
    body = f"""<section class="hero">
  <img src="/static/img/avatar-256.webp" srcset="/static/img/avatar-256.webp 1x, /static/img/avatar-512.webp 2x"
       alt="Gladi" width="120" height="120">
  <div><h1>Gladi</h1><p>{e(t['tagline'])}</p></div>
</section>
<section id="projects">
  <h2>{e(t['projects'])}</h2>
  <div class="projects">
{chr(10).join(cards)}
  </div>
</section>
<section id="support" class="support">
  <p><strong>{e(t['support'])}.</strong> {e(t['support_text'])}</p>
  <a class="button" href="{KOFI}">{e(t['kofi'])}</a>
</section>"""
    return page(lang, "", t["title"], body)


def privacy(lang: str) -> str:
    t = TEXT[lang]
    sections = "".join(f"<h2>{e(h)}</h2>\n<p>{e(p)}</p>\n" for h, p in t["privacy_body"])
    note = f'<p class="note">{e(t["privacy_note"])}</p>' if t["privacy_note"] else ""
    body = f'<article class="prose"><h1>{e(t["privacy_title"])}</h1>{note}\n{sections}</article>'
    return page(lang, "privacy/", f"{t['privacy_title']} - Gladi", body)


def not_found() -> str:
    t = TEXT["en"]
    body = (f'<article class="prose"><h1>{e(t["not_found"])} · {e(TEXT["de"]["not_found"])}</h1>'
            f'<p><a href="/en/">{e(t["back"])}</a> · <a href="/de/">{e(TEXT["de"]["back"])}</a></p></article>')
    return page("en", "", f"404 - {t['not_found']}", body)


def build(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():          # Inhalt leeren, den Ordner selbst behalten (Bind-Mount von Caddy)
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(ROOT / "static", out / "static")
    for lang in LANGS:
        (out / lang / "privacy").mkdir(parents=True, exist_ok=True)
        (out / lang / "index.html").write_text(home(lang), encoding="utf-8")
        (out / lang / "privacy" / "index.html").write_text(privacy(lang), encoding="utf-8")
    (out / "404.html").write_text(not_found(), encoding="utf-8")
    (out / "robots.txt").write_text("User-agent: *\n" + ("Allow: /\n" if INDEX else "Disallow: /\n"), encoding="utf-8")
    print("gebaut:", out, "| Seiten:", sum(1 for _ in out.rglob("*.html")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "public"))
    build(Path(parser.parse_args().out))
