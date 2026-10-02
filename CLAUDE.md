# CLAUDE.md — dawnedwards-jones.com

Instructions for Claude Code working in this repo. Read this before touching anything.

## What this site is

The personal-brand and authority site for **Dawn Edwards-Jones** — author, speaker, and
founder of New Dawn Wellness. It is a sibling to `newdawnwellness.health` (a separate
repo and separate site, not in scope here).

This site has **one job**: answer "why Dawn, how do I work with her, how do I bring her
into my organisation?" and convert that into an enquiry or a booked call.

Two audiences, in priority order:

1. **B2B** — corporate decision-makers, HR and wellbeing leads, event organisers, media.
   They arrive for keynote speaking, corporate workshops, or menopause policy advisory.
2. **B2C** — women looking for premium 1:1 coaching (Soul Mastery Ascension) or
   soul-led business coaching (Calm to Chaos).

If a change would make the site better for studio clients looking for Pilates classes,
it belongs on the wellness site, not here.

## Non-negotiables

**Never publish or send anything client-facing without Dawn's explicit approval.** That
includes copy changes on live pages, form confirmation emails, and anything that would go
out to a contact list. Draft it, show her, wait.

**Do not rewrite Dawn's copy.** The words on these pages are approved and in her voice.
Fix typos, fix the HTML-escaping bugs, fix broken links. If you believe a section converts
poorly, say so and propose an alternative — do not swap it in.

**Do not change the brand colours or fonts.** They are confirmed against Dawn's brand
guidelines (see Brand section below). The existing CSS is correct.

**Do not invent a logo.** If a logo asset is missing, leave a clearly marked placeholder
and flag it.

## Brand

Confirmed palette, already correct in the CSS. Do not alter these values.

```
--navy:       #192b53   /* headings, key text, dark backgrounds */
--cream:      #ffead1   /* backgrounds, large areas */
--ivory:      #fdf8f2   /* page background */
--gold:       #f4a261   /* CTAs, highlights */
--orange:     #ee7c19   /* accents, energy */
--forest:     #374a34   /* Soul Mastery sub-brand */
--beige:      #e9cba7   /* soft accents, dividers, cards */
--olive-gold: #a9993e
--burgundy:   #502a1f
```

Typography: **Cormorant Garamond** for headings, **Montserrat** for body. Never substitute.
Body text 16px minimum, line-height 1.6–1.8. Headings sentence case, not ALL CAPS.

Avoid: bright white, neon or saturated colour, cool blues and purples, heavy black
(use navy instead), hot pinks, fitness-brand reds.

Layout principle: **space is breathing room, not waste.** Generous whitespace, wide
margins, one idea per section. If a change makes the page denser, it is probably wrong.

Imagery: natural light, warm tones, real and unposed, grounded environments. Never
gym/fitness-style, corporate stock, cool-toned, or before/after framing.

Logo: `https://assets.cdn.filesafe.space/udrK047tPShRFKCOgu0a/media/69ba2f9e9c981702addae6c0.png`

Brand mood gut check — grounded, calm, supportive, embodied, real, expansive. If a design
feels clinical, rushed, loud, corporate, or fitness-y, revise it.

## Voice

Warm, grounded, emotionally intelligent, direct when it needs to be. Calm authority.
No hype, no urgency, no scarcity, no "boss babe" energy. The brand should feel like
relief, not pressure.

Core message the whole ecosystem reinforces: *"You're not inconsistent. You've been trying
to do everything alone."* Dawn is a self-leadership and nervous-system coach — not a
fitness coach, not a generic mindset coach.

Sales language is invitation-based and relational. Never pushy or deadline-driven.

## Architecture — read this before editing

The site is built with **Eleventy**. Source is in `src/`, output goes to `_site/` (never
edit `_site/`, it is rebuilt every time).

- **Copy lives in `src/pages/*.md`**, as a list of `sections` in each file's front matter.
  Each section's `type` maps to a template in `src/_includes/sections/`.
- **Menu, footer, contact details, analytics IDs** live in `src/_data/site.json`. Header and
  footer are shared partials, so a menu change is one edit.
- **Images**: reference originals like `/images/photos/x.jpg`. The image transform in
  `eleventy.config.js` produces WebP + JPEG, `srcset`, dimensions and lazy loading. Never
  inline images as base64.
- **Pages CMS** (`.pages.yml`) is how Dawn's VA edits text and photos. It only preserves
  fields declared in `.pages.yml`, so **any new field you add to a section template must
  also be added to `.pages.yml`**, or the CMS will silently drop it on the next save.
- **Contact form** posts to `functions/api/enquiry.js` (Cloudflare Pages Function), which
  upserts the contact in Tekmatix, adds tags from `src/_data/enquiry.json`, and attaches the
  message as a note. It needs the `TEKMATIX_API_TOKEN` secret in Cloudflare.
- **Motion** follows `docs/UPGRADE-PROMPT.md`: tokens and the reduced-motion guard are in
  `src/assets/style.css`, behaviour in `src/assets/site.js`. No animation libraries. Sheen
  is used on two elements; the third is reserved for the speaker-kit download button.
- **Links to `newdawnwellness.health` are hidden automatically** while
  `wellnessSiteLive` is `false` in `site.json`. Leave those links in the content; flipping the
  switch brings them all back.

Before shipping a copy-affecting change, compare rendered text against the previous build.
Copy must not drift.

## Tekmatix (the CRM and booking system)

Everything commercial runs through Tekmatix, a GoHighLevel white-label. Dawn's location ID
is `udrK047tPShRFKCOgu0a`. Booking widgets embed as:

```
https://api.leadconnectorhq.com/widget/booking/<calendarId>
```

Live calendars relevant to this site:

| Calendar | ID | Use for |
|---|---|---|
| Soul Mastery Alignment Call (30min, Zoom or phone, Mon–Fri 8am–4pm) | `7EiIsiDaO3oyu3OXTsjP` | Ascension 1:1 enquiries |
| Holistic Health Strategy Session | `8rs01DaXV0POzk8S96I9` | General strategy calls |
| Wellness Retreat Connection Call | `qs9qb6brKdn6EWUp2BN6` | Retreat enquiries |
| Dawn Edwards-Jones Personal Calendar | `GsXtcUaFqeU2FfwwKJSn` | Fallback / ad-hoc |

`Free 15 Minute Consult` (`zUZ27bXMmnGOu9O4lnKP`) exists but is **inactive** — do not use
it without asking Dawn to reactivate it.

There is **no corporate or speaking discovery calendar yet.** The "Book a discovery call"
CTAs on the corporate workshops and menopause policy pages currently open the enquiry form
with the right topic preselected. When Dawn creates the calendar, add a `calendar` section.
See `docs/DAWN-TO-SUPPLY.md`.

Relevant products: Soul Mastery Ascension `6a18178e5e7d1e7aef6b9acc`,
Soul Mastery Sanctuary `6922785fbeeb5a99c08307c5`.

## Site facts — use these exact values

- Contact email: **contact@newdawnwellness.health** (not admin@newdawnpilates.com)
- Phone: **+61 429 460 733**
- Studio address (public, safe to display): **4 Cross Street, Cleveland QLD 4163**
- Dawn's **private home studio address must never be published.** It is used for
  hands-on healings only and is sent to clients on booking.
- The old 12-hour cancellation notice and $15 late fee **no longer apply.** Never
  reintroduce them into any copy.

## Cross-site links

The top nav has a "New Dawn Wellness" dropdown pointing at six pages on
`newdawnwellness.health`, plus Soul Mastery Sanctuary links on several pages. **Those pages
are not live yet**, so Dawn decided (2 October 2026) to hide them until the wellness site
launches. They are hidden by the `wellnessSiteLive` switch in `src/_data/site.json`, not
deleted.

## Working style Dawn expects

Give her 1–3 key actions, not long lists. Be concise and concrete. Challenge her directly
when something is weak rather than agreeing to be agreeable — she has explicitly asked for
this. No fluff, no hype, no filler enthusiasm.

When you finish a piece of work, say what the outcome was in a sentence or two. She has
been following along; she does not need a recap of every step.
