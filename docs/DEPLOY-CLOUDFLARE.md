# Deploying dawnedwards-jones.com to Cloudflare Pages

Chosen because it keeps the site as plain files in a Git repo. That matters for one specific
reason: Claude can read and change files in a repo and open a pull request. Claude cannot
edit a Squarespace, Wix or GoDaddy-builder site, because none of them expose a usable content
API. The hosting choice is what makes ongoing Claude-assisted updates possible at all.

Cost: free tier covers this site comfortably. Unlimited bandwidth, 500 builds a month.

---

## 1. The repo

The site lives at `github.com/DawnEdwardsJ/DEJWebsite`. `main` is production. Changes arrive
as pull requests from branches, each with a Cloudflare preview URL Dawn can check first.

Recommended: make the repo **private** (Settings → Change visibility). Cloudflare Pages and
Pages CMS both work with private repos once authorised.

Suggested branch protection on `main`: require a pull request, no force pushes. Pages CMS
edits by the VA commit to `main` directly; that is intended for text and photo changes.

---

## 2. Create the Pages project

Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → choose
`DawnEdwardsJ/DEJWebsite`.

| Setting | Value |
|---|---|
| Production branch | `main` |
| Framework preset | Eleventy (or None) |
| Build command | `npm run build` |
| Build output directory | `_site` |
| Root directory | *(leave empty)* |

Node 22 is picked up from `.nvmrc`. The `functions/` folder is detected automatically and
becomes `/api/enquiry`. `_headers` (security and caching) and `_redirects` (old `.html`
addresses → clean addresses) are copied into the output by the build.

### The contact form secret

The enquiry form needs one secret, or it tells visitors to email instead:

1. Tekmatix → Settings → **Private Integrations** → create one named "Website enquiry
   form" with scopes to **view and edit contacts** (contacts, contact tags, contact notes).
   Copy the token.
2. Cloudflare → the Pages project → Settings → **Variables and Secrets** → add
   `TEKMATIX_API_TOKEN` (type: Secret) for Production *and* Preview → redeploy.
3. Submit a real test enquiry on the preview URL and confirm the contact appears in
   Tekmatix with the `website-contact-dej` tag plus the topic tags (see
   `src/_data/enquiry.json`).

Each enquiry type adds tags (`b2b-enquiry` / `b2c-enquiry` plus a topic tag such as
`speaking-enquiry`). Build Tekmatix workflows on those tags for pipeline placement,
notifications and any confirmation email. Confirm the authenticated sending domain before
switching a confirmation email on.

### Spam protection (recommended before any confirmation email is switched on)

The form has a hidden honeypot field. For stronger protection, add Cloudflare Turnstile
(free): Cloudflare → Turnstile → add the site → copy the **site key** into Pages CMS → Site
settings → "Cloudflare Turnstile site key", and add the **secret key** to the Pages project
as `TURNSTILE_SECRET_KEY`. Both are optional, and the form works without them.

If Tekmatix can't be reached, the function logs the full enquiry so it can be followed up
by hand. Turn on Workers Logs for the Pages project so those logs are kept.

First deploy lands at `<project-name>.pages.dev`. Check the 14 pages there before touching DNS.

---

## 3. Point the domain

The domain is registered at **GoDaddy**. Two routes.

### Route A — move DNS to Cloudflare (recommended)

Add the domain as a site in Cloudflare, let it scan existing records, then change the
nameservers at GoDaddy to the two Cloudflare gives you. Propagation is usually under an hour,
occasionally up to 24.

Why this is better: apex-domain support without CNAME flattening workarounds, automatic TLS,
caching and analytics, and redirect rules you can configure in one place. It also means
future DNS changes happen where the hosting lives rather than split across two providers.

Before you switch nameservers, copy every existing GoDaddy record across — especially **MX
and TXT records**. If `dawnedwards-jones.com` has email on it, missing an MX record silently
breaks mail. Check SPF, DKIM and DMARC TXT records too.

Then in Pages → Custom domains, add `dawnedwards-jones.com` and `www.dawnedwards-jones.com`.
Cloudflare creates the records and issues the certificate itself.

### Route B — keep DNS at GoDaddy

Add the custom domain in Pages, then at GoDaddy:

| Type | Name | Value |
|---|---|---|
| CNAME | `www` | `<project-name>.pages.dev` |
| A or forward | `@` | per the values Pages displays |

GoDaddy does not support CNAME at the apex, so the root domain needs either their forwarding
feature or the A records Cloudflare shows you. Workable, more fiddly, fewer features. Route A
unless there's a reason.

### Pick one canonical host

Either `dawnedwards-jones.com` or `www.dawnedwards-jones.com` — not both serving content.
The canonical tags point at the **non-www** form, so redirect `www` → apex and
leave the tags alone.

---

## 4. Redirect newdawnpilates.com

Currently on Squarespace, holding real local search authority built up over years. Throwing
that away would be an own goal.

Important: the old Pilates content is destined for the **New Dawn Wellness** site, not this
one. So most newdawnpilates.com URLs should eventually redirect there, not here. Until that
site is live, two sane options:

- Leave newdawnpilates.com alone for now, and do the redirect work as part of the wellness
  site launch. Safest, and it avoids sending studio-class traffic to a speaking-and-coaching
  site where it will bounce.
- Redirect only the pages that are genuinely about Dawn personally (an about or bio page, say)
  to the matching page here, and leave the class and timetable pages where they are.

What not to do: a blanket redirect of every old URL to this homepage. Google treats mass
redirects to an unrelated page as soft 404s and the authority evaporates. Map URL to
equivalent URL, or don't redirect it.

Once the mapping is agreed, Cloudflare Bulk Redirects does this cleanly (Rules → Redirect
Rules → Bulk Redirects), with `301` status and "preserve query string" on.

Confirm the approach with Dawn before changing anything on newdawnpilates.com — it is
currently live and taking real traffic.

---

## 5. After the first production deploy

- Open all 14 pages on the live domain. Check the nav, the logos, the stylesheet, the OG image.
- Verify HTTPS and that HTTP redirects to it. Cloudflare → SSL/TLS → set mode **Full (strict)**
  and turn on **Always Use HTTPS**.
- Submit `https://dawnedwards-jones.com/sitemap.xml` in Google Search Console.
- Confirm `robots.txt` resolves and isn't blocking anything it shouldn't.
- Re-check the enquiry form end to end once it's wired — submit a real test and confirm the
  contact lands in Tekmatix with the right tag.

---

## 6. How updates work from here

Text and photo edits (Dawn or her VA):

```
Pages CMS (app.pagescms.org) → Save
  → commit to main → Cloudflare rebuilds → live in about a minute
```

Design or structural changes (Claude Code or a developer):

```
edit a branch → open a PR
  → Cloudflare builds a preview at <hash>.<project>.pages.dev
  → Dawn reviews the preview → merge to main → live in under a minute
```

Pages CMS setup, once: sign in at app.pagescms.org with GitHub, install the Pages CMS GitHub
App on `DEJWebsite`, then add the VA under Collaborators by email.

Rollback is one click in the Pages deployment history. Every deploy is kept, so a bad change
is never more than a minute from being undone.

Remember the standing rule: **nothing client-facing goes live without Dawn's explicit
approval.** The PR preview exists so she can see it first. Use it.
