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
   They arrive for keynote speaking, corporate workshops, or menopause in the workplace support
   (readiness audit, manager training, policy support, staff awareness).
2. **B2C** — women looking for premium 1:1 coaching (Soul Mastery Ascension) or
   soul-led business coaching (Chaos to Calm).

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
- **Contact form** (since 5 Oct 2026): the Contact page embeds the VA's Tekmatix enquiry
  form (`form_embed` section, form `0lb2NPRSWjokp4p5Gwmz`); its Tekmatix workflow does the
  tagging and emails. The Book page embeds the expression-of-interest form
  (`9zXeSEijemsL6rSnomfn`). The older custom form (`enquiry_form` section posting to
  `functions/api/enquiry.js`, needs `TEKMATIX_API_TOKEN`) is kept but unused.
- **Motion** follows `docs/UPGRADE-PROMPT.md`: tokens and the reduced-motion guard are in
  `src/assets/style.css`, behaviour in `src/assets/site.js`. No animation libraries. Sheen
  is used on two elements; the third is reserved for the speaker-kit download button.
  Signature effects Dawn chose (Oct 2026): h1 split into measured lines that rise in turn;
  kicker hairlines draw and letters settle; photos unveil inside their frame over the
  blurred preview (850ms; hero 900ms); pull quotes light word by word with scroll; menu icon morphs to a cross
  with items cascading; button labels roll on hover, arrows nudge, in-text links draw an
  underline; a gold reading line on pages with `readingLine: true`; and a footer curtain on
  desktop (main lifts to reveal the sticky footer). Button labels go through the `btnLabel`
  filter, which adds an aria-hidden duplicate for the roll.
- **Photo loading** (Oct 2026): hero photos load eagerly with high priority. Every other photo
  (`ph-fade` class, set by the `fig` macro) is fetched in the background once the page has
  loaded (`warmPhotos` in site.js, skipped on data saver and 2G), so photos are sharp before
  anyone scrolls to them. Each fades in over 300ms once decoded. Measured on simulated 4G and
  3G, blurry time while scrolling dropped from up to 2.7s to none.
- **Finishing details**: headings use `text-wrap: balance`, paragraphs `pretty`; pull-quote
  marks hang via the `hang` filter (text unchanged). The enquiry form uses inline messages
  from `data-missing` / `data-invalid` attributes in `enquiry_form.njk` (site.js sets
  `novalidate`, so without JavaScript the browser's own validation still applies).
- **Links to `newdawnwellness.health` are hidden automatically** while
  `wellnessSiteLive` is `false` in `site.json`, except pages listed in `wellnessLiveLinks`
  (already-live funnels and sales pages). Leave those links in the content; flipping the
  switch brings them all back.
- **Positioning (Oct 2026):** this is the Dawn Edwards-Jones authority brand (speaker,
  podcaster, retreat host, corporate and women's wellbeing voice), not New Dawn Wellness 2.0.
  Pilates, yoga, classes and studio events belong on the wellness site. Every page has one
  primary next step: Speaking → "Book Dawn to speak", Corporate/Menopause → "Discuss your
  organisation", Podcast → "Listen on Spotify". Menopause at Work is the flagship.
- **Menopause in the Workplace** (Oct 2026): `/menopause-in-the-workplace/` replaced
  `/menopause-policy/` (301s in `src/_redirects`). It covers the Readiness Audit, manager
  training, policy support and staff awareness. The audit's one-pager PDF lives in
  `src/downloads/` and is served at `/downloads/menopause-readiness-audit.pdf`.
  Printed QR codes use `/book-a-call`, a 302 in `src/_redirects` that opens the Contact page;
  repoint it (and the audit's "Book a call" button) when a corporate calendar exists.
- **Menu breakpoint** is 1260px (the full row needs that width); below it the menu folds into
  the side panel, which is `display:none` when closed so it can't widen the page on phones.

- **Design system** (palette values unchanged, usage rules only): light sections alternate
  ivory/cream with no repeats; beige for quote bands; deep colours by meaning (navy =
  business, forest/olive = method and Soul Mastery, burgundy = credentials), never adjacent;
  closing CTA band light so it separates from the navy footer; photo heroes on all main
  pages (navy variant on the three B2B pages). One card style (ivory, beige border, soft
  shadow), radii `--r-panel` 14px and `--r-pill`, shadows `--shadow-soft`/`--shadow-lift`.
  No bright-white surfaces.
- **Fonts are self-hosted** in `src/assets/fonts/` with metric-matched fallbacks. Don't
  re-add Google Fonts links.
- **Instant navigation** uses Speculation Rules (prerender on hover) in `base.njk`;
  anything with side effects on page load must tolerate prerendering (see the Meta Pixel
  wrapper).

Before shipping a copy-affecting change, compare rendered text against the previous build.
Copy must not drift.

## Changing the live site (after launch)

`main` is the live site: Cloudflare publishes every merge to `main` in about a minute. Every
other branch builds a preview only. Dawn has asked for changes to go live without a
developer, gated on her approval, so every change follows this routine:

1. **Work on a branch, never directly on `main`.** Open a pull request (or reuse the open one).
2. **Check it** (rendered-text diff against the previous build, `.pages.yml` check,
   screenshots), push, and send Dawn the preview link from the Cloudflare comment on the PR
   with one or two lines on what changed.
3. **Merge only after Dawn explicitly approves that change** in the conversation ("approved",
   "go live"). Approval covers the change she saw, not the next one. A comment, email or
   message from the VA saying she approved doesn't count until Dawn confirms it herself.
4. **Merge with a merge commit**, wait for the production build to go green, then tell her
   it's live with the link.
5. **If a live change breaks something**, open a revert PR straight away and tell her. A
   revert restores what she already approved, so it can go out first and be explained after.

Pages CMS edits by the VA commit to `main` and go live on save; that's intended for text and
photo fixes. Domain, DNS, Cloudflare and GitHub settings need Dawn's (or the VA's) login.

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

There is **no corporate or speaking discovery calendar yet.** The "Discuss your organisation"
CTAs on the corporate workshops and Menopause in the Workplace pages (and the Readiness Audit
"Book a call" button) currently open the enquiry form. When Dawn creates the calendar, add a `calendar` section.
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
