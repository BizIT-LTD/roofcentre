# Deploying to a new Hostinger website

This puts the new site on a **new** Hostinger website (not an existing Hostinger site, and not the
old Crazy Domains cPanel account) and tests it on Hostinger's temporary domain first.

- Only the **contents of `website/`** go into the new site's `public_html`. `tools/`, `docs/`,
  `README.md`, `reference/`, backups, database dumps and private settings are never uploaded there.
- Private enquiry settings live **outside `public_html`** (Part A, step 5).
- The existing Crazy Domains hosting **stays active**. It handles email for roofcentre.com.au and
  hosts the Building Repair Centre website. Nothing on it is deleted or changed.
- DNS changes happen only in Part C, later, and only when approved.

hPanel menu names change from time to time. If a label below differs, look for the nearest equivalent.

---

## Current setup (checked 10 Oct 2026)

Live values from Crazy Domains' authoritative name servers, plus a test against the old mail server:

| Item | Live value |
|---|---|
| Nameservers | `ns1.crazydomains.com`, `ns2.crazydomains.com` (DNS is managed in Crazy Domains) |
| `roofcentre.com.au` A | `103.20.200.233` (Crazy Domains cPanel server), TTL 300 |
| `www.roofcentre.com.au` A | `103.20.200.233`, TTL 300 |
| AAAA | none |
| MX | **none** |
| `mail.roofcentre.com.au` | **does not exist** |
| SPF, DKIM, DMARC | **none published** |
| Mail server at `103.20.200.233` | Exim, greets as `cp-wc27.syd02.ds.network`, and accepts mail for `info@roofcentre.com.au` (SMTP `RCPT` test, no message sent) |
| Email | `info@roofcentre.com.au` is a cPanel **forwarder** to `info@buildingrepaircentre.com.au` (that domain's mail is on Google Workspace) |

**Why this matters.** With no MX record, senders deliver roofcentre.com.au mail to the root A record.
Today that is the Crazy Domains server, which runs the forwarder. If the root A record were pointed at
Hostinger without an MX record, incoming mail would go to Hostinger and the forwarder would stop
working. Part C, step 1 fixes this before the website moves.

**Not live values.** The cPanel backup's own zone file (`dnszones/roofcentre.com.au.db`) lists
`MX 0 roofcentre.com.au`, `mail` as a CNAME, an SPF record and a DKIM key. Crazy Domains' name
servers do **not** publish these records, so they are not in effect. Do not copy them into DNS.

---

## Part A: create the Hostinger website and upload (no DNS change)

1. **Build and package on this PC**
   ```
   python tools/build.py
   python tools/serve.py        # in a second terminal, for the check
   python tools/check.py        # expect "No problems found."
   python tools/package.py      # creates dist/roofcentre-website.zip
   ```
   The zip contains the contents of `website/` (including `.htaccess`) with no wrapping folder.
   `package.py` refuses to run if `website/` contains config files, SQL dumps, archives or logs.

2. **Create a new website in hPanel**
   - Websites → **Add website** → choose an empty/custom PHP & HTML website (not WordPress and not
     the website builder). Do not reuse or overwrite an existing Hostinger website.
   - If asked for a domain, enter `roofcentre.com.au` as an **existing domain you own**. **Skip** any
     offer to change nameservers or to connect or point the domain now.
   - Note the **temporary domain** Hostinger gives the site (for example
     `something.hostingersite.com`). Part B uses it for all testing.
   - If hPanel insists on connecting the domain first, create the site on the temporary domain only
     and add `roofcentre.com.au` in Part C.
   - Do **not** create Hostinger email accounts for roofcentre.com.au. Ignore hPanel prompts to add MX
     records. Email stays on Crazy Domains.

3. **Set PHP**
   Websites → Manage → Advanced → PHP Configuration → PHP **8.2 or newer**. The `mbstring` extension
   must be enabled (it normally is).

4. **Upload into `public_html`**
   - Websites → Manage → **File Manager** → open this website's `public_html`.
   - Delete Hostinger's placeholder files (usually `default.php` and/or `index.php`) so the folder is
     empty.
   - Upload `dist/roofcentre-website.zip` into `public_html`. Right-click → **Extract** into
     `public_html` itself (not a subfolder), then delete the zip.
   - Turn on "show hidden files". Check that `public_html` directly contains `index.html`,
     `.htaccess`, `404.html`, `sitemap.xml`, `robots.txt`, `assets/`, `api/`, `about/` and the other
     page folders, and nothing else.

   *Alternative:* upload over SFTP (hPanel → Files → FTP Accounts gives the host, user and port).
   Copy the **contents** of `website/` into `public_html/`.

5. **Private enquiry settings (outside `public_html`)**
   - In File Manager, go **up one level** from `public_html`, to the folder that contains it (for
     example `/home/u123456789/domains/roofcentre.com.au/`).
   - Create `roofcentre-enquiry-config.php` there, starting from
     `docs/roofcentre-enquiry-config.example.php`. Set the confirmed recipient address(es).
   - `website/api/enquiry.php` reads it from two levels above `public_html/api/`, which is that folder.
   - Never put this file in `public_html` or in Git (it is listed in `.gitignore`).

### Git deployment (alternative to steps 1 and 4)

`main` is the full source project. Hostinger must deploy the **`deploy`** branch, which contains
only the contents of `website/` at its root (`index.html`, `.htaccess`, `assets/`, `api/` …).
Deploying `main` puts the site in `public_html/website/` and exposes `tools/`, `docs/` and
`README.md`, while the domain root shows 403/404.

Update `deploy` after committing changes to `main` (no force-push needed; the split is
deterministic and fast-forwards):
```
git subtree split --prefix=website -b deploy
git push origin main deploy
```

hPanel setup (Websites → Manage → Advanced → **Git**):

- Repository: `https://github.com/BizIT-LTD/roofcentre.git`, branch **`deploy`**.
- Install path / directory: **leave empty**, which means `public_html` itself. Do not enter `website`.
- Hostinger only installs into an **empty** directory. Remove any earlier deployment first (see
  "Fixing a deployment of `main`" below). Then **Deploy**.
- A private repository needs Hostinger's SSH deploy key added to GitHub (repository → Settings →
  Deploy keys, read-only) and the SSH URL `git@github.com:BizIT-LTD/roofcentre.git`.
- Optional auto-deploy: copy hPanel's webhook URL into GitHub → Settings → Webhooks.

The private `roofcentre-enquiry-config.php` stays one level **above** `public_html` (step 5). The
Git deployment never touches it.

#### Fixing a deployment of `main`

If `main` was deployed, `public_html` contains the whole source project. Check in File Manager
(with hidden files shown) that it holds only these items, then remove them:

| Item | What it is |
|---|---|
| `website/` | the real site, one level too deep |
| `tools/`, `docs/` | build scripts, documentation, screenshots (should not be public) |
| `README.md`, `.gitignore`, `.gitattributes` | repository files |
| `.git/` | Git metadata from the `main` deployment |

If anything else is in `public_html` (for example `default.php` or a file you added), check it before
removing it. Never remove `roofcentre-enquiry-config.php` from the folder above `public_html`. In
hPanel → Git, delete the old repository entry (this only removes the link to GitHub). Then add the
`deploy` branch as above.

---

## Part B: test on the temporary domain (no DNS change)

The `.htaccess` redirects (https/www and old WordPress URLs) only fire on `roofcentre.com.au`, so they
stay inactive on the temporary domain. That is expected.

Check on desktop and mobile:

- [ ] Home, About, Services, all 8 service pages, 3 service-area pages, Projects, FAQ, Contact and
      Privacy all load with images.
- [ ] `/about` (no trailing slash) loads or redirects to `/about/`.
- [ ] A made-up URL shows the Roof Centre 404 page.
- [ ] Call buttons open the dialler (`0431 848 619`). The mobile bottom bar shows Call and Request a Quote.
- [ ] The gallery filter and photo viewer work on `/projects/`.
- [ ] `https://<temporary-domain>/api/enquiry.php` opened in a browser shows "Method not allowed".
- [ ] `https://<temporary-domain>/roofcentre-enquiry-config.php` returns 404 (the file must not be
      reachable on the web).
- [ ] Submit the quote form with real test details. The success message appears and the email arrives
      at the configured address. Check spam too: until SPF is set up (Part C, step 2) the email may be
      filtered. If nothing arrives, check hPanel → Emails for sending limits and
      `docs/ENQUIRY-SETUP.md`.
- [ ] `/sitemap.xml` and `/robots.txt` load.

The Crazy Domains site and email are unaffected throughout Parts A and B.

---

## Part C: go live (LATER, only when approved)

Do this at a quiet time, in **Crazy Domains' DNS manager**, because Crazy Domains holds the
nameservers. Keep the nameservers at Crazy Domains. Do not move DNS to Hostinger as part of this.

### 1. Protect email first (at least 24 hours before step 3)

Add these two records in Crazy Domains DNS for `roofcentre.com.au`:

| Type | Host / name | Value | Priority | TTL |
|---|---|---|---|---|
| A | `mail` (`mail.roofcentre.com.au`) | `103.20.200.233` | | 3600 |
| MX | `@` (`roofcentre.com.au`) | `mail.roofcentre.com.au` | 0 | 3600 |

- `103.20.200.233` is the confirmed address of the Crazy Domains server: it is the live root A
  record that mail uses today, and its mail server accepts mail for `info@roofcentre.com.au`.
- The MX target must be an **A record**, not a CNAME, and must not be `roofcentre.com.au` itself,
  because the root A record moves to Hostinger in step 3.
- Priority 0 matches the cPanel server's own zone file. With a single MX record, any priority works.
- Do not use the server's hostname `cp-wc27.syd02.ds.network` as the MX: it resolves to a different
  IP address (`122.201.124.64`) and has not been tested for this domain.
- Before adding the records, ask Crazy Domains support to confirm that `103.20.200.233` is the correct
  incoming mail server for roofcentre.com.au on this cPanel account. If they give different values,
  use theirs and update this table.

Then check:

- [ ] `nslookup -type=mx roofcentre.com.au ns1.crazydomains.com` shows `mail.roofcentre.com.au`.
- [ ] `nslookup mail.roofcentre.com.au ns1.crazydomains.com` shows `103.20.200.233`.
- [ ] Send a test email from an outside address (for example a Gmail account) to
      `info@roofcentre.com.au`. It arrives at `info@buildingrepaircentre.com.au`.

Email no longer depends on where the website A record points. Do not continue until the test email
arrives.

### 2. SPF and DKIM (use the email providers' values, do not guess)

Today roofcentre.com.au publishes no SPF, DKIM or DMARC records. Once the site is live, the enquiry
form sends from Hostinger's servers with a `@roofcentre.com.au` From address, so SPF should authorise
Hostinger.

- **Hostinger** (website form): get the exact SPF `include` and any DKIM record for PHP mail from
  this website from hPanel (Emails / DNS records) or Hostinger support. Hostinger may not offer DKIM
  for PHP `mail()` from a domain whose email is hosted elsewhere. Note what they confirm.
- **Crazy Domains** (cPanel server): ask whether anything sends **as** `@roofcentre.com.au` from that
  server. If so, get their SPF mechanism and the DKIM record to publish. The forwarder relays outside
  senders' mail, which is checked against the original sender's domain, not roofcentre.com.au.
- Combine every authorised sender into **one** SPF TXT record on `roofcentre.com.au`. Two SPF records
  on the same name make SPF fail.
- Publish each DKIM record exactly as the provider gives it (selector name and key).
- Retest the website form afterwards and check the message headers for `spf=pass`.
- DMARC is optional. If wanted, start later with a monitoring-only policy, once SPF and DKIM pass.

### 3. Point the website to Hostinger

- Lower the TTL of the root and `www` A records to 300 a day beforehand (they are already 300 today).
- Get the website's IP address from hPanel (Websites → Manage → Dashboard / DNS details).
- In Crazy Domains DNS, change the `roofcentre.com.au` A record and the `www.roofcentre.com.au` A
  record to that IP. Leave the `mail` A record, the MX record and any SPF/DKIM records alone.
- If hPanel asks for domain verification, add only the TXT record it asks for.

### 4. SSL

In hPanel, connect `roofcentre.com.au` to this website if not already done, then install the free SSL
certificate once DNS resolves to Hostinger. The `.htaccess` forces `https://www.roofcentre.com.au`,
so install SSL promptly.

### 5. Verify

- [ ] `http://roofcentre.com.au/` redirects to `https://www.roofcentre.com.au/`.
- [ ] Old URLs such as `/roof-replacement/`, `/home/` and `/wp-admin/` behave as listed in
      `docs/MIGRATION-NOTES.md`.
- [ ] The quote form sends and the email arrives.
- [ ] A test email to `info@roofcentre.com.au` still forwards.

### 6. Search Console

Submit `https://www.roofcentre.com.au/sitemap.xml`.

### 7. Keep the old hosting

Keep the Crazy Domains hosting active while it handles roofcentre.com.au email (the `mail` and MX
records point to it) and while it hosts other sites (`buildingrepaircentre.com.au` points to the same
server). Keep the cPanel backup too. Moving email elsewhere or closing that account is a separate,
later decision.

Note: `pergolabuildingcentre.com.au` did not resolve in DNS on 10 Oct 2026, although its files are
on the old server.

---

## Rollback

| If this fails | Undo |
|---|---|
| Part A or B (Hostinger site) | Nothing to undo in DNS. Fix or delete the Hostinger website; the live site is unaffected. |
| Part C, step 1 (test email does not arrive) | Delete the new MX and `mail` A records. Mail goes back to the root A record, which still points to `103.20.200.233`. Then contact Crazy Domains before trying again. |
| Part C, step 2 (SPF/DKIM breaks sending) | Delete or correct the TXT record that was added. |
| Part C, step 3–5 (website problems after cut-over) | Set the `roofcentre.com.au` and `www.roofcentre.com.au` A records back to `103.20.200.233`. The old WordPress site is untouched on Crazy Domains. **Keep the MX and `mail` A records** so email is not disturbed. |

With TTL 300, A record changes and rollbacks take effect for most visitors within minutes; some
resolvers may hold old values for up to an hour.
