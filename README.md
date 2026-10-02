# dawnedwards-jones.com

The personal-brand and authority site for **Dawn Edwards-Jones** — author, speaker, and
founder of New Dawn Wellness.

Static site. 14 pages. No framework, no runtime, no database. Deploys to Cloudflare Pages.

**Read `CLAUDE.md` before editing anything.** It covers the brand constraints, the voice,
and — importantly — the fact that the HTML in `src/` is generated output rather than source.
`HANDOVER.md` is the prioritised punch list of what still needs doing before launch.

## Repo layout

```
.
├── CLAUDE.md               Instructions and constraints — read first
├── HANDOVER.md             Prioritised punch list to final release
├── README.md               This file
├── docs/
│   ├── DEPLOY-CLOUDFLARE.md   Hosting, DNS and deploy procedure
│   └── DAWN-TO-SUPPLY.md      The five things only Dawn can provide
├── src/                    Deployable site root (publish this directory)
│   ├── *.html              14 pages
│   ├── assets/style.css    Shared stylesheet
│   ├── logos/              9 client logos
│   ├── og-image.jpg        Social share image
│   ├── robots.txt
│   └── sitemap.xml
└── generator/
    ├── build_sites.py      Python generator that produced src/
    └── photos/             29 original photographs at full quality
```

## The 14 pages

| File | Purpose |
|---|---|
| `index.html` | Homepage |
| `about.html` | Dawn's story |
| `philosophy.html` | Method and approach |
| `start-here.html` | Orientation / audience router |
| `speaking.html` | Keynote speaking (B2B) |
| `corporate-workshops.html` | Corporate workshops and wellbeing days (B2B) |
| `menopause-policy.html` | Menopause policy advisory and implementation (B2B) |
| `soul-mastery-ascension.html` | 1:1 premium coaching (B2C) |
| `calm-to-chaos.html` | Soul-led business coaching (B2C) |
| `podcast.html` | The Adawning Podcast |
| `book.html` | Dawn's book |
| `contact.html` | Enquiry form — 56 CTAs across the site point here |
| `privacy.html` | Privacy policy |
| `terms.html` | Terms |

## Running it locally

`src/` is plain static files, so any static server works:

```bash
cd src
python3 -m http.server 8000
# → http://localhost:8000
```

Opening the files directly with `file://` mostly works, but relative asset paths and the
dropdown nav behave more predictably over HTTP. Use the server.

## Rebuilding from the generator

```bash
cd generator
python3 build_sites.py
```

Two things to know before you run that:

1. It builds **both** this site and New Dawn Wellness. Only the Dawn Edwards-Jones half
   matters here; the wellness half is dead weight in this repo.
2. It **overwrites the HTML**, and it base64-inlines every photograph into the output, which
   is why pages are 250–850KB. This is `HANDOVER.md` item 2 — the architecture decision that
   most other work depends on.

Until that decision is made, treat `build_sites.py` as the source of truth and `src/` as
disposable build output.

## Deploying

Cloudflare Pages, auto-deploying from the `main` branch of this repo, publish directory
`src`, no build command. Domain is registered at GoDaddy. Full procedure, DNS records and
the newdawnpilates.com redirect plan are in `docs/DEPLOY-CLOUDFLARE.md`.

Pull requests get automatic preview URLs, which is the right way to show Dawn a change
before it goes live.

## Before you launch

Three things block launch, all detailed in `HANDOVER.md`:

1. The enquiry form submits to nothing. 56 CTAs lead to a dead end.
2. The generator architecture question needs Dawn's decision.
3. The top nav on all 14 pages links to six `newdawnwellness.health` pages that don't exist yet.

## Scope

In scope: this site. Out of scope: the New Dawn Wellness site (separate repo, separate
launch), rewriting Dawn's approved copy, and changing the brand colours or fonts.
