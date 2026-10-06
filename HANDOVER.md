# HANDOVER — dawnedwards-jones.com

Status as of 5 October 2026: Eleventy rebuild, VA amendments and the corporate-visibility pass. The original punch list is in the
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
| Signature motion | Chosen by Dawn from the Motion Lab: line-by-line headlines, drawn hairlines, photo unveil, scroll-lit quotes, menu morph and cascade, rolling buttons, reading line on long pages, footer curtain. Dropdown family names now link to their main page. | CLS 0, performance 98–99, keyboard and reduced-motion tests pass |
| Finishing | Typography: balanced headlines, no stranded last words, hanging quote marks on pull quotes, steady even-width numbers, hairlines both sides of centred labels. Form: calm inline messages instead of browser bubbles, softer focus, menu-style chevron, warm autofill, breathing button while sending, confirmation panel with a drawn tick. Closed phone menu fully hidden (no edge shadow, not reachable by Tab). | Copy diff clean, performance 98–99, keyboard tests pass |
| VA amendments (5 Oct) | Copy and links aligned to the VA's Google Doc: "Soul Mastery — Personal Coaching" replaces the separate Sanctuary/Ascension entries, Chaos to Calm (formerly mislabelled Calm to Chaos) added to the menu and homepage, Spotify link, Ascension and Sanctuary sales pages, New Dawn Reset meditation replaces the missing "3-minute reset" guide, single "New Dawn Wellness" menu link (still hidden), duplicate "Book a discovery call" buttons removed. | Rendered-text diff: only the intended changes |
| Tekmatix forms | New **Form (Tekmatix)** section embeds forms built in Tekmatix, so their workflows (tags, notification and confirmation emails) run. Contact uses the VA's enquiry form (`0lb2NPRSWjokp4p5Gwmz`); the Book page uses the expression-of-interest form (`9zXeSEijemsL6rSnomfn`). The custom form and `functions/api/enquiry.js` stay in the repo, unused, if Dawn ever wants them back. | |
| Live wellness pages | `wellnessLiveLinks` in Site settings lists pages on newdawnwellness.health that already work (meditation opt-in, Ascension and Sanctuary sales pages). Those links show while the rest of the wellness site stays hidden. | |
| Corporate visibility | Homepage hero repositioned ("Keynote Speaker · Menopause & Women's Wellbeing · Podcaster · Retreat Host", first button "Book Dawn to speak"); Menopause at Work flagship section on the homepage; corporate door in "Three ways in"; menu family renamed "Speaking & Corporate"; one primary action per page ("Book Dawn to speak" / "Discuss your organisation" / "Listen on Spotify"); four recent episodes featured on the podcast page; structured data leads with menopause and women's wellbeing. | |
| Layout fixes (5 Oct) | On phones the hidden side menu widened the page by about 330px (sideways drift, in-page links landing short); it is now removed from the page when closed and still slides in. The full desktop menu no longer cramps between 900 and 1260px wide; tablets get the folded menu. | Phone width 390 = 390, keyboard and tap menu tests pass |
| Bugs fixed on the way | Outline buttons invisible on navy bands; hero photo squashed beside text on phones; footer column wrapping; off-centre opt-in small print; three placeholder panels replaced with real photos. | |

### Lighthouse (mobile, simulated throttling)

| | Performance | Accessibility | SEO | LCP | CLS |
|---|---|---|---|---|---|
| Original (4 pages sampled) | 68–90 | 89–90 | 100 | 3.2–5.3s | 0 |
| Rebuild (all 14 pages) | 98–100 | 95–96 | 100 | 1.4–2.1s | 0 |

## Open: before launch

1. **Check the two Tekmatix forms on the preview.** They can't be loaded from the build
   sandbox, so the first real look is on the preview link: the enquiry form on Contact and the
   expression-of-interest form on The Adawning Book. Style them to the brand inside Tekmatix
   (Montserrat, navy text, gold button, no bright white).
2. **Analytics IDs.** Paste the GA4 and Meta Pixel IDs into Site settings when available.
3. **Legal pages** still show "Draft for review". Remove the note once reviewed.
4. **Production branch.** Switch the Cloudflare production branch and the GitHub default
   branch to `main` before attaching dawnedwards-jones.com.

## Open: content only Dawn can supply (5 Oct)

- **Corporate and speaking testimonials:** ✅ from the VA's linked doc ("Speaking Gig - Client
  Testimonial", Maybanke wording as amended by Dawn). Only six exist, so nothing repeats:
  Corporate Workshops has all four workplace ones (Maddy, Jenifer Hasbun, Caroline/Maybanke,
  workplace attendee), Speaking has the two talk/workshop ones (Kirsty Foster, Talia Read),
  and the homepage strip under the hero carries Kirsty's opening line (the Speaking card uses
  her later sentences). Excerpts are verbatim (… marks a cut; "jouney" typo fixed). Maddy is
  attributed without her organisation, per the note in that doc. New headings needing
  approval: "What workplaces say." and "What audiences say." More named corporate
  testimonials would let the homepage carry a proof band again without repeats.
- **Speaking photos:** ✅ four from Dawn (6 Oct) are in: the "Your body knows" talk shot as the
  Speaking hero, the microphone close-up beside "What you get", the wide workshop shot in the
  homepage Menopause at Work section (cropped to remove another practitioner's pull-up banner),
  and an event portrait beside the Contact form (cropped to remove bins). More from the Drive
  folders (75 speaking photos, 11 workshop events) can be added the same way: attach them as
  files in the chat, or upload through Pages CMS → Media. The newer shoot (animal-print kimono,
  desk with laptop) still needs sending as files; the desk shots suit Chaos to Calm.
- **Speaker kit:** short and long bio, headshots, talk descriptions, AV needs, a one-page
  speaker sheet PDF. A page is ready to build once these exist.
- **Retreats & Experiences:** past retreat proof, imagery, and either the next retreat or an
  expression-of-interest form. The About page's "Explore retreats" button stays hidden until
  then (the interim newdawnpilates.com/events link wasn't used, because it lists studio classes).
- **Socials:** ✅ LinkedIn added first in the footer and in the structured data (5 Oct).
  Facebook and Instagram still go to the studio's @newdawnpilates accounts; swap or remove
  them once Dawn decides (personal accounts, or LinkedIn only).
- **Programme name:** ✅ confirmed "Chaos to Calm" (5 Oct). Renamed everywhere; the page moved
  to `/chaos-to-calm/` and the old `/calm-to-chaos/` address redirects there.

## Open: Dawn's call (not changed, flagged)

- **New copy needing approval (5 Oct):** homepage hero sentence ("I help women and workplaces
  navigate midlife, menopause and change with greater wellbeing, confidence and choice.") and
  kicker; the Menopause at Work section's label and lead line ("Flagship keynote & workshop",
  "The conversation most workplaces still aren't having well."); the corporate card text in
  "Three ways in"; button labels "Book Dawn to speak", "Discuss your organisation", "Listen on
  Spotify", "Keep me updated"; podcast "Recent episodes / A few places to start." and the
  one-line episode summaries (taken from the episode descriptions); the homepage page title.
- **Sections the VA's doc doesn't include** (kept): Start Here "You don't have to have it
  figured out" and Philosophy "None of this is theory".
- **Start Here** says "Six ways in" but shows five while the studio door is hidden. Given the
  authority-brand direction, the suggestion is to drop the studio door and say "Five ways in".

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
  form's success/failure messages, plus the form's inline prompts ("Please add your first
  name.", "Please add your email address.", "That email address looks incomplete.",
  "Please choose what this is about."), which live in `src/_includes/sections/enquiry_form.njk`.

## Phase 1 evidence (from `docs/ELEVATION-FRAMEWORK.md`): needs Dawn

Showreel footage, a speaker-kit PDF (the third sheen is reserved for its download button),
named signature talks with outcomes, testimonials attributed to a role and organisation,
and a corporate discovery calendar in Tekmatix. See `docs/DAWN-TO-SUPPLY.md`.
