# Elevation framework — dawnedwards-jones.com

How to take this site from competent to bespoke-tier for a corporate speaking buyer, without
touching the brand.

Read `CLAUDE.md` first for the hard constraints, and `HANDOVER.md` for the launch blockers.
This document sits on top of both. It does not replace them, and it does not override the
non-negotiables.

---

## The honest starting point

Motion makes a credible site feel expensive. It cannot make an under-evidenced site credible.

A head of HR with a $15–40k speaker budget decides in roughly ten seconds whether Dawn is at
their level. What settles that is evidence: footage of her on a stage, named organisations,
specific talk titles with specific outcomes, and something they can forward to a committee.
Right now the site has nine real client logos — genuinely good — and almost none of the rest.
There is no showreel, no speaker one-pager, no named signature talks, and no calendar.

So the work splits in two, and the order matters:

**Track A — evidence and conversion.** What makes a corporate buyer trust and book her.
**Track B — craft and motion.** What makes the site feel like it belongs to someone who
commands that fee.

Track B on its own produces a beautiful site that doesn't convert. Track A on its own
produces a convincing site that feels mid-market. Do both. Start A first, because it
determines what Track B is animating.

---

## On shimmer specifically

Shimmer, done one way, reads as hand-finished luxury: a slow, low-opacity sheen travelling
once across a gold element, over about three seconds. Done the other way it reads as a
discount-code banner — glitter, sparkles, fast repeating glints, anything that twinkles.

The brand guide is explicit: *"subtle fade only — no animations that feel energetic."* So the
rule here is a **sheen, not a sparkle**, on no more than three elements across the whole site,
and never on body text. Everything below is built to that standard. If a motion choice would
look at home on a fitness brand or a Black Friday page, it is wrong for this one regardless of
how well it is executed.

---

## Phases

Sequential by necessity. Until the architecture question in `HANDOVER.md` item 2 is settled,
everything funnels through one 197KB Python file, and parallel agents editing it will collide.
Resolving that first is what makes the rest of this work parallelisable.

### Phase 0 — Foundation (blocks everything)

One agent. No visual decisions.

- Resolve the generator question (`HANDOVER.md` item 2). Eleventy or Astro is the recommended
  route and the only one that makes later phases cheap.
- Extract base64 images to real files, WebP with JPEG fallback, responsive `srcset`,
  `loading="lazy"` below the fold. Originals at full quality are in `generator/photos/`.
- Move the Google Fonts load out of the CSS `@import` into `<link rel="preconnect">` plus
  `<link rel="stylesheet">` in the head.
- Fix the double-escaped `&amp;` at generator level.

Exit condition: every page under 150KB, Lighthouse performance 90+ on mobile, one shared nav
and footer partial, and a heading can be changed by editing one file.

**Motion work cannot start before this is done.** Animating a page that takes four seconds to
paint makes the site feel slower, not more premium.

### Phase 1 — Evidence and conversion

Can run in parallel with Phase 2 once Phase 0 is complete.

In rough order of commercial value:

1. **Showreel.** The single highest-converting asset on any speaker site. Two to three minutes
   of Dawn on stage, audience visible, cut to show range. Above the fold on `speaking.html`,
   and a shorter cut on the homepage. If no footage exists, this becomes a request to Dawn, and
   it should be framed as the highest-priority thing she can produce.
2. **Speaker kit as a downloadable PDF.** Bio in three lengths, high-res headshots, talk
   titles and outcomes, AV and room requirements, travel notes, logos, testimonials. This is
   what gets forwarded to the person who signs off. Also solves the dead "Send me the guide"
   form (`HANDOVER.md` item 6) by giving it a real asset for the B2B audience.
3. **Signature talks, named and specified.** Three to four, each with a title, the audience it
   suits, three outcomes a delegate leaves with, available formats and durations. Vague
   "workshops available" loses to a competitor with named talks every time.
4. **Discovery calendar on the B2B pages.** Dawn needs to create one in Tekmatix — see
   `docs/DAWN-TO-SUPPLY.md` item 5. A corporate buyer given a time converts far better than one
   given a form.
5. **Enquiry form wired to Tekmatix** with the routing table in `HANDOVER.md` item 1.
6. **Testimonials attributed to a role and an organisation.** An unattributed quote is worth
   close to nothing to a procurement-minded reader.

Copy constraint: Dawn's existing copy is approved and must not be rewritten. New copy for new
sections is drafted and shown to her — never published without her explicit approval.

### Phase 2 — Motion and craft

One agent builds the motion token layer first, as a single shared system. Only then is it
applied page by page. Do not let individual pages invent their own timings; inconsistent
easing is the clearest tell of an amateur build.

Build order: tokens → reduced-motion guard → scroll reveal → nav → hero → media → logos →
buttons → the three sheen elements → page transitions.

The full specification is in `docs/UPGRADE-PROMPT.md`, including the CSS. It is deliberately
library-free: native CSS plus one IntersectionObserver is about 3KB and gets substantially all
of the effect. GSAP, ScrollTrigger and Lenis together are around 150KB, which on a site already
fighting page weight is a bad trade. If an agent proposes an animation library, it needs to
justify the kilobytes against a named effect that cannot be achieved natively.

### Phase 3 — Review gates

These run after, and they have teeth. Any one of them failing sends work back.

**Brand guardian.** Checks every change against `CLAUDE.md` and the brand guide. Veto power on
anything that reads clinical, rushed, loud, corporate or fitness-y. Confirms no colour, font or
approved-copy change has crept in.

**Performance.** Lighthouse on all 14 pages, mobile throttled. Performance ≥90, LCP under 2.0s,
CLS under 0.05, INP under 200ms, every page under 150KB.

**Accessibility.** This is a procurement requirement for corporate clients, not a nice-to-have.
`prefers-reduced-motion: reduce` must remove all motion. Full keyboard navigation with visible
focus states. `aria-expanded` on the nav toggle, which is currently missing on all 14 pages.
Contrast AA on all body text — amber `#f4a261` on ivory `#fdf8f2` will likely fail and needs
checking honestly rather than waved through.

---

## Agent roles

Five, with clear ownership so they don't overwrite each other.

| Role | Owns | Must not |
|---|---|---|
| **Architect** | Build system, image pipeline, partials, deploy config | Make visual or copy decisions |
| **Motion designer** | The token layer and its application | Introduce a library without justifying the weight; invent per-page timings |
| **Conversion strategist** | Evidence assets, CTA paths, form and calendar wiring | Publish any copy without Dawn's approval |
| **Brand guardian** | Veto on brand drift | Rewrite — flags and proposes, Dawn decides |
| **QA auditor** | Performance, accessibility, cross-browser, 375/768/1440 | Sign off on anything unmeasured |

Running Architect and Motion designer concurrently before Phase 0 completes will produce merge
conflicts in the generator. Don't.

---

## Guardrails

Carried from `CLAUDE.md`, restated because they are the ones most likely to be broken while
chasing polish:

- **Nothing client-facing goes live without Dawn's explicit approval.** Every change arrives as
  a pull request with a Cloudflare preview URL. She looks, then it merges.
- **No colour or font changes.** The palette and the Cormorant/Montserrat pairing are confirmed.
- **No rewriting Dawn's copy.** Flag weak sections, propose alternatives, change nothing
  unilaterally.
- **Her private home studio address is never published**, in any form, including schema markup.
- **The retired 12-hour cancellation notice and $15 late fee never reappear.**
- **Density is a failure mode.** The brand's layout principle is that space is breathing room.
  If an elevation makes a page denser, it is the wrong elevation.

---

## Banned, regardless of how well executed

Each of these actively lowers perceived tier for this audience and this brand:

Bounce and spring easing. Parallax backgrounds. Custom cursors. Typewriter text. Autoplaying
carousels. Scroll-jacking or smooth-scroll libraries that override native scrolling. Glitter,
sparkle or particle effects. Neon or coloured glows. 3D tilt cards. Confetti. Loading screens
longer than 400ms. Entrance animations on body paragraphs. Anything that moves on a loop in the
reader's peripheral vision while they are trying to read.

A slow one-time count-up on a credential number is acceptable if it runs over at least 1.5
seconds and never repeats.

---

## Done looks like

Measurable, so it can be checked rather than argued about:

- Lighthouse: performance ≥90 mobile, accessibility ≥95, on all 14 pages
- Every page under 150KB; LCP under 2.0s; CLS under 0.05
- Zero motion under `prefers-reduced-motion: reduce`
- Full keyboard traversal with visible focus; `aria-expanded` correct on the nav
- All body text passes WCAG AA contrast
- A corporate buyer landing cold can, within one screen, see Dawn speak, see who has booked
  her, see what she delivers, and book a call
- One shared nav and footer; changing either touches one file
- Every change shipped through a reviewed PR with a preview Dawn approved

---

## The question to ask at the end

Not "does this look premium." Ask:

*Would a head of people at a listed company forward this to their CEO as the speaker for the
national conference?*

If the honest answer is no, find the reason. It will almost never be the animation.
