# Deploying dawnedwards-jones.com to Cloudflare Pages

Chosen because it keeps the site as plain files in a Git repo. That matters for one specific
reason: Claude can read and change files in a repo and open a pull request. Claude cannot
edit a Squarespace, Wix or GoDaddy-builder site, because none of them expose a usable content
API. The hosting choice is what makes ongoing Claude-assisted updates possible at all.

Cost: free tier covers this site comfortably. Unlimited bandwidth, 500 builds a month.

---

## 1. Put the repo on GitHub

```bash
cd dawn-edwards-jones-site
git init
git add .
git commit -m "Initial commit — dawnedwards-jones.com"
git branch -M main
git remote add origin git@github.com:<account>/dawnedwards-jones.git
git push -u origin main
```

Private repo is fine — Cloudflare Pages reads private repos once authorised.

Give Claude Code access at this level: push to branches, open pull requests. Do **not** give
it direct push access to `main`. Every change should arrive as a PR with a preview URL Dawn
can look at before it goes live.

Suggested branch protection on `main`: require a pull request, no force pushes.

---

## 2. Create the Pages project

Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.

| Setting | Value |
|---|---|
| Repository | the repo from step 1 |
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `src` |
| Root directory | *(leave empty)* |

No build command is correct. `src/` is already finished HTML. Cloudflare just uploads it.

If `HANDOVER.md` item 2 is resolved by moving to Eleventy or Astro, this changes to a real
build command (`npx @11ty/eleventy` or `npm run build`) and an output directory of `_site` or
`dist`. Update this file when that happens.

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
The canonical tags in `src/` point at the **non-www** form, so redirect `www` → apex and
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

```
Claude Code (or Dawn) edits a branch
  → opens a PR
  → Cloudflare builds a preview at <hash>.<project>.pages.dev
  → Dawn reviews the preview
  → merge to main
  → live in under a minute
```

Rollback is one click in the Pages deployment history. Every deploy is kept, so a bad change
is never more than a minute from being undone.

Remember the standing rule: **nothing client-facing goes live without Dawn's explicit
approval.** The PR preview exists so she can see it first. Use it.
