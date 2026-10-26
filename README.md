# gladi.de

Personal website of Gladi: projects (YATB, GFK-Bot, 401-Bot) and support link. Static HTML in English and German,
light/dark theme following the system with a manual switch. No cookies, no tracking, no external fonts or scripts.

## Build

```
python3 build.py              # writes public/ (committed, served directly by Caddy)
python3 build.py --out /tmp/x # e.g. for a preview
```

Texts and projects live in `build.py` (`TEXT`, `PROJECTS`), styles in `static/style.css`, the theme switch in
`static/theme.js`. `INDEX = False` keeps search engines out (noindex) until an imprint is added.

## Serving

`Caddyfile.snippet` defines `gladi_site` (security headers, language redirect from `/` by `Accept-Language`,
404 page). Local preview on port 8089:

```
docker run --rm -p 127.0.0.1:8089:8089 -v $PWD:/site:ro -v $PWD/public:/srv/gladi:ro -w /site caddy:2 \
  caddy run --config /site/Caddyfile.preview --adapter caddyfile
```

## License

Code: [GNU Affero General Public License v3.0](LICENSE). The Gladi logo and the texts are © Gladi and not covered by
the license.
