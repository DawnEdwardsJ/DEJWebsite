# dawnedwards-jones.com

The personal-brand and authority site for **Dawn Edwards-Jones**: author, speaker, and
founder of New Dawn Wellness.

Static site, 14 pages, built with [Eleventy](https://www.11ty.dev/). The output is plain
HTML, CSS and images, with no framework, runtime or database. It deploys to Cloudflare
Pages. Day-to-day text and photo edits happen in [Pages CMS](https://pagescms.org) (see
`docs/EDITING-GUIDE.md`), which commits to this repo.

**Read `CLAUDE.md` before changing anything.** It covers the brand constraints and the voice.
`HANDOVER.md` lists what is done and what is still open before launch.

## Repo layout

```
.
├── CLAUDE.md                  Instructions and constraints. Read first
├── HANDOVER.md                Launch checklist and status
├── .pages.yml                 Pages CMS editor configuration
├── eleventy.config.js         Build configuration (Markdown, image optimisation)
├── functions/api/enquiry.js   Cloudflare Pages Function: contact form → Tekmatix
├── docs/
│   ├── EDITING-GUIDE.md       Plain-English guide for whoever edits the site
│   ├── DEPLOY-CLOUDFLARE.md   Hosting, DNS and deploy procedure
│   ├── DAWN-TO-SUPPLY.md      Things only Dawn can provide or decide
│   ├── ELEVATION-FRAMEWORK.md Phasing and review gates for the upgrade work
│   └── UPGRADE-PROMPT.md      Motion and craft specification
└── src/                       Site source
    ├── pages/*.md             The 14 pages. All copy lives in the front matter
    ├── _data/site.json        Menu, footer, contact details, analytics, wellness switch
    ├── _data/logos.json       Client logo strip
    ├── _data/enquiry.json     Enquiry types and the Tekmatix tags each one gets
    ├── _includes/layouts/     Page shell (head, header, footer)
    ├── _includes/partials/    Header and footer, shared by every page
    ├── _includes/sections/    One template per section type (hero, split, cards…)
    ├── assets/style.css       The stylesheet, including the motion system
    ├── assets/site.js         Navigation, scroll reveal, form handling (~3KB, no libraries)
    ├── images/photos/         Original photographs at full quality
    └── images/logos/          Client logos
```

## How a page is made

Each file in `src/pages/` is a list of **sections** in its front matter:

```yaml
sections:
  - type: hero
    kicker: "Keynote Speaking"
    heading: "A voice that lands — and lasts."
    buttons:
      - { label: "Enquire about speaking", link: "/contact/", style: gold }
  - type: logos
  - type: cards
    background: cream
    ...
```

`type` picks a template from `src/_includes/sections/`. The header and footer are shared, so
changing the menu means editing `src/_data/site.json`, one file.

Images referenced in content (e.g. `/images/photos/group1.jpg`) are resized at build time
into WebP and JPEG at several widths, with `srcset`, `width`/`height` and lazy loading added
automatically. Upload the original and let the build handle the rest.

## Running it locally

```bash
npm install
npm start          # http://localhost:8080, rebuilds as you save
npm run build      # writes the finished site to _site/
```

The contact form posts to a Cloudflare Function, which doesn't run under `npm start`. To
test it locally, use `npx wrangler pages dev _site` after a build.

## Deploying

Cloudflare Pages builds from `main`: build command `npm run build`, output directory
`_site`. Every pull request gets a preview URL. Full procedure, the one secret the contact
form needs, and the DNS steps are in `docs/DEPLOY-CLOUDFLARE.md`.

## History

The site was originally produced by a single Python generator that also built the New Dawn
Wellness site and inlined every photo into the HTML (pages were 250–850KB). That generator
and its output are preserved in the first commit on `main`. The copy was carried across word
for word and checked by an automated text comparison against the original pages.
