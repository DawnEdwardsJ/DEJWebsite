# What only Dawn can supply

Six items. No one else can answer these. Items 1 and 2 are decided; the rest block work that
is otherwise ready to go. Whoever picks up this repo should send Dawn this list before starting.

---

## 1. Decision — the generator question ✅ decided 2 October 2026

Dawn's brief: fast, clean and responsive, editable by a VA without code, no lock-in to a
website builder. Resolved with Eleventy (output is plain HTML, hostable anywhere) plus Pages
CMS for editing (content stays as plain files in this repo). Done.

---

## 2. Decision — the cross-site nav links ✅ decided 2 October 2026

Dawn chose to hide them until New Dawn Wellness is live, so this site can launch first. They
are switched off by `wellnessSiteLive` in Site settings, not deleted. The Soul Mastery
Sanctuary links are hidden too, because their page doesn't exist yet. **Still needed: a live
URL for the Sanctuary**, so the homepage's "Three ways in" has its third door back.

---

## 2a. A Tekmatix Private Integration token (new)

**Blocks:** the enquiry form actually delivering leads.

The form is built and tested. It needs one token: Tekmatix → Settings → Private
Integrations → create one with contacts view/edit access, then paste it into Cloudflare as
`TEKMATIX_API_TOKEN`. Steps in `docs/DEPLOY-CLOUDFLARE.md`. Two minutes of clicking.

---

## 3. GA4 Measurement ID and Meta Pixel ID

**Blocks:** all analytics and conversion tracking.

Every page carries commented-out tracking blocks with placeholders `G-XXXXXXXXXX` and
`PIXEL_ID_HERE`. Nothing is being measured.

- **GA4:** Google Analytics → Admin → Data streams → the web stream for this domain → the
  Measurement ID, format `G-` followed by ten characters. If no property exists for
  dawnedwards-jones.com yet, one needs creating.
- **Meta Pixel:** Meta Events Manager → Data sources → the pixel → its numeric ID. Dawn may
  already have a pixel in use for New Dawn ads; the same one can serve both sites.

Worth saying plainly: without these, there is no way to know whether the B2B pages are
working. The site is built to win corporate enquiries and right now that would be invisible.

---

## 4. The homepage lead magnet — what is "the guide"?

**Blocks:** wiring the homepage email capture.

The homepage has an email field and a button reading **"Send me the guide"**. There is no
guide. No PDF, no named asset, nothing specified anywhere in the repo.

Two things needed:

- What the guide actually is — title, and the PDF or the content to build one from.
- Who it's for. A B2B lead magnet (a menopause policy starter, say, or a wellbeing-day
  planning guide) and a B2C one (a nervous-system reset guide) are different assets and
  different follow-up sequences. This site's primary audience is B2B, so a B2B magnet is
  probably the stronger play — but that's Dawn's call.

If there's no guide and no appetite to make one, the honest fix is to remove the form rather
than collect emails for something that will never arrive.

---

## 5. A corporate / speaking discovery calendar in Tekmatix

**Blocks:** real booking on the two highest-value B2B pages.

`corporate-workshops.html` and `menopause-policy.html` both have "Book a discovery call" CTAs
that currently fall back to the generic contact form. For a corporate decision-maker, a
calendar converts considerably better than a form — they get a time instead of a wait.

Dawn's Tekmatix has no such calendar. The existing ones are all wellness or 1:1 coaching:

| Calendar | ID | Status |
|---|---|---|
| Soul Mastery Alignment Call | `7EiIsiDaO3oyu3OXTsjP` | Active — fine for Ascension |
| Holistic Health Strategy Session | `8rs01DaXV0POzk8S96I9` | Active |
| Wellness Retreat Connection Call | `qs9qb6brKdn6EWUp2BN6` | Active |
| Dawn Edwards-Jones Personal Calendar | `GsXtcUaFqeU2FfwwKJSn` | Active |
| Free 15 Minute Consult | `zUZ27bXMmnGOu9O4lnKP` | **Inactive** |

Create one new calendar — something like "Corporate Discovery Call", 30 minutes, Zoom,
business hours — and send the calendar ID. It embeds as
`https://api.leadconnectorhq.com/widget/booking/<calendarId>`.

`soul-mastery-ascension.html` doesn't need to wait; it can be wired to
`7EiIsiDaO3oyu3OXTsjP` immediately.

---

## 6. Confirmation of the sending domain

**Blocks:** any confirmation email going out from the enquiry form.

Dawn has a specific authenticated sender setup, and mail sent from the wrong domain fails to
deliver silently — no bounce, no error, the lead just never hears back. Before a single
confirmation email is configured, confirm the exact from-address and sending domain to use.

The site's public contact address is **contact@newdawnwellness.health**. Whether that is also
the correct authenticated *sending* domain needs checking, not assuming.

---

## Not needed from Dawn

For clarity, so nobody asks her twice:

- **Brand colours, fonts, logo** — confirmed and already correct in the CSS. See `CLAUDE.md`.
- **The copy** — written, in her voice, approved. Flag weak sections, don't rewrite them.
- **Photographs** — 29 originals are in `generator/photos/` at full quality.
- **Client logos** — 9 real ones already in `src/logos/`.
- **Tekmatix location ID** — `udrK047tPShRFKCOgu0a`.
- **Site facts** — phone, public studio address and contact email are all in `CLAUDE.md`.
  Her private home studio address must never be published.
