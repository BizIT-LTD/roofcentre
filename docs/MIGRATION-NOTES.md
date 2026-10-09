# Migration notes

## Source verified

- Document root: `homedir/public_html` in the cPanel backup.
- `wp-config.php` → database `roofcent_wp1`, prefix `wp_`. `siteurl` and `home` are `https://www.roofcentre.com.au`.
- `roofcent_wp2` is Building Repair Centre and `roofcent_wp3` is Pergola Building Centre (separate sites, excluded).
- Content was built with Elementor (`_elementor_data`), plus Elementor Header and Footer templates.

## URL map

Every published Roof Centre page keeps its URL.

| Original URL | New site |
|---|---|
| `/` | kept |
| `/about/`, `/contact/`, `/projects/` | kept |
| `/faq/` | kept (it was empty and now has FAQs) |
| `/roof-repair/`, `/roof-restoration/`, `/colorbond-roofing/` | kept |
| `/roof-replacment/` (original misspelling) | kept as canonical. `/roof-replacement/` 301s to it |
| `/gutter-8-downpipe-replacement/`, `/gutter-protection/` | kept |
| `/emergency-roof-make-safe/`, `/custom-valley-flashings/` | kept |
| `/roof-repair-botany/`, `/roof-repair-chipping-norton/`, `/roof-repair-near-me/` | kept |
| `/home/`, `/blog/`, `/sample-page/`, `/hello-world/`, `/create-your-website-with-blocks/` | 301 → `/` |
| `/privacy-policy/` (was a draft) | 301 → `/privacy/` |
| `/request-a-quote/` | 301 → `/contact/#quote` |
| Yoast sitemaps (`/sitemap_index.xml`, `/page-sitemap.xml` …) | 301 → `/sitemap.xml` |
| `/wp-admin`, `/wp-login.php`, `/xmlrpc.php`, `/wp-content/…`, `/wp-json` | 410 Gone |

New pages: `/services/`, `/privacy/`, `/thank-you/` (noindex) and `/404.html`.

All redirects are in `website/.htaccess` and only apply to the `roofcentre.com.au` host.

## Deployment cautions

- The new site goes on a **new Hostinger website**. Follow `docs/DEPLOY-HOSTINGER.md`.
- The old cPanel `public_html` (Crazy Domains) also holds the Building Repair Centre and Pergola
  Building Centre sites in subfolders. Nothing is deleted there: the old hosting keeps running.
- Live DNS has **no MX record**, so email follows the root A record. Add an explicit MX record and a
  `mail` A record for the Crazy Domains server before pointing the website at Hostinger (Part C,
  step 1 of the deployment guide). The old hosting stays active for email and the other sites.
- Old image URLs under `/wp-content/uploads/` will return 410 on the new site. If Google Images
  traffic matters, map the important ones instead.
- Submit `https://www.roofcentre.com.au/sitemap.xml` in Google Search Console after launch.

## Content decisions to confirm with the business

| Item | Old site | New site |
|---|---|---|
| Emergency availability | "24 Emergency Make Safe" and "available 24/7 and 365 days a year", but footer hours were Mon–Fri 9–5 | 24/7 not claimed. Emergency page says to call. Confirm and add back if true |
| Experience | "over 7 years experience" (written 2021) and elsewhere "since 2006" (template text) | "several years' experience", as used on the service pages. Confirm the real figure |
| Licence | "fully licensed", "full builders licence" — no number anywhere | Licensed and insured claim kept. **Add the NSW contractor licence number**, which NSW rules generally require in advertising |
| ABN / address | None. The suburb pages showed "Suite 270 94 Karimbla Rd, Miranda", which looks like copied template text | No address or ABN shown. Supply them if wanted |
| Suburb pages | Copied template text ("roofing supply company", "[your region or market]", "[phone number]", "shingles") | Rewritten with factual local information and the real project photos |
| Gutter Protection page | Lorem ipsum | Written from general, factual service information |
| Facebook | `facebook.com/amir.mehdi.712` (looks like a personal profile) | Kept in footer. Replace with a business page if there is one |
| Social menu | WordPress placeholder links (wordpress@example.com etc.) | Dropped |
| Photos | Stock avatars, an Athens stock photo, an Unsplash background, and some non-roofing building photos | Excluded. Only Roof Centre roofing photos are used (94) |
