# Upgrade prompt

Paste the block below into Claude Code at the start of the elevation work. It is written to be
self-contained — the agent has no memory of any prior conversation.

---

## THE PROMPT

You are elevating `dawnedwards-jones.com` from a competent static site to a bespoke-tier
speaker site aimed at corporate buyers with real budgets — heads of people, HR and wellbeing
leads, conference organisers at mid-to-large organisations.

**You are not redesigning it.** The brand is confirmed and correct. Your job is craft: motion,
timing, hierarchy, spacing, and the evidence a corporate buyer needs. Everything you add must
feel like it was always there.

### Read before you start

`CLAUDE.md` for hard constraints. `HANDOVER.md` for launch blockers. `README.md` for structure.
`docs/ELEVATION-FRAMEWORK.md` for phasing, roles and review gates. Do not skip these — several
constraints in them are not inferable from the code.

### Hard constraints — breaking any of these is a failed task

1. **Do not change any colour value.** The palette is confirmed: navy `#192b53`, cream
   `#ffead1`, ivory `#fdf8f2`, gold `#f4a261`, orange `#ee7c19`, forest `#374a34`, beige
   `#e9cba7`, olive-gold `#a9993e`, burgundy `#502a1f`.
2. **Do not change the fonts.** Cormorant Garamond for headings, Montserrat for body. No
   substitutions, no third font.
3. **Do not rewrite existing copy.** It is approved and in Dawn's voice. Fix typos and escaping
   bugs. If a section converts poorly, say so and propose an alternative — do not swap it in.
4. **Nothing goes live without Dawn's explicit approval.** Every change is a pull request with
   a Cloudflare preview URL. Never push to `main`.
5. **Never publish Dawn's private home studio address**, including in schema markup. Only the
   public studio address `4 Cross Street, Cleveland QLD 4163` is safe to display.
6. **Never reintroduce the retired 12-hour cancellation notice or $15 late fee.**
7. **Density is failure.** This brand treats space as breathing room. If a change makes a page
   denser, it is wrong.

### Brand feel — the filter for every decision

Grounded, calm, supportive, embodied, real, expansive. Calm luxury. Feminine without fluff.

The brand must feel like **relief, not pressure**. If a change feels clinical, rushed, loud,
corporate, cold, or fitness-y, revise it. No hype, no urgency, no scarcity.

### Sequence

Work in this order. Do not start motion work before step 1 is complete.

**1. Foundation — blocks everything else.**

`src/` is generated output from `generator/build_sites.py`, a single 197KB Python file that also
builds a second site and base64-inlines every photograph into the HTML. Pages are 250–850KB.

Migrate to Eleventy or Astro: real templates, shared nav and footer partials, images as
optimised assets. Confirm the route with Dawn before starting — `HANDOVER.md` item 2 costs out
the alternatives.

Then: extract images to WebP with JPEG fallback and responsive `srcset` (originals at full
quality are in `generator/photos/`); move the Google Fonts load out of the CSS `@import` into
`<link rel="preconnect">` plus `<link rel="stylesheet">` in the head; fix the double-escaped
`&amp;` that renders as literal `&amp;` on seven pages.

Exit condition: every page under 150KB, Lighthouse performance 90+ mobile.

**2. Evidence — what actually converts a corporate buyer.**

In priority order: a showreel of Dawn on stage, above the fold on `speaking.html` (if no
footage exists, flag this to Dawn as the single highest-value thing she can produce); a
downloadable speaker kit PDF with bio in three lengths, high-res headshots, talk titles and
outcomes, AV requirements and travel notes; three to four named signature talks each with a
title, target audience, three delegate outcomes, and available formats and durations;
testimonials attributed to a role and an organisation rather than a first name; the Soul Mastery
Alignment Call calendar `7EiIsiDaO3oyu3OXTsjP` embedded on `soul-mastery-ascension.html` via
`https://api.leadconnectorhq.com/widget/booking/<calendarId>`; and the enquiry form wired to
Tekmatix location `udrK047tPShRFKCOgu0a` using the routing table in `HANDOVER.md` item 1.

Draft all new copy and show Dawn. Publish none of it without her approval.

**3. Motion — build the token layer first, then apply it.**

Build the shared system before touching any page. Per-page improvised timings are the clearest
tell of an amateur build.

**No animation library.** Native CSS plus one IntersectionObserver is roughly 3KB and achieves
substantially all of this. GSAP plus ScrollTrigger plus Lenis is around 150KB on a site already
fighting weight. If you believe a library is necessary, name the specific effect that cannot be
done natively and justify the kilobytes before adding it.

Tokens:

```css
:root{
  /* expo-out. settled and expensive. never bouncy */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-smooth: cubic-bezier(0.65, 0, 0.35, 1);

  --t-hover: 240ms;
  --t-panel: 420ms;
  --t-reveal: 620ms;
  --t-line: 820ms;
  --t-sheen: 2800ms;

  --stagger: 70ms;
}
```

Reduced-motion guard. Write this immediately after the tokens, before any animation:

```css
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Scroll reveal — the workhorse. Sections and cards only, never body paragraphs:

```css
.reveal{
  opacity:0; transform:translateY(22px);
  transition:opacity var(--t-reveal) var(--ease-out),
             transform var(--t-reveal) var(--ease-out);
}
.reveal.in{opacity:1; transform:none}
```

```js
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.style.transitionDelay = (e.target.dataset.delay || 0) + 'ms';
    e.target.classList.add('in');
    io.unobserve(e.target);
  });
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

Stagger siblings with `data-delay` in multiples of 70ms, maximum four steps. Anything longer
feels like the page is loading badly rather than arriving gracefully.

Hero headline — line-by-line mask reveal. The `<h1>` only, once per page:

```css
.line-mask{overflow:hidden}
.line-mask > span{
  display:block; transform:translateY(105%);
  transition:transform var(--t-line) var(--ease-out);
}
.line-mask.in > span{transform:none}
```

Sticky nav that condenses on scroll past 80px:

```css
.nav{
  transition:padding var(--t-panel) var(--ease-out),
             background var(--t-panel) var(--ease-out),
             box-shadow var(--t-panel) var(--ease-out);
}
.nav.condensed{
  padding-block:10px;
  background:rgba(253,248,242,.88);
  backdrop-filter:blur(12px);
  box-shadow:0 1px 0 rgba(25,43,83,.08);
}
```

Media — slow scale inside a clipped container. 900ms is deliberate; faster reads as cheap:

```css
.media{overflow:hidden}
.media img{transition:transform 900ms var(--ease-out)}
.media:hover img{transform:scale(1.045)}
```

Buttons — lift, never grow:

```css
.btn{
  transition:transform var(--t-hover) var(--ease-out),
             box-shadow var(--t-hover) var(--ease-out);
}
.btn:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 24px -8px rgba(238,124,25,.45);
}
```

Client logos — continuous slow marquee, 45s or slower, pausing on hover, duplicated track for a
seamless loop. Nine real logos are in `src/logos/`. Grayscale at rest easing to full colour on
hover is appropriate here and nowhere else.

**Sheen — read this carefully.** Dawn asked for shimmer. Shimmer done as a slow low-opacity
sweep reads as hand-finished luxury. Shimmer done as glitter, sparkle, or fast repeating glints
reads as a discount banner and will undo the rest of this work.

A sheen, not a sparkle. **Maximum three elements across the entire site.** Never on body text.
Never on a loop in peripheral vision.

```css
.sheen{position:relative; overflow:hidden}
.sheen::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(105deg,
    transparent 35%, rgba(255,255,255,.34) 50%, transparent 65%);
  transform:translateX(-120%);
}
.sheen:hover::after{animation:sheen var(--t-sheen) var(--ease-smooth)}
@keyframes sheen{to{transform:translateX(120%)}}
```

Suggested placement: the primary homepage CTA, the speaker-kit download button, and one gold
divider. Nothing else.

Page transitions: the View Transitions API where supported, a 300ms opacity fade otherwise.
No slide-ins from the edge of the viewport.

**4. Accessibility — a procurement requirement, not a polish item.**

`prefers-reduced-motion: reduce` must remove all motion, verified by actually toggling it.
Full keyboard navigation with visible focus states. `aria-expanded` on the nav toggle, which is
currently absent from all 14 pages. Honest WCAG AA contrast checks on all body text — amber
`#f4a261` on ivory `#fdf8f2` will probably fail at body size; report it rather than passing it.

### Never do these

Bounce or spring easing. Parallax backgrounds. Custom cursors. Typewriter text. Autoplaying
carousels. Scroll-jacking or smooth-scroll libraries overriding native scroll. Glitter, sparkle
or particle effects. Neon or coloured glows. 3D tilt cards. Confetti. Loading screens over
400ms. Entrance animations on body paragraphs. Anything looping in peripheral vision while
someone is reading.

A one-time count-up on a credential number is fine if it runs over 1.5 seconds or more and
never repeats.

### Definition of done

- Lighthouse performance ≥90 mobile and accessibility ≥95, on all 14 pages
- Every page under 150KB; LCP under 2.0s; CLS under 0.05; INP under 200ms
- Zero motion under `prefers-reduced-motion: reduce`
- Full keyboard traversal, visible focus, correct `aria-expanded`
- All body text passes WCAG AA contrast
- Checked at 375px, 768px and 1440px
- One shared nav and footer — changing either touches one file
- A cold corporate visitor can, within one screen, see Dawn speak, see who has booked her, see
  what she delivers, and book a call

### How to report back

Dawn wants concision and directness. Give her one or two sentences on the outcome and **1–3 key
actions**, not a long list. No hype, no filler enthusiasm. If something is weak, say so plainly
and propose the stronger version — she has explicitly asked to be challenged rather than agreed
with. She has been following along and does not need a recap of every step.

### The test to apply before calling anything finished

Not "does this look premium." Ask:

*Would a head of people at a listed company forward this to their CEO as the speaker for the
national conference?*

If the honest answer is no, find the reason. It will almost never be the animation.
