# HANDOVER — dawnedwards-jones.com

Status as of 2 October 2026, after the Eleventy rebuild. The original punch list is in the
first commit on `main` if you need the history.

## Done

| Item | What changed | Evidence |
|---|---|---|
| Generator question | Rebuilt on Eleventy with shared header/footer and section templates. Python generator retired. | `src/`, `eleventy.config.js` |
| Copy | Carried across word for word. | Automated text diff of all 14 pages against the original: the only differences are the intended ones listed below |
| Page weight | Photos are real files: WebP + JPEG, responsive `srcset`, lazy loading, dimensions set. | HTML 10–23KB per page (was 250–850KB) |
| `&amp;` double-escaping | Gone (titles, descriptions, alt text). | |
| Google Fonts | Loaded via `preconnect` + `<link>` in the head, not CSS `@import`. | |
| Enquiry form | Wired to Tekmatix through a Cloudflare Pages Function. Option values and a required topic choice, routing tags per enquiry type, note written before tags (so workflows see the message), phone retried without the number if Tekmatix rejects it, honeypot (logged, not silently dropped), optional Turnstile, no-JS fallback, GA4/Meta lead events. | Tested against a mock Tekmatix API, including the failure paths |
| Discovery-call CTAs | Open the enquiry form with the right topic preselected (`/contact/?type=…#enquire`). | |
| Ascension calendar | Soul Mastery Alignment Call (`7EiIsiDaO3oyu3OXTsjP`) embedded on the Ascension page. | |
| Cross-site links | Hidden while `wellnessSiteLive` is `false` (Dawn's decision). One switch brings them back. | |
| Accessibility | Skip link, visible focus states, dropdowns are real buttons with `aria-expanded`, Escape closes menus, correct heading order, reduced-motion respected everywhere. | Keyboard-only and reduced-motion tests pass |
| Motion | Token system, scroll reveal, hero mask, condensing nav, media scale, button lift, logo marquee, two sheens, View Transitions. No libraries. | |
| VA editing | Pages CMS config for every page, section, setting and logo. | `.pages.yml`, `docs/EDITING-GUIDE.md` |
| Design system | Colour rhythm with no repeated neighbours on any page (13 of 14 had them); photo heroes on all main pages, navy on the three B2B pages; one card style, two corner radii, two shadow depths; grain on every deep section; no bright-white surfaces. | Automated audit of section order |
| Premium details | Self-hosted fonts with preload and metric-matched fallbacks (no font jump, no Google request); instant page loads via prerender-on-hover; header holds still between pages; blurred photo previews with fade-in; branded share card per page; anchor links clear the sticky header. | |
| Bugs fixed on the way | Outline buttons invisible on navy bands; hero photo squashed beside text on phones; footer column wrapping; off-centre opt-in small print; three placeholder panels replaced with real photos. | |

### Lighthouse (mobile, simulated throttling)

| | Performance | Accessibility | SEO | LCP | CLS |
|---|---|---|---|---|---|
| Original (4 pages sampled) | 68–90 | 89–90 | 100 | 3.2–5.3s | 0 |
| Rebuild (all 14 pages) | 98–100 | 95–96 | 100 | 1.4–2.1s | 0 |

## Open: before launch

1. **Tekmatix token.** Create the Private Integration and add `TEKMATIX_API_TOKEN` in
   Cloudflare (steps in `docs/DEPLOY-CLOUDFLARE.md`). Until then the form asks people to email.
   Then build the Tekmatix workflows on the tags in `src/_data/enquiry.json`.
2. **Homepage lead magnet.** The "Send me the guide" form (3-Minute Nervous System Reset)
   still collects nothing, because no guide exists. Dawn decides: supply the guide, or remove the section.
3. **Soul Mastery Sanctuary link.** Hidden with the wellness links because its page doesn't
   exist yet. The homepage card heading still reads "Three ways in" above two cards. Give the
   Sanctuary a live page (or a Tekmatix funnel URL) and it comes back.
4. **Spam protection.** Add Cloudflare Turnstile keys (optional, steps in the deploy guide)
   before any Tekmatix confirmation email goes out, so bots can't trigger mail from the
   sending domain.
5. **Analytics IDs.** Paste the GA4 and Meta Pixel IDs into Site settings when available.
6. **Legal pages** still show "Draft for review". Remove the note once reviewed.

## Open: Dawn's call (not changed, flagged)

- **Colour contrast.** Orange `#ee7c19` and olive-gold `#a9993e` used as small text (kickers,
  card titles, the tagline, nav current state) measure 1.9–2.8:1 on ivory, cream and beige.
  WCAG AA needs 4.5:1. The colours are brand-locked, so nothing was changed. Proposed fix:
  keep orange and olive-gold for large display text and buttons, and set small labels in
  burgundy `#502a1f` or navy, both already in the palette and both well above 7:1. This is
  the only thing keeping accessibility below 100.
- **Placeholder panels.** Three sections had captioned colour blocks instead of photos
  (About → Retreats, Corporate Workshops → "Wellbeing is a business issue", Menopause
  Policy → "A policy is only as good as its practice"). They now use existing photos
  (`nd-circle`, `nd-dawn-leading`, `dawn-portrait-smile`). Swap in the CMS if Dawn prefers others.
- **New copy needing approval:** the Ascension calendar section heading ("Book a Soul
  Mastery Alignment Call.", "30 minutes, by Zoom or phone, Monday to Friday.") and the
  form's success/failure messages.

## Phase 1 evidence (from `docs/ELEVATION-FRAMEWORK.md`): needs Dawn

Showreel footage, a speaker-kit PDF (the third sheen is reserved for its download button),
named signature talks with outcomes, testimonials attributed to a role and organisation,
and a corporate discovery calendar in Tekmatix. See `docs/DAWN-TO-SUPPLY.md`.
