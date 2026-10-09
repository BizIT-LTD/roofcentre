"""Generate the static Roof Centre website into website/.

    python tools/images.py   # once, or after changing photos
    python tools/build.py    # regenerate HTML, sitemap and robots.txt
"""
from pathlib import Path
from html import escape
import json
import datetime
import hashlib
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import SITE, SERVICES, AREAS, GENERAL_FAQS, ABOUT

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website"
IMG = json.loads((ROOT / "tools" / "image-manifest.json").read_text(encoding="utf-8"))
YEAR = datetime.date.today().year
# Cache-busting version from the CSS/JS content, so rebuilds without asset changes leave the HTML identical.
ASSET_V = hashlib.sha1(b"".join((OUT / "assets" / f).read_bytes() for f in ("css/site.css", "js/site.js"))).hexdigest()[:10]
PAGES = []  # (path, priority) for sitemap

E = escape


def esc_attr(s):
    return escape(s, quote=True)


# ---------------------------------------------------------------- images

def img(key, sizes="100vw", cls="", loading="lazy", priority=False, alt=None):
    m = IMG[key]
    files = m["files"]
    srcset = ", ".join(f"/assets/img/{f['file']} {f['w']}w" for f in files)
    default = next((f for f in files if f["w"] >= 800), files[-1])
    a = esc_attr(m["alt"] if alt is None else alt)
    extra = ' fetchpriority="high"' if priority else ""
    lazy = "eager" if priority else loading
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{default["file"]}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{default["w"]}" height="{default["h"]}" alt="{a}" loading="{lazy}" decoding="async"{extra}>')


def largest(key):
    return "/assets/img/" + IMG[key]["files"][-1]["file"]


def gallery(keys, cls="gallery", sizes="(min-width: 1000px) 25vw, (min-width: 600px) 33vw, 50vw", filterable=False):
    items = []
    for k in keys:
        m = IMG[k]
        cat = f' data-category="{m["category"]}"' if filterable else ""
        items.append(
            f'<li{cat}><button type="button" class="gallery__item" data-full="{largest(k)}" data-caption="{esc_attr(m["alt"])}" aria-label="View larger: {esc_attr(m["alt"])}">'
            f'{img(k, sizes=sizes)}</button></li>')
    return f'<ul class="{cls}" role="list">' + "".join(items) + "</ul>"


# ---------------------------------------------------------------- icons

ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "quote": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "alert": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/>',
}


def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


# ---------------------------------------------------------------- layout

def nav_link(href, label, current):
    cur = ' aria-current="page"' if href == current else ""
    return f'<a href="{href}"{cur}>{E(label)}</a>'


def header(current):
    svc_links = "".join(f"<li>{nav_link('/' + s['slug'] + '/', s['name'], current)}</li>" for s in SERVICES)
    area_links = "".join(f"<li>{nav_link('/' + a['slug'] + '/', a['name'], current)}</li>" for a in AREAS)
    svc_active = " is-active" if current in ["/services/"] + [f"/{s['slug']}/" for s in SERVICES] + [f"/{a['slug']}/" for a in AREAS] else ""
    return f'''
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container topbar__inner">
    <span>{icon("clock")} {E(SITE["hours"])}</span>
    <span class="topbar__links"><a href="mailto:{SITE["email"]}">{icon("mail")} {SITE["email"]}</a><a href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a></span>
  </div>
</div>
<header class="site-header" data-header>
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Roof Centre home">
      <img src="/assets/img/logo-white.webp" width="{IMG["_logo-white"]["w"]}" height="{IMG["_logo-white"]["h"]}" alt="Roof Centre">
    </a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list" role="list">
        <li>{nav_link("/", "Home", current)}</li>
        <li>{nav_link("/about/", "About", current)}</li>
        <li class="nav__has-sub{svc_active}">
          <a href="/services/"{' aria-current="page"' if current == "/services/" else ""}>Services</a>
          <button class="nav__sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services"><span class="visually-hidden">Show services</span>{icon("chev")}</button>
          <div class="nav__sub" id="sub-services">
            <div>
              <p class="nav__sub-title">Services</p>
              <ul role="list">{svc_links}</ul>
            </div>
            <div>
              <p class="nav__sub-title">Service areas</p>
              <ul role="list">{area_links}</ul>
            </div>
          </div>
        </li>
        <li>{nav_link("/projects/", "Projects", current)}</li>
        <li>{nav_link("/faq/", "FAQ", current)}</li>
        <li>{nav_link("/contact/", "Contact", current)}</li>
      </ul>
      <div class="nav__mobile-cta">
        <a class="btn btn--accent btn--block" href="/contact/#quote">{icon("quote")} Request a Quote</a>
        <a class="btn btn--ghost-light btn--block" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
        <p>{E(SITE["hours"])}<br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
      </div>
    </nav>
    <div class="header-cta">
      <a class="btn btn--ghost-light header-cta__call" href="{SITE["phone_href"]}">{icon("phone")}<span>{SITE["phone"]}</span></a>
      <a class="btn btn--accent header-cta__quote" href="/contact/#quote">Request a Quote</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle>
        {icon("menu", "icon icon--open")}{icon("close", "icon icon--close")}<span class="visually-hidden">Menu</span>
      </button>
    </div>
  </div>
</header>'''


def footer():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="/{a["slug"]}/">{E(a["name"])}</a></li>' for a in AREAS)
    return f'''
<section class="cta-band" aria-labelledby="cta-band-title">
  <div class="container cta-band__inner">
    <div>
      <h2 id="cta-band-title">Need a roofer? Get a free quote.</h2>
      <p>Tell us about your roof and we will get back to you as soon as possible.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--accent btn--lg" href="/contact/#quote">Request a Quote {icon("arrow")}</a>
      <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <img src="/assets/img/logo-white.webp" width="{IMG["_logo-white"]["w"]}" height="{IMG["_logo-white"]["h"]}" alt="Roof Centre" loading="lazy">
      <p>Roof repairs, restorations and replacements across Sydney. Licensed and insured.</p>
      <a class="social" href="{SITE["facebook"]}" rel="noopener" target="_blank">{icon("facebook")}<span>Facebook</span></a>
    </div>
    <div>
      <h2 class="site-footer__title">Contact</h2>
      <ul class="site-footer__contact" role="list">
        <li>{icon("phone")}<a href="{SITE["phone_href"]}">{SITE["phone"]}</a></li>
        <li>{icon("mail")}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        <li>{icon("clock")}<span>{E(SITE["hours"])}</span></li>
        <li>{icon("pin")}<span>Servicing Sydney</span></li>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__title">Services</h2>
      <ul role="list">{svc}</ul>
    </div>
    <div>
      <h2 class="site-footer__title">Quick links</h2>
      <ul role="list">
        <li><a href="/about/">About us</a></li>
        <li><a href="/projects/">Projects</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact/">Contact us</a></li>
        {areas}
        <li><a href="{SITE["pergola"]}" rel="noopener">Pergola Building Centre</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__base">
    <div class="container">
      <p>&copy; {YEAR} Roof Centre. All rights reserved.</p>
      <p><a href="/privacy/">Privacy</a></p>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick contact">
  <a class="mobile-bar__call" href="{SITE["phone_href"]}">{icon("phone")} Call</a>
  <a class="mobile-bar__quote" href="/contact/#quote">{icon("quote")} Request a Quote</a>
</div>
<dialog class="lightbox" data-lightbox aria-label="Photo viewer">
  <figure>
    <img alt="" data-lightbox-img>
    <figcaption data-lightbox-caption></figcaption>
  </figure>
  <button class="lightbox__btn lightbox__close" type="button" data-lightbox-close aria-label="Close">{icon("close")}</button>
  <button class="lightbox__btn lightbox__prev" type="button" data-lightbox-prev aria-label="Previous photo">{icon("arrow")}</button>
  <button class="lightbox__btn lightbox__next" type="button" data-lightbox-next aria-label="Next photo">{icon("arrow")}</button>
</dialog>'''


ORG_LD = {
    "@context": "https://schema.org",
    "@type": "RoofingContractor",
    "@id": SITE["url"] + "/#business",
    "name": SITE["name"],
    "url": SITE["url"] + "/",
    "logo": SITE["url"] + "/assets/img/logo.png",
    "image": SITE["url"] + "/assets/img/og-roof-centre.jpg",
    "telephone": "+61 431 848 619",
    "email": SITE["email"],
    "areaServed": {"@type": "City", "name": "Sydney"},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00", "closes": "17:00"}],
    "sameAs": [SITE["facebook"]],
}


def page(path, title, description, body, current=None, priority="0.7", noindex=False, ld=None, crumbs=None, og_image=None):
    url = SITE["url"] + path
    lds = []
    if path == "/":
        lds.append(ORG_LD)
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["url"] + "/"}]
        for i, (name, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": i, "name": name, "item": SITE["url"] + href})
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if ld:
        lds.append(ld)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    og = SITE["url"] + (og_image or "/assets/img/og-roof-centre.jpg")
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    html = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{esc_attr(description)}">
{f'<link rel="canonical" href="{url}">' if not noindex else ''}
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Roof Centre">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="{esc_attr(title)}">
<meta property="og:description" content="{esc_attr(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a2552">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{ld_html}
</head>
<body>
{header(current or path)}
<main id="main" tabindex="-1">
{body}
</main>
{footer()}
</body>
</html>
'''
    dest = OUT / path.strip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(l for l in html.splitlines() if l.strip()) + "\n", encoding="utf-8")
    if not noindex:
        PAGES.append((path, priority))


# ---------------------------------------------------------------- components

FULL_BLEED_MIN = 1800  # px width a photo needs before it is used edge to edge
LOW_RES_HEROES = []


def page_hero(title, lead, key, eyebrow=None, crumbs=None, cta=True, size="md"):
    bc = ""
    if crumbs:
        parts = ['<li><a href="/">Home</a></li>'] + [
            f'<li><a href="{h}">{E(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{E(n)}</li>'
            for i, (n, h) in enumerate(crumbs)]
        bc = f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol role="list">{"".join(parts)}</ol></nav>'
    ey = f'<p class="eyebrow">{E(eyebrow)}</p>' if eyebrow else ""
    actions = f'''<div class="hero__actions">
        <a class="btn btn--accent btn--lg" href="/contact/#quote">Request a Quote {icon("arrow")}</a>
        <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
      </div>''' if cta else ""
    # Full-bleed heroes need a large original. Photos only available at phone
    # resolution (~1080px) are shown as a framed photo beside the text instead,
    # so they are never stretched across a wide screen.
    if IMG[key]["files"][-1]["w"] >= FULL_BLEED_MIN:
        return f'''
<section class="page-hero page-hero--{size}">
  <div class="page-hero__media">{img(key, sizes="(max-aspect-ratio: 3/4) 150vw, 100vw", priority=True)}</div>
  <div class="container page-hero__content">
    {bc}{ey}
    <h1>{title}</h1>
    <p class="page-hero__lead">{lead}</p>
    {actions}
  </div>
</section>'''
    LOW_RES_HEROES.append(key)
    return f'''
<section class="page-hero page-hero--split page-hero--{size}">
  <div class="container page-hero__grid">
    <div class="page-hero__content">
      {bc}{ey}
      <h1>{title}</h1>
      <p class="page-hero__lead">{lead}</p>
      {actions}
    </div>
    <div class="page-hero__photo">{img(key, sizes="(min-width: 900px) 520px, min(560px, 92vw)", priority=True)}</div>
  </div>
</section>'''


def faq_list(faqs, heading_level=3):
    out = []
    for q, a in faqs:
        out.append(f'<details class="faq"><summary><h{heading_level} class="faq__q">{E(q)}</h{heading_level}>{icon("chev")}</summary><div class="faq__a"><p>{a}</p></div></details>')
    return '<div class="faq-list">' + "".join(out) + "</div>"


def faq_ld(faqs):
    import re
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


def service_cards(exclude=None, limit=None):
    cards = []
    for s in SERVICES:
        if s["slug"] == exclude:
            continue
        cards.append(f'''<li class="svc-card reveal">
  <a href="/{s["slug"]}/">
    <div class="svc-card__img">{img(s["card"], sizes="(min-width: 1100px) 25vw, (min-width: 640px) 50vw, 100vw")}</div>
    <div class="svc-card__body">
      <h3>{E(s["name"])}</h3>
      <p>{E(s["summary"])}</p>
      <span class="svc-card__more">Learn more {icon("arrow")}</span>
    </div>
  </a>
</li>''')
    if limit:
        cards = cards[:limit]
    return '<ul class="svc-grid" role="list">' + "".join(cards) + "</ul>"


SERVICE_OPTIONS = [s["name"] for s in SERVICES] + ["Roof inspection", "Something else"]


def quote_form(heading="Request a free quote", intro="Fill out the form and we will get back to you as soon as possible.", hid="quote"):
    opts = "".join(f'<option value="{esc_attr(o)}">{E(o)}</option>' for o in SERVICE_OPTIONS)
    return f'''
<div class="quote-card" id="{hid}">
  <h2>{E(heading)}</h2>
  <p class="quote-card__intro">{E(intro)}</p>
  <form class="quote-form" action="/api/enquiry.php" method="post" data-enquiry-form novalidate>
    <div class="field-row">
      <div class="field">
        <label for="{hid}-name">Name <span aria-hidden="true">*</span></label>
        <input id="{hid}-name" name="name" type="text" autocomplete="name" required maxlength="100">
      </div>
      <div class="field">
        <label for="{hid}-phone">Phone <span aria-hidden="true">*</span></label>
        <input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="30">
      </div>
    </div>
    <div class="field-row">
      <div class="field">
        <label for="{hid}-email">Email <span aria-hidden="true">*</span></label>
        <input id="{hid}-email" name="email" type="email" autocomplete="email" required maxlength="150">
      </div>
      <div class="field">
        <label for="{hid}-suburb">Suburb</label>
        <input id="{hid}-suburb" name="suburb" type="text" autocomplete="address-level2" maxlength="80">
      </div>
    </div>
    <div class="field">
      <label for="{hid}-service">Service needed</label>
      <select id="{hid}-service" name="service"><option value="">Please choose</option>{opts}</select>
    </div>
    <div class="field">
      <label for="{hid}-message">How can we help? <span aria-hidden="true">*</span></label>
      <textarea id="{hid}-message" name="message" rows="5" required maxlength="3000" placeholder="For example: the type of roof, where the leak is and how long it has been happening."></textarea>
    </div>
    <div class="field field--hp" aria-hidden="true">
      <label for="{hid}-website">Leave this field empty</label>
      <input id="{hid}-website" name="website" type="text" tabindex="-1" autocomplete="off">
    </div>
    <input type="hidden" name="page" value="">
    <input type="hidden" name="started" value="">
    <p class="form-note">Fields marked * are required. We only use your details to respond to your enquiry. See our <a href="/privacy/">privacy statement</a>.</p>
    <button class="btn btn--primary btn--lg btn--block" type="submit">Send enquiry {icon("arrow")}</button>
    <div class="form-status" role="status" aria-live="polite" tabindex="-1" data-form-status></div>
  </form>
</div>'''


def contact_aside():
    return f'''
<aside class="contact-aside">
  <h2>Contact details</h2>
  <ul class="contact-list" role="list">
    <li>{icon("phone")}<div><span>Phone</span><a href="{SITE["phone_href"]}">{SITE["phone"]}</a></div></li>
    <li>{icon("mail")}<div><span>Email</span><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></li>
    <li>{icon("clock")}<div><span>Business hours</span>{E(SITE["hours"])}</div></li>
    <li>{icon("pin")}<div><span>Service area</span>Sydney, including Botany and Chipping Norton</div></li>
  </ul>
  <div class="contact-aside__note">
    {icon("alert")}
    <p><strong>Storm damage or an urgent leak?</strong> Call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>. If life or property is at immediate risk during a storm, call the NSW SES on <a href="tel:132500">132 500</a>.</p>
  </div>
</aside>'''


# ---------------------------------------------------------------- pages

def build_home():
    trust = [("shield", "Licensed &amp; insured"), ("quote", "Free quotes"), ("home", "Residential, commercial &amp; industrial"), ("check", "Tile and metal roofs")]
    trust_html = "".join(f'<li>{icon(i)}<span>{t}</span></li>' for i, t in trust)
    feature_svcs = SERVICES[:4]
    body = f'''
<section class="hero">
  <div class="hero__media">{img("colorbond-reroof-progress", sizes="(max-aspect-ratio: 3/4) 180vw, 100vw", priority=True, cls="hero__img")}</div>
  <div class="container hero__content">
    <p class="eyebrow eyebrow--light">Sydney roofing contractor</p>
    <h1>Roof repairs, replacements and Colorbond roofing you can count on</h1>
    <p class="hero__lead">Roof Centre repairs, restores and replaces tile and metal roofs for homes and businesses across Sydney. Our speciality is converting existing roofs to new Colorbond and Zincalume steel.</p>
    <div class="hero__actions">
      <a class="btn btn--accent btn--lg" href="#quote">Request a Quote {icon("arrow")}</a>
      <a class="btn btn--ghost-light btn--lg" href="{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a>
    </div>
    <ul class="hero__trust" role="list">{trust_html}</ul>
  </div>
</section>

<section class="section intro">
  <div class="container split">
    <div class="split__text reveal">
      <p class="eyebrow">About Roof Centre</p>
      <h2>A local roofer focused on roofs that last</h2>
      <p>{ABOUT["intro"][0]}</p>
      <p>{ABOUT["intro"][2]}</p>
      <ul class="ticks" role="list">
        <li>{icon("check")} Fully licensed and insured</li>
        <li>{icon("check")} Builder and client references available on request</li>
        <li>{icon("check")} Free quotes</li>
      </ul>
      <a class="btn btn--primary" href="/about/">More about us {icon("arrow")}</a>
    </div>
    <div class="split__media reveal">
      <div class="stack">
        {img("cottage-reroof-complete", sizes="(min-width: 900px) 40vw, 90vw", cls="stack__a")}
        {img("cn-3", sizes="(min-width: 900px) 22vw, 50vw", cls="stack__b")}
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">What we do</p>
      <h2>Our roofing services</h2>
      <p>From a single cracked tile to a complete re-roof, we handle the full range of roofing work.</p>
    </div>
    {service_cards()}
  </div>
</section>

<section class="section feature-rows">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Recent projects</p>
      <h2>Real roofs, real results</h2>
      <p>Photos from our own jobs across Sydney.</p>
    </div>
    <article class="project reveal">
      <div class="project__text">
        <h3>Botany roof repair</h3>
        <p>We provide professional repairs for all types of roofs, from broken tiles to rusted sheets. Whether your leak was caused by weather, rust, debris or overflowing water, our roofers will fix the problem.</p>
        <a class="link-arrow" href="/roof-repair-botany/">Roof repair in Botany {icon("arrow")}</a>
      </div>
      {gallery(["botany-2", "botany-3", "botany-1", "botany-4"], cls="gallery gallery--feature", sizes="(min-width: 900px) 30vw, 50vw")}
    </article>
    <article class="project project--flip reveal">
      <div class="project__text">
        <h3>Chipping Norton roof replacement</h3>
        <p>Replacing tile with tile or tile with metal, we deliver quality work at a competitive price. This home was re-roofed with new metal roofing, ridge capping and valleys.</p>
        <a class="link-arrow" href="/roof-repair-chipping-norton/">Roofing in Chipping Norton {icon("arrow")}</a>
      </div>
      {gallery(["cn-2", "cn-3", "cn-5", "cn-1"], cls="gallery gallery--feature", sizes="(min-width: 900px) 30vw, 50vw")}
    </article>
    <div class="center reveal"><a class="btn btn--primary btn--lg" href="/projects/">View all projects {icon("arrow")}</a></div>
  </div>
</section>

<section class="section section--dark steps">
  <div class="container">
    <div class="section-head section-head--light reveal">
      <p class="eyebrow eyebrow--light">How it works</p>
      <h2>Getting your roof fixed</h2>
    </div>
    <ol class="steps__list" role="list">
      <li class="reveal"><span class="steps__num">1</span><h3>Tell us about the job</h3><p>Call us or send an enquiry with your suburb, roof type and the problem. Photos help.</p></li>
      <li class="reveal"><span class="steps__num">2</span><h3>Inspection and free quote</h3><p>We inspect the roof, explain what we found and give you a quote for the work.</p></li>
      <li class="reveal"><span class="steps__num">3</span><h3>The work is done</h3><p>Once you accept the quote, we book the job and complete the work.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container split split--top">
    <div class="reveal">
      <p class="eyebrow">Common questions</p>
      <h2>Frequently asked questions</h2>
      {faq_list(GENERAL_FAQS[:5])}
      <p class="more-link"><a class="link-arrow" href="/faq/">See all FAQs {icon("arrow")}</a></p>
    </div>
    <div class="reveal">
      {quote_form()}
    </div>
  </div>
</section>
'''
    page("/", "Roof Centre | Roof Repairs, Re-roofing & Colorbond Sydney",
         "Sydney roofer for roof repairs, restoration, replacement, Colorbond roofing, gutters and flashings. Licensed and insured. Call 0431 848 619 for a free quote.",
         body, priority="1.0", ld=faq_ld(GENERAL_FAQS[:5]))


def build_about():
    body = page_hero("About Roof Centre", "A local roofing contractor for homes and businesses that need to replace, repair or renovate their roof.", "cottage-rear", crumbs=[("About", "/about/")]) + f'''
<section class="section">
  <div class="container split">
    <div class="split__text prose reveal">
      <h2>Who we are</h2>
      {"".join(f"<p>{p}</p>" for p in ABOUT["intro"])}
      <p>Please contact our friendly team for a free quote or more information.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="/contact/#quote">Request a Quote {icon("arrow")}</a>
        <a class="btn btn--outline" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
      </div>
    </div>
    <div class="split__media reveal">
      <div class="stack">
        {img("crew-commercial", sizes="(min-width: 900px) 40vw, 90vw", cls="stack__a")}
        {img("cottage-valley", sizes="(min-width: 900px) 22vw, 50vw", cls="stack__b")}
      </div>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <h2>What we focus on</h2>
    </div>
    <ul class="value-grid" role="list">
      <li class="reveal">{icon("home")}<h3>Domestic re-roofing</h3><p>Converting existing homes of any roof type to Colorbond or Zincalume steel is our speciality.</p></li>
      <li class="reveal">{icon("shield")}<h3>Long-lasting work</h3><p>Our goal is to make every new roof or repair last as long as possible, using high-grade materials on a sensible budget.</p></li>
      <li class="reveal">{icon("check")}<h3>All roof types</h3><p>We also repair and restore industrial, commercial and residential roofs, both tile and metal.</p></li>
    </ul>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head reveal"><h2>Our services</h2></div>
    {service_cards()}
  </div>
</section>'''
    page("/about/", "About Roof Centre | Sydney Roofing Contractor",
         "Roof Centre is a licensed and insured Sydney roofer specialising in converting existing roofs to Colorbond and Zincalume, plus roof repairs and restoration.",
         body, crumbs=[("About", "/about/")])


def build_services_hub():
    area_links = "".join(f'<li><a class="link-arrow" href="/{a["slug"]}/">{E(a["name"])} {icon("arrow")}</a></li>' for a in AREAS)
    body = page_hero("Roofing services", "Repairs, restorations, replacements, Colorbond roofing, gutters and flashings for homes and businesses across Sydney.", "cottage-battens", crumbs=[("Services", "/services/")]) + f'''
<section class="section">
  <div class="container">
    {service_cards()}
  </div>
</section>
<section class="section section--tint">
  <div class="container narrow reveal">
    <h2>Service areas</h2>
    <p>We work across Sydney. Read more about our work in these areas:</p>
    <ul class="link-list" role="list">{area_links}</ul>
  </div>
</section>'''
    page("/services/", "Roofing Services in Sydney | Roof Centre",
         "Roof repair, restoration and replacement, Colorbond roofing, gutters and downpipes, gutter protection, emergency make-safe and valley flashings in Sydney.",
         body, priority="0.8", crumbs=[("Services", "/services/")])


def render_blocks(blocks):
    out = []
    for b in blocks:
        if isinstance(b, list):
            out.append('<ul class="ticks" role="list">' + "".join(f"<li>{icon('check')} {x}</li>" for x in b) + "</ul>")
        else:
            out.append(f"<p>{b}</p>")
    return "".join(out)


def build_service(s):
    path = f"/{s['slug']}/"
    crumbs = [("Services", "/services/"), (s["name"], path)]
    sections = "".join(
        f'<section class="prose-block reveal"><h2>{E(h)}</h2>{render_blocks(blocks)}</section>' for h, blocks in s["sections"])
    signs = "".join(f"<li>{icon('check')} {E(x)}</li>" for x in s["signs"])
    side_img = s["gallery"][1] if s["gallery"][0] == s["hero"] else s["gallery"][0]
    faqs = s["faqs"] + [GENERAL_FAQS[0], GENERAL_FAQS[1]]
    body = page_hero(E(s["name"]), s["lead"], s["hero"], eyebrow="Roof Centre services", crumbs=crumbs) + f'''
<section class="section">
  <div class="container svc-layout">
    <div class="prose">
      {sections}
    </div>
    <aside class="svc-aside">
      <div class="svc-aside__card reveal">
        {img(side_img, sizes="(min-width: 1000px) 360px, 90vw")}
        <div class="svc-aside__body">
          <h2>{"Good times to call us" if s["slug"] == "colorbond-roofing" else "Signs you may need this"}</h2>
          <ul class="ticks ticks--sm" role="list">{signs}</ul>
          <a class="btn btn--accent btn--block" href="/contact/?service={s["slug"]}#quote">Request a Quote</a>
          <a class="btn btn--outline btn--block" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
        </div>
      </div>
    </aside>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our work</p>
      <h2>{E(s["name"])} photos</h2>
      <p>Photos from Roof Centre jobs. Select a photo to enlarge it.</p>
    </div>
    {gallery(s["gallery"])}
  </div>
</section>
<section class="section">
  <div class="container narrow reveal">
    <h2>Questions about {E(s["name"].lower())}</h2>
    {faq_list(faqs)}
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal"><h2>Other services</h2></div>
    {service_cards(exclude=s["slug"], limit=4)}
  </div>
</section>'''
    page(path, s["seo_title"], s["description"], body, priority="0.8", crumbs=crumbs, ld=faq_ld(faqs),
         og_image="/assets/img/" + IMG[s["hero"]]["files"][min(1, len(IMG[s["hero"]]["files"]) - 1)]["file"])


def build_area(a):
    path = f"/{a['slug']}/"
    crumbs = [("Services", "/services/"), (a["name"], path)]
    where = f"in {a['suburb']}" if a["suburb"] else "near you"
    local = "".join(f'<section class="prose-block reveal"><h2>{E(h)}</h2><p>{p}</p></section>' for h, p in a["local"])
    svc_list = "".join(f'<li><a href="/{s["slug"]}/">{E(s["name"])}</a></li>' for s in SERVICES)
    title = f"Roof repair in {E(a['suburb'])}" if a["suburb"] else "Roof repairs near you"
    body = page_hero(title, a["lead"], a["hero"], eyebrow="Service area", crumbs=crumbs) + f'''
<section class="section">
  <div class="container svc-layout">
    <div class="prose">
      <section class="prose-block reveal">
        <h2>Your local roofer {E(where)}</h2>
        <p>Roof Centre provides professional repairs for all types of roofs, from broken tiles to rusted sheets. Whether your leak was caused by weather, rust, debris or overflowing water, our roofers will find the problem and fix it.</p>
        <p>{a["about"]}</p>
      </section>
      {local}
      <section class="prose-block reveal">
        <h2>Common roof problems we fix</h2>
        <ul class="ticks" role="list">
          <li>{icon("check")} <span><strong>Leaking roofs:</strong> often caused by cracked tiles, failed flashings or rusted valleys.</span></li>
          <li>{icon("check")} <span><strong>Broken or slipped tiles:</strong> high winds and storms can crack or move tiles and ridge capping.</span></li>
          <li>{icon("check")} <span><strong>Rusted metal roofs:</strong> rusted sheets, screws and flashings let water in over time.</span></li>
          <li>{icon("check")} <span><strong>Moss and lichen:</strong> holds moisture against the roof and wears down tiles over time.</span></li>
          <li>{icon("check")} <span><strong>Blocked or damaged gutters:</strong> can push water back under the roof and into the eaves.</span></li>
        </ul>
      </section>
      <section class="prose-block reveal">
        <h2>Our services {E(where)}</h2>
        <ul class="link-columns" role="list">{svc_list}</ul>
      </section>
    </div>
    <aside class="svc-aside">
      <div class="svc-aside__card reveal">
        <div class="svc-aside__body">
          <h2>Get a free quote</h2>
          <p>Call us or send an enquiry with your suburb, roof type and what you have noticed.</p>
          <a class="btn btn--accent btn--block" href="/contact/?service=roof-repair#quote">Request a Quote</a>
          <a class="btn btn--outline btn--block" href="{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a>
          <p class="svc-aside__hours">{icon("clock")} {E(SITE["hours"])}</p>
        </div>
      </div>
    </aside>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Project photos</p>
      <h2>{E(a["project_title"])}</h2>
    </div>
    {gallery(a["project"])}
  </div>
</section>
<section class="section">
  <div class="container narrow reveal">
    <h2>Frequently asked questions</h2>
    {faq_list([GENERAL_FAQS[0], GENERAL_FAQS[1], GENERAL_FAQS[5], GENERAL_FAQS[7]])}
  </div>
</section>'''
    page(path, a["seo_title"], a["description"], body, priority="0.6", crumbs=crumbs)


GALLERY_FILTERS = [("all", "All"), ("replacement", "Roof replacement"), ("repair", "Roof repair"), ("colorbond", "Colorbond"), ("restoration", "Restoration"), ("gutters", "Gutters"), ("flashing", "Flashings"), ("emergency", "Make safe")]


def build_projects():
    order = [k for k in IMG if not k.startswith("_")]
    skip = {"tarp-make-safe", "metal-roof-escarpment"}
    keys = [k for k in order if k not in skip]
    btns = "".join(
        f'<button type="button" class="chip" data-filter="{v}" aria-pressed="{"true" if v == "all" else "false"}">{E(l)}</button>' for v, l in GALLERY_FILTERS)
    body = page_hero("Our projects", "We have completed projects from small repairs to full re-roofs, covering almost every part of the roof. Here are some of them.", "cottage-reroof-complete", crumbs=[("Projects", "/projects/")]) + f'''
<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <h2>Featured projects</h2>
    </div>
    <div class="featured-projects">
      <article class="fp reveal">
        <a href="/roof-repair-botany/">{img("botany-2", sizes="(min-width: 900px) 45vw, 100vw")}</a>
        <div><h3>Botany roof repair</h3><p>Repairs to a metal roof in Botany.</p><a class="link-arrow" href="/roof-repair-botany/">See the project {icon("arrow")}</a></div>
      </article>
      <article class="fp reveal">
        <a href="/roof-repair-chipping-norton/">{img("cn-2", sizes="(min-width: 900px) 45vw, 100vw")}</a>
        <div><h3>Chipping Norton roof replacement</h3><p>A full re-roof with new metal roofing, ridges and valleys.</p><a class="link-arrow" href="/roof-repair-chipping-norton/">See the project {icon("arrow")}</a></div>
      </article>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <div class="section-head reveal">
      <h2>Project gallery</h2>
      <p>Filter by type of work, and select a photo to enlarge it.</p>
    </div>
    <div class="chips" role="group" aria-label="Filter photos">{btns}</div>
    <p class="visually-hidden" role="status" data-filter-status></p>
    {gallery(keys, cls="gallery gallery--masonry", filterable=True)}
  </div>
</section>'''
    page("/projects/", "Roofing Projects | Photo Gallery | Roof Centre Sydney",
         "Photos of Roof Centre's roofing work across Sydney: roof replacements, roof repairs, Colorbond roofing, restorations, gutters, flashings and make-safes.",
         body, priority="0.8", crumbs=[("Projects", "/projects/")])


def build_faq():
    groups = [("General", GENERAL_FAQS)] + [(s["name"], s["faqs"]) for s in SERVICES]
    sections = "".join(f'<section class="faq-group reveal"><h2>{E(n)}</h2>{faq_list(f)}</section>' for n, f in groups)
    allf = [f for _, fs in groups for f in fs]
    body = page_hero("Frequently asked questions", "Answers to common questions about our roofing services. Can't find what you need? Call us or send an enquiry.", "cottage-valley-2", crumbs=[("FAQ", "/faq/")]) + f'''
<section class="section">
  <div class="container narrow">
    {sections}
  </div>
</section>'''
    page("/faq/", "Roofing FAQs | Roof Centre Sydney",
         "Answers to common roofing questions: free quotes, service areas, roof repair versus replacement, Colorbond, gutters, storm damage and more.",
         body, priority="0.6", ld=faq_ld(allf), crumbs=[("FAQ", "/faq/")])


def build_contact():
    body = page_hero("Contact us", "Fill out the form and we will get back to you as soon as possible, or call us during business hours.", "cottage-sheets", crumbs=[("Contact", "/contact/")], cta=False, size="sm") + f'''
<section class="section">
  <div class="container contact-layout">
    {quote_form(heading="Request a quote", intro="Tell us about your roof. Include your suburb and, if you can, a description of the problem.")}
    {contact_aside()}
  </div>
</section>'''
    page("/contact/", "Contact Roof Centre | Request a Roofing Quote",
         "Contact Roof Centre for a free roofing quote. Call 0431 848 619 or email info@roofcentre.com.au. Business hours: Monday to Friday, 9 am to 5 pm.",
         body, priority="0.8", crumbs=[("Contact", "/contact/")])


def build_thanks():
    body = f'''
<section class="section message-page">
  <div class="container narrow center">
    {icon("check", "icon icon--xl")}
    <h1>Thanks, your enquiry has been sent</h1>
    <p>We will get back to you as soon as possible. If your job is urgent, please call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="/">Back to home</a>
      <a class="btn btn--outline" href="/projects/">View our projects</a>
    </div>
  </div>
</section>'''
    page("/thank-you/", "Thank You | Roof Centre", "Your enquiry has been sent to Roof Centre.", body, noindex=True)


def build_privacy():
    body = page_hero("Privacy statement", "How Roof Centre handles the personal information you send us.", "colorbond-ridge-solar", crumbs=[("Privacy", "/privacy/")], cta=False, size="sm") + f'''
<section class="section">
  <div class="container narrow prose">
    <h2>Information we collect</h2>
    <p>When you send an enquiry through this website, we collect the details you enter: your name, phone number, email address, suburb, the service you are interested in and your message.</p>
    <h2>How we use it</h2>
    <p>We use these details only to respond to your enquiry, prepare a quote and contact you about your job. We do not sell your information.</p>
    <h2>How it is sent and stored</h2>
    <p>Enquiries are sent to our business email. They are kept for as long as needed to respond to you and to keep business records.</p>
    <h2>Access and corrections</h2>
    <p>To ask about, correct or delete the information we hold about you, email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> or call <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
  </div>
</section>'''
    page("/privacy/", "Privacy Statement | Roof Centre", "How Roof Centre collects and uses the personal information you send through our website.", body, priority="0.2", crumbs=[("Privacy", "/privacy/")])


def build_404():
    body = f'''
<section class="section message-page">
  <div class="container narrow center">
    <p class="eyebrow">Error 404</p>
    <h1>Sorry, we couldn't find that page</h1>
    <p>The page may have moved. Try one of these instead, or call us on <a href="{SITE["phone_href"]}">{SITE["phone"]}</a>.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--primary" href="/">Home</a>
      <a class="btn btn--outline" href="/services/">Services</a>
      <a class="btn btn--outline" href="/contact/">Contact</a>
    </div>
  </div>
</section>'''
    page("/404.html", "Page Not Found | Roof Centre", "The page you are looking for could not be found.", body, noindex=True, current="")


def build_meta_files():
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE['url']}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nDisallow: /api/\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": "Roof Centre", "short_name": "Roof Centre", "start_url": "/", "display": "browser",
        "background_color": "#ffffff", "theme_color": "#0a2552",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2), encoding="utf-8")


def main():
    build_home()
    build_about()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
    for a in AREAS:
        build_area(a)
    build_projects()
    build_faq()
    build_contact()
    build_privacy()
    build_thanks()
    build_404()
    build_meta_files()
    print(f"Built {len(PAGES)} indexable pages + thank-you + 404")
    if LOW_RES_HEROES:
        print("Framed (not full-bleed) heroes, originals under", FULL_BLEED_MIN, "px:", ", ".join(LOW_RES_HEROES))


if __name__ == "__main__":
    main()
