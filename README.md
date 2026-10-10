# Roof Centre website (roofcentre.com.au)

Static HTML/CSS/JS rebuild of the Roof Centre WordPress site.

```
website/     the deployable site: its CONTENTS go into Hostinger's public_html
tools/       content and build scripts
docs/        deployment, enquiry setup, URL map, screenshots
reference/   original cPanel backup: local only, never in Git, never deployed
```

## Preview locally

```
python tools/serve.py
```

Open http://localhost:8080/. Form submissions are mocked and printed in that terminal; nothing is
emailed. Stop with Ctrl+C. Requires Python 3.10+ only.

## Edit and rebuild

| What | Where |
|---|---|
| Services, service areas, FAQs, business details | `tools/content.py` |
| Page layouts, titles, meta descriptions | `tools/build.py` |
| Styles and behaviour | `website/assets/css/site.css`, `website/assets/js/site.js` |
| Photos (list, alt text, categories) | `tools/images.py` |

```
python tools/build.py      # regenerates all HTML, sitemap.xml, robots.txt, site.webmanifest
python tools/check.py      # with serve.py running: links, images, titles, canonicals, sitemap
python tools/package.py    # dist/roofcentre-website.zip for upload
```

`build.py` needs only the files in this repository: it reads `tools/content.py`,
`tools/image-manifest.json` and the optimised images already in `website/assets/img/`.
`images.py` (re-processing photos) needs the original backup extracted to `reference/extracted/`,
which is deliberately not in Git. Image processing needs Pillow (`pip install pillow`).

## Pages

18 indexable pages (all in `sitemap.xml`) plus `/thank-you/` (noindex) and `/404.html`.
See `docs/MIGRATION-NOTES.md` for the URL map and redirects.

## Deployment

See `docs/DEPLOY-HOSTINGER.md`. Hostinger's Git deployment uses the `deploy` branch, which holds
only the contents of `website/` (`git subtree split --prefix=website -b deploy`). Never deploy `main`. Private enquiry settings live on the server outside `public_html`
(`docs/ENQUIRY-SETUP.md`) and are never committed.

## Screenshots

`docs/screenshots/`: desktop (1440px) and mobile (390px) full-page captures of the homepage,
the Roof Repair service page, the project gallery and the contact page.
