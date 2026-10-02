# HANDOVER — dawnedwards-jones.com

Punch list for final upgrades before launch. Every item below was verified against the
files in `src/` on 2 October 2026, not assumed. Figures are real counts.

## State of the build

Better than it looks. The content and SEO foundations are genuinely solid:

- 14 pages, all with unique meta descriptions, canonical tags, Open Graph tags, Twitter
  card tags, favicon references and JSON-LD structured data. All 14. No gaps.
- `robots.txt` and `sitemap.xml` both present and correctly pointed at
  `https://dawnedwards-jones.com`. Sitemap lists all 14 pages.
- `og-image.jpg` present.
- Dropdown navigation works, including a mobile toggle with a JS fallback.
- 9 real client logos in `src/logos/` (Redland City Council, QNMU, Faith Lutheran, UBX
  Birkdale, Kensho Pilates, Bayside Women in Business, Redland Art Gallery, Maybanke,
  Corporate Protection) — real B2B credibility, already in place.
- Copy is written, in Dawn's voice, and approved. Do not rewrite it.

The gaps are infrastructure, not content. Nothing here requires starting over.

---

## P0 — blocks launch

### 1. The enquiry form is not connected to anything

`src/contact.html` has a well-built form: 9 enquiry types covering both B2B and B2C,
fields for `first_name`, `last_name`, `email`, `phone`, `enquiry_type`, `message`.

Its submit handler does this:

```js
f.addEventListener("submit", function(e){
  e.preventDefault();
  document.getElementById("f-done").style.display = "block";
});
```

That reveals a message reading *"Your message has not been sent yet because this form is
still being connected. Please email contact@newdawnwellness.health in the meantime."*

Credit where it's due — that's honest, not a fake success state. But it means **56 CTAs
across the site point at `contact.html`, and none of them currently produce a lead.**
This is the single highest-value fix in the repo.

Wire it to Tekmatix (location `udrK047tPShRFKCOgu0a`). The `enquiry_type` values map
cleanly onto routing, so use them — a keynote enquiry and a 1:1 coaching enquiry should
not land in the same undifferentiated bucket:

| Enquiry type | Suggested routing |
|---|---|
| Keynote speaking | B2B pipeline, tag `speaking-enquiry` |
| Corporate workshop or wellbeing day | B2B pipeline, tag `corporate-enquiry` |
| Menopause policy advisory | B2B pipeline, tag `menopause-policy` |
| Menopause policy implementation | B2B pipeline, tag `menopause-policy` |
| Soul Mastery Ascension (1:1 coaching) | B2C pipeline, tag `ascension-enquiry` |
| Calm to Chaos (business coaching) | B2C pipeline, tag `calm-to-chaos` |
| Podcast guest or interview | tag `podcast-guest` |
| Media enquiry | tag `media` |
| Something else | general enquiry |

Note the `<option>` elements currently carry no `value` attribute — only text. Add explicit
values before wiring, so the payload is stable if the labels are ever reworded.

Confirm the sending domain before any confirmation email goes out — Dawn has a specific
authenticated sender setup and mail sent from the wrong domain silently fails to deliver.

### 2. Decide the generator question — everything else depends on it

`src/` is **generated output**. The source is `generator/build_sites.py`, a single ~197KB
Python file. Edits to the HTML are destroyed on the next build.

Two complications:

- It builds **both** this site and New Dawn Wellness. Only the Dawn Edwards-Jones half is
  in scope here, so roughly half the file is dead weight in this repo.
- It **base64-inlines every photograph straight into the HTML**, which is the direct cause
  of item 3.

Three options. My recommendation is the first.

**a. Convert to Eleventy or Astro (recommended).** Real template files, shared nav and
footer partials, images as separate optimised assets, proper build pipeline. Solves item 3
as a side effect. Biggest upfront effort, best position afterwards — and it makes every
future change cheap instead of awkward.

**b. Keep the Python generator, strip the wellness half.** Cheapest path. Still leaves you
editing a single large Python file to change a heading, and item 3 needs solving separately.

**c. Retire the generator, make the HTML canonical.** Simple to edit, but every nav or
footer change then has to be repeated across 14 files by hand. Workable only because the
page count is small. Expect drift.

Ask Dawn before committing to a route. This is an architecture decision with a real cost
attached and she should choose it knowingly.

### 3. Cross-site nav links point at pages that are not live

The top nav on **all 14 pages** contains a "New Dawn Wellness" dropdown with six links to
`newdawnwellness.health` — The Studio, Pilates & Yoga, Retreats, Wellness Events, Massage &
Healing, The Adawning Experience. `soul-mastery-sanctuary.html` on that domain is also
linked from the "Work With Me" dropdown and from the homepage "Join the group" CTA.

**None of those pages exist yet.** As of 2 October 2026 `newdawnwellness.health` is live but
serving Tekmatix funnel pages, not the new wellness site. Launching this site as-is sends
visitors to broken or wrong destinations from the primary navigation.

Options, in order of preference:

1. Launch both sites together. Cleanest, but couples this launch to the other site's
   timeline.
2. Point those six links at the equivalent live pages on `newdawnpilates.com` (currently
   on Squarespace) until the wellness site ships, then switch them over.
3. Collapse the dropdown to a single link to the wellness homepage and hide the rest until
   their targets exist.

Do not launch with them as they are. Confirm the choice with Dawn.

---

## P1 — fix before launch, but not blocking the decision above

### 4. Page weight is 250–850KB per page because photos are inlined

Current sizes:

| Page | Size |
|---|---|
| index.html | 848 KB |
| contact.html | 492 KB |
| book.html | 485 KB |
| start-here.html | 475 KB |
| calm-to-chaos.html | 437 KB |
| soul-mastery-ascension.html | 420 KB |
| about.html | 414 KB |
| philosophy.html | 390 KB |
| speaking.html | 361 KB |
| podcast.html | 304 KB |
| corporate-workshops.html | 256 KB |
| privacy / terms / menopause-policy | 11–14 KB |

The three small pages are the ones with no photographs — which confirms the cause. Base64
encoding also adds roughly 33% overhead on top of the original file size, and inlined
images cannot be cached separately or lazily fetched, so the cost is paid on every page view.

Fix: extract to real files in `src/images/`, convert to WebP with JPEG fallback, generate
responsive `srcset` variants, keep `loading="lazy"` on everything below the fold. The 29
original photographs are in `generator/photos/` for re-encoding at full quality.

Target under 150KB per page. This matters for Core Web Vitals, which matters for the local
and B2B search visibility this site is built to win.

### 5. HTML double-escaping bug — visible on the page

`&` has been escaped twice in several places, producing the literal string `&amp;` in
rendered text. Affected pages and occurrence counts:

```
about.html               1
contact.html             1
corporate-workshops.html 2
index.html               2
menopause-policy.html    1
speaking.html            1
terms.html               1
```

Visible in page titles — `index.html`'s `<title>` currently renders as
`Pilates, Yoga &amp; Whole-Body Healing`. Fix at the generator level so it cannot recur,
not by patching the output.

### 6. Homepage lead magnet form goes nowhere, and has no magnet

`src/index.html` contains:

```html
<form onsubmit="return false">
  <input type="email" placeholder="Your email address">
  <button class="btn btn-gold" type="submit">Send me the guide</button>
</form>
```

Two problems. The form is a no-op, and **no guide is specified anywhere** — there is no
PDF, no download, no named lead magnet. Wiring the form without creating the asset will
leave subscribers waiting for something that does not exist. Ask Dawn what the guide is
before connecting this.

### 7. Analytics are stubbed out

Every page carries commented-out Google Analytics 4 and Meta Pixel blocks with placeholder
IDs (`G-XXXXXXXXXX`, `PIXEL_ID_HERE`). Nothing is tracking. Dawn needs to supply the real
IDs — see `docs/DAWN-TO-SUPPLY.md`. Once live, add conversion events on form submit and on
each booking widget so the B2B funnel is measurable.

### 8. No discovery-call booking anywhere

`corporate-workshops.html` and `menopause-policy.html` both have "Book a discovery call"
CTAs that resolve to the generic contact form. For a B2B audience, a real calendar converts
considerably better than a form — the prospect gets a time rather than a wait.

Dawn's Tekmatix has no corporate or speaking discovery calendar yet. Once she creates one,
embed it via `https://api.leadconnectorhq.com/widget/booking/<calendarId>`.

`soul-mastery-ascension.html` can be wired immediately — use the **Soul Mastery Alignment
Call** calendar, `7EiIsiDaO3oyu3OXTsjP` (30 minutes, Zoom or phone, Mon–Fri 8am–4pm).

---

## P2 — pre-launch QA

- Run every page through Lighthouse; fix anything under 90 on performance or accessibility.
- Move the Google Fonts load out of the CSS. `assets/style.css` pulls Cormorant Garamond and
  Montserrat via `@import`, which no page can start fetching until the stylesheet itself has
  downloaded — two serial round trips before any text renders in the right typeface. Replace
  with `<link rel="preconnect">` plus a `<link rel="stylesheet">` in each page `<head>`. The
  fonts are correct; only the loading method is wrong.
- Check colour contrast on gold-on-ivory and gold-on-cream combinations against WCAG AA.
  Amber `#f4a261` on ivory `#fdf8f2` is likely to fail for body-size text.
- Test the dropdown nav by keyboard alone, and with a screen reader. The mobile toggle
  relies on JS with no `aria-expanded` state — add it.
- Verify every internal link resolves. 56 point at `contact.html` alone.
- Confirm `og-image.jpg` renders correctly when a page is shared to LinkedIn and Facebook.
- Validate the JSON-LD with Google's Rich Results Test.
- Check all 14 pages at 375px, 768px and 1440px.
- Confirm no reference to the retired 12-hour cancellation policy or $15 late fee has crept
  back in, and that Dawn's private home studio address appears nowhere.
- Submit the sitemap in Google Search Console for `dawnedwards-jones.com`.

---

## Explicitly out of scope

- The New Dawn Wellness site. Separate build, separate repo, separate launch.
- Rewriting Dawn's copy. Flag weak sections, propose alternatives, change nothing without
  her approval.
- Brand colours, fonts and the visual system. Confirmed correct — see `CLAUDE.md`.
- Sending anything to a contact list. Dawn approves all client-facing communication first.
