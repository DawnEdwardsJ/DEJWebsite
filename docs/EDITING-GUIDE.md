# Editing the website: a guide for Dawn's VA

You can change any words, photos, buttons and menu links on dawnedwards-jones.com without
touching code. Edits are made in **Pages CMS**, a free editor that saves straight into the
website's files. About a minute after you save, the live site updates by itself.

---

## Getting in (one-time setup)

1. Dawn invites you. In Pages CMS she opens the site, goes to **Collaborators**, and adds
   your email address. You don't need a GitHub account.
2. Open the invite email and sign in at **https://app.pagescms.org**.
3. Choose **dawnedwards-jones** (the DEJWebsite repository) and the **main** branch.

(For Dawn, the first time only: sign in at app.pagescms.org with GitHub and install the
Pages CMS app on the DEJWebsite repository when it asks.)

---

## What you'll see

The left-hand menu has three areas:

| Area | What it controls |
|---|---|
| **Pages** | One entry per page. Inside each is a list of **sections**, top to bottom. |
| **Site settings** | Top menu, footer, contact email, social links, analytics IDs, and the New Dawn Wellness switch. |
| **Client logos** | The "Trusted to speak & work with" logo strip. |

---

## Common jobs

**Change some words**
Pages → choose the page → open the section → edit the field → **Save**.

**Make a word italic in a heading**
Wrap it in asterisks: `From overwhelm to *calm, embodied leadership.*`

**Swap a photo**
Open the section → click the photo → upload a new one or pick from the library. Then
update **Photo description**. Describe what's in the picture in a short sentence, because
screen readers and Google rely on it. Upload the largest, best-quality version you have.
The site resizes and compresses it automatically.

**Keep a face in frame**
If a photo crops someone's head off, set **Photo focus point** to `center top`.

**Change a button**
Each button has text, a link and a style. Links to pages on this site look like
`/contact/` or `/speaking/`. To send someone straight to the enquiry form with a topic
already chosen, use `/contact/?type=keynote-speaking#enquire`. The topic options are
`keynote-speaking`, `corporate-workshop`, `menopause-policy-advisory`,
`menopause-policy-implementation`, `soul-mastery-ascension`, `chaos-to-calm`,
`podcast-guest`, `media` and `other`.

**Embed a Tekmatix form**
Add a **Form (Tekmatix)** section and paste the form ID: the code after `/widget/form/` in
the embed code Tekmatix gives you. Give it a section ID like `enquire` if buttons should jump
to it (`/contact/#enquire`). Add a photo to show it beside the form. The form's look (fonts,
colours, button) is set inside Tekmatix.

**Two links on one door**
On Start Here, a door can carry a second link (**Second link text** and **Second link**),
like the podcast and book door.

**A small line under a call-to-action band**
Use **Small line underneath**. Links work: `[Find your way in →](/start-here/)`.

**Reorder or add sections**
Drag sections up and down in the list, or use **Add** to insert a new one. Pick the kind of
section from the list (photo + text, cards, testimonials, and so on).

**Switch on the New Dawn Wellness links**
When newdawnwellness.health has its new pages, go to Site settings and tick **New Dawn
Wellness site is live**. Every hidden menu item, footer link and button pointing there
comes back at once.

Some pages on that site already work (the meditation opt-in, the Ascension and Sanctuary
sales pages). They're listed under **New Dawn Wellness pages already live**, and links to
them show even while the switch is off. Add a page's full address there once it's live.

**Add analytics**
Site settings → Analytics → paste the Google Analytics ID (starts `G-`) and/or the Meta
Pixel ID. Leave them blank to switch tracking off.

---

## Keeping the design consistent

The site follows a simple colour rhythm. Sticking to it is what makes it look designed
rather than assembled:

- **Light sections alternate Ivory and Cream.** Never put the same colour twice in a row.
- **Beige is for quote bands** (pull quotes, testimonials).
- **Deep colours carry meaning:** Navy for business and speaking, Forest or Olive for the
  method and Soul Mastery, Burgundy for credentials and numbers. Never two deep sections
  in a row.
- **The last band before the footer is always light**, so it stands apart from the navy
  footer.
- **Every main page opens with a photo banner.** Business pages (Speaking, Corporate
  Workshops, Menopause in the Workplace) use the navy version; the rest use cream.

## House rules

- **Dawn approves all wording before it goes live.** Draft changes and show her first.
  Saving publishes within about a minute.
- **Never add Dawn's private home studio address** anywhere on the site. The only address
  that may appear is the public studio: 4 Cross Street, Cleveland QLD 4163.
- **Never mention the old 12-hour cancellation notice or $15 late fee.** They no longer apply.
- **Colours and fonts are fixed.** The background options in each section are the only
  colour choices, and they're all on-brand.
- **Leave space.** Fewer, calmer sections beat a crowded page.

## If something goes wrong

Every save is recorded. If a change breaks a page, tell whoever looks after the site
technically. Any earlier version can be restored in a minute, either from the GitHub history
or with one click in Cloudflare's deployment list.
