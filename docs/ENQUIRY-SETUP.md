# Enquiry form setup

The quote/contact form posts to `/api/enquiry.php`, which emails the enquiry using PHP `mail()`.
It has not been tested on a live server yet (PHP is not installed on the development machine).
Locally, `tools/serve.py` mocks the endpoint and prints enquiries to the console.

## What the old WordPress site did

The Elementor forms in database `roofcent_wp1` sent to:

| Form | Sent to | From |
|---|---|---|
| Contact page form | the owner's personal Gmail address | email@roofcentre.com.au |
| Home page "Request a Quote" form | the owner's personal Gmail address | email@roofcentre.com.au |
| "Request a Quote" popup | info@roofcentre.com.au (copy to the owner's personal Gmail address) | info@roofcentre.com.au |

On the old cPanel server (Crazy Domains), `info@roofcentre.com.au` is **a forwarder** to
`info@buildingrepaircentre.com.au`, not a mailbox. Live DNS has no MX record, so mail for
roofcentre.com.au follows the root A record to that server. See `DEPLOY-HOSTINGER.md` before changing
any DNS.

The new handler sends to **info@roofcentre.com.au** by default. Confirm which address(es) should
receive enquiries.

## Private settings (outside the web root and outside Git)

Settings live in `roofcentre-enquiry-config.php` **in the folder that contains `public_html`**.
`enquiry.php` looks two levels up from `public_html/api/`.

| Host | Path |
|---|---|
| Hostinger | `/home/u123456789/domains/roofcentre.com.au/roofcentre-enquiry-config.php` (your own `u…` number) |
| cPanel | `/home/<account>/roofcentre-enquiry-config.php` |

Start from `docs/roofcentre-enquiry-config.example.php`. The real file is listed in `.gitignore`
and must never be placed in `public_html` or committed.

```php
<?php
return [
    'to'        => 'info@roofcentre.com.au',
    'bcc'       => '',                          // optional second recipient
    'from'      => 'website@roofcentre.com.au', // an address on the domain
    'from_name' => 'Roof Centre Website',
];
```

Without this file, the defaults in `website/api/enquiry.php` are used.

## Needed before go-live

1. **Recipient:** confirm the address(es). While DNS still points to Crazy Domains, mail to
   `info@roofcentre.com.au` is delivered by Crazy Domains and forwarded as above.
2. **Sender, SPF and DKIM:** the form sends from Hostinger's servers using a `@roofcentre.com.au`
   From address. roofcentre.com.au currently publishes no SPF, DKIM or DMARC records (the SPF and DKIM
   in the cPanel backup's zone file are not live). Get the exact values from Hostinger (and from
   Crazy Domains, if anything sends as the domain from there) and publish one combined SPF record.
   See `DEPLOY-HOSTINGER.md`, Part C, step 2.
3. **Test:** submit the form on the Hostinger temporary domain and on the live domain after cut-over,
   and check the spam folder.
4. **If `mail()` is unreliable:** switch to authenticated SMTP (for example with PHPMailer). Keep the
   SMTP password in the private config file above, never in `public_html` or Git.

## Spam protection included

Hidden honeypot field, a minimum fill time of 3 seconds, a same-origin check, a limit of 8 enquiries
per hour per IP, header-injection guards and server-side validation. No CAPTCHA is used. If spam
becomes a problem, consider adding Cloudflare Turnstile.
