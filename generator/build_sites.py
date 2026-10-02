# -*- coding: utf-8 -*-
"""Generator for the two New Dawn websites (multi-page, dropdown nav, SEO)."""
import os, shutil, html, base64

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(ROOT, "assets", "photos")
_IMGCACHE = {}
def _img_data(fname):
    if fname not in _IMGCACHE:
        with open(os.path.join(PHOTO_DIR, fname), "rb") as f:
            _IMGCACHE[fname] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
    return _IMGCACHE[fname]
def img(fname, alt, pos=None):
    # pos sets CSS object-position, e.g. 'center top' or '50% 18%', so faces are
    # never cropped out when a tall portrait is shown in a shorter frame.
    style = ' style="object-position:%s"' % pos if pos else ''
    return '<img class="ph" src="%s" alt="%s" loading="lazy"%s>' % (
        _img_data(fname), html.escape(alt, quote=True), style)
def photofig(fname, alt, tone="gold", pos=None):
    return '<div class="fig %s has-img">%s</div>' % (tone, img(fname, alt, pos))
SITES_DIR = os.path.join(ROOT, "sites")
LOGO = "https://assets.cdn.filesafe.space/udrK047tPShRFKCOgu0a/media/69ba2f9e9c981702addae6c0.png"
PHONE = "+61 429 460 733"
EMAIL = "contact@newdawnwellness.health"
ADDRESS = "4 Cross Street, Cleveland QLD 4163"

# ---------------------------------------------------------------- shared CSS
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');
:root{
  --navy:#192b53; --forest:#374a34; --cream:#ffead1; --ivory:#fdf8f2;
  --gold:#f4a261; --orange:#ee7c19; --beige:#e9cba7; --burgundy:#502a1f;
  --olive-gold:#a9993e; --accent:#f4a261; --accent-deep:#ee7c19;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Montserrat',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  color:var(--navy);background:var(--ivory);line-height:1.75;font-weight:300;font-size:17px}
h1,h2,h3,h4{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;line-height:1.15;letter-spacing:.5px}
h1{font-size:clamp(2.4rem,5vw,4rem)}
h2{font-size:clamp(1.9rem,3.5vw,2.9rem)}
h3{font-size:1.4rem}
a{color:inherit;text-decoration:none}
p{margin-bottom:1.1em;max-width:64ch}
img{max-width:100%;display:block}
.wrap{width:min(1160px,90%);margin:0 auto}
.kicker{font-size:.72rem;letter-spacing:3px;text-transform:uppercase;color:var(--accent-deep);font-weight:600;margin-bottom:18px}
.say{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.5rem;color:var(--navy);line-height:1.4}
.btn{display:inline-block;font-family:'Montserrat';font-size:.8rem;letter-spacing:1.5px;text-transform:uppercase;
  font-weight:600;padding:15px 32px;border-radius:999px;transition:.25s;cursor:pointer;border:1.5px solid var(--accent)}
.btn-gold{background:var(--accent);color:var(--navy)}
.btn-gold:hover{background:var(--accent-deep);border-color:var(--accent-deep);color:#fff}
.btn-ghost{background:transparent;color:var(--navy);border-color:var(--navy)}
.btn-ghost:hover{background:var(--navy);color:var(--cream)}
.btn-row{display:flex;flex-wrap:wrap;gap:14px;margin-top:26px}

/* ---- header / dropdown nav ---- */
.site-header{position:sticky;top:0;z-index:100;background:rgba(253,248,242,.94);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--beige)}
.nav-inner{width:min(1240px,94%);margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.brand{display:flex;align-items:center;gap:12px}
.brand img{height:44px;width:auto;mix-blend-mode:multiply}
.brand .wtext{font-family:'Cormorant Garamond',serif;font-size:1.15rem;letter-spacing:1px;color:var(--navy);line-height:1.05}
.brand .wtext small{display:block;font-family:'Montserrat';font-size:.56rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--accent-deep);font-weight:600}
.main-nav>ul{list-style:none;display:flex;align-items:center;gap:4px}
.main-nav a{font-size:.82rem;letter-spacing:.4px;font-weight:400;padding:10px 14px;display:block;white-space:nowrap;color:var(--navy);transition:.2s}
.main-nav>ul>li>a:hover{color:var(--accent-deep)}
.main-nav li{position:relative}
.main-nav .has-drop>a::after{content:" \\25BE";font-size:.6em;opacity:.6}
.drop{list-style:none;position:absolute;top:100%;left:0;min-width:230px;background:#fff;border:1px solid var(--beige);
  border-radius:12px;box-shadow:0 16px 40px rgba(25,43,83,.14);padding:8px;opacity:0;visibility:hidden;transform:translateY(8px);transition:.2s}
.main-nav li:hover>.drop, .main-nav li:focus-within>.drop{opacity:1;visibility:visible;transform:translateY(0)}
.drop a{border-radius:8px;font-size:.8rem;padding:9px 12px}
.drop a:hover{background:var(--cream);color:var(--accent-deep)}
.nav-cta{background:var(--accent);color:var(--navy)!important;border-radius:999px;font-weight:600!important;
  letter-spacing:1px!important;text-transform:uppercase;font-size:.72rem!important;padding:11px 20px!important;margin-left:8px}
.nav-cta:hover{background:var(--accent-deep);color:#fff!important}
.nav-toggle{display:none;background:none;border:0;font-size:1.6rem;color:var(--navy);cursor:pointer}
.current>a{color:var(--accent-deep)!important;font-weight:600}

/* ---- sections ---- */
.hero{padding:clamp(70px,11vw,140px) 0;background:linear-gradient(160deg,var(--cream),var(--ivory))}
.hero.dark{background:linear-gradient(160deg,var(--navy),#0f1c38);color:var(--cream)}
.hero.dark h1,.hero.dark .say{color:var(--cream)}
.hero.dark .btn-ghost{color:var(--cream);border-color:var(--cream)}
.hero .lead{max-width:62ch}
.hero.dark .kicker{color:var(--gold)}
.sec{padding:clamp(56px,8vw,104px) 0}
.sec.cream{background:var(--cream)}
.sec.navy{background:var(--navy);color:var(--cream)}
.sec.navy h2,.sec.navy .say{color:var(--cream)}
.sec.forest{background:var(--forest);color:var(--ivory)}
.sec.forest h2{color:var(--ivory)}
.sec-head{text-align:center;max-width:60ch;margin:0 auto 46px}
.sec-head p{margin:0 auto}
.grid{display:grid;gap:26px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.card{background:#fff;border:1px solid var(--beige);border-radius:16px;padding:30px 26px}
.sec.navy .card,.sec.forest .card{background:rgba(255,255,255,.06);border-color:rgba(255,234,209,.18)}
.card h3{margin-bottom:10px;color:var(--accent-deep)}
.sec.navy .card h3,.sec.forest .card h3{color:var(--gold)}
.card p{font-size:.95rem;margin-bottom:0}
.card .price{font-family:'Cormorant Garamond';font-size:1.8rem;color:var(--navy);margin:6px 0}
.imgph{background:repeating-linear-gradient(135deg,rgba(233,203,167,.35),rgba(233,203,167,.35) 12px,rgba(255,234,209,.5) 12px,rgba(255,234,209,.5) 24px);
  border:1px dashed var(--olive-gold);border-radius:16px;min-height:280px;display:flex;align-items:center;justify-content:center;
  text-align:center;color:var(--burgundy);font-size:.78rem;letter-spacing:1px;padding:20px;font-style:italic}
.split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(40px,5vw,68px);align-items:stretch}
.split>*{min-width:0}
.split>div:not(.fig){align-self:center}
.split .fig{min-height:360px;height:100%}
.two{display:grid;grid-template-columns:1fr 1fr;gap:30px}
.trusted{text-align:center}
.trusted .label{font-size:.7rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--accent-deep);margin-bottom:38px}
.logo-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:38px 64px;max-width:960px;margin:0 auto}
.logo-row img{height:46px;max-height:46px;width:auto;max-width:150px;object-fit:contain;filter:grayscale(1);opacity:.55;transition:.3s}
.logo-row img:hover{filter:grayscale(0);opacity:1;transform:translateY(-2px)}
@media(max-width:640px){.logo-row{gap:28px 40px}.logo-row img{height:38px;max-height:38px;max-width:120px}}
.faq-item{border-bottom:1px solid var(--beige);padding:22px 0;max-width:820px;margin:0 auto}
.faq-item h3{color:var(--navy);margin-bottom:8px}
.faq-item p{margin-bottom:0;font-size:.98rem}
.cta-band{text-align:center}
.cta-band .say{margin:0 auto 22px;max-width:34ch}
.crosslink{background:var(--beige);text-align:center;padding:40px 0;font-size:.95rem}
.crosslink a{color:var(--burgundy);border-bottom:1px solid var(--accent-deep);font-weight:500}
ul.ticks{list-style:none;max-width:60ch}
ul.ticks li{padding:8px 0 8px 30px;position:relative}
ul.ticks li::before{content:"\\2713";position:absolute;left:0;color:var(--accent-deep);font-weight:700}
p.attrib{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;color:var(--olive-gold);margin-top:8px}
p.local-seo{max-width:70ch;margin:0 auto;text-align:center;font-size:.95rem;line-height:1.8;color:var(--olive-gold);letter-spacing:.3px}

/* ---- footer ---- */
.site-footer{background:var(--navy);color:var(--cream);padding:64px 0 30px}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px;margin-bottom:40px}
.site-footer h4{color:var(--gold);font-size:1.5rem;margin-bottom:14px}
.site-footer h5{font-family:'Montserrat';font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:14px;font-weight:600}
.site-footer a{color:rgba(255,234,209,.82)}
.site-footer a:hover{color:var(--gold)}
.site-footer ul{list-style:none}
.site-footer li{padding:5px 0;font-size:.88rem}
.foot-bottom{border-top:1px solid rgba(255,234,209,.16);padding-top:22px;display:flex;flex-wrap:wrap;
  justify-content:space-between;gap:10px;font-size:.74rem;color:rgba(255,234,209,.6)}
.foot-social{display:flex;gap:12px;margin-top:20px}
.foot-social a{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;
  border:1px solid rgba(255,234,209,.28);border-radius:50%;transition:.2s}
.foot-social a:hover{background:var(--gold);border-color:var(--gold)}
.foot-social svg{width:19px;height:19px;fill:rgba(255,234,209,.85)}
.foot-social a:hover svg{fill:var(--navy)}
.foot-legal{display:flex;gap:18px}
.foot-legal a{color:rgba(255,234,209,.6);text-decoration:underline;text-underline-offset:3px}
.legal-doc{max-width:760px;margin:0 auto}
.legal-doc h2{font-size:1.5rem;margin:34px 0 12px}
.legal-doc h3{font-family:'Montserrat';font-size:.95rem;font-weight:600;margin:22px 0 8px}
.legal-doc p,.legal-doc li{font-size:.95rem;line-height:1.75;margin-bottom:12px}
.legal-doc ul{padding-left:22px;margin-bottom:16px}
.legal-note{background:var(--cream);border-left:3px solid var(--gold);padding:18px 22px;margin-bottom:30px;font-size:.9rem}
.nd-form{max-width:620px;margin:0 auto;display:grid;gap:16px}
.nd-form label{font-family:'Montserrat';font-size:.74rem;letter-spacing:1.4px;text-transform:uppercase;
  font-weight:600;color:var(--navy);display:block;margin-bottom:6px}
.nd-form input,.nd-form select,.nd-form textarea{width:100%;padding:13px 15px;border:1px solid rgba(25,43,83,.22);
  border-radius:3px;font-family:'Montserrat';font-size:.95rem;background:#fff;color:var(--ink)}
.nd-form input:focus,.nd-form select:focus,.nd-form textarea:focus{outline:2px solid var(--gold);border-color:var(--gold)}
.nd-form textarea{min-height:130px;resize:vertical}
.nd-form .fine{font-size:.78rem;color:rgba(44,36,24,.66);line-height:1.6}
.nd-form .row-2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:600px){.nd-form .row-2{grid-template-columns:1fr}}

@media(max-width:900px){
  .nav-toggle{display:block}
  .main-nav{position:fixed;top:73px;right:0;width:min(320px,86%);height:calc(100vh - 73px);background:#fff;
    border-left:1px solid var(--beige);padding:16px;overflow-y:auto;transform:translateX(105%);transition:.3s;box-shadow:-10px 0 40px rgba(25,43,83,.12)}
  .main-nav.open{transform:translateX(0)}
  .main-nav>ul{flex-direction:column;align-items:stretch;gap:0}
  .main-nav>ul>li{border-bottom:1px solid var(--cream)}
  .drop{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:0;
    max-height:0;overflow:hidden;padding:0 0 0 14px;transition:.25s}
  .main-nav li.open>.drop{max-height:500px;padding:4px 0 10px 14px}
  .nav-cta{margin:12px 0 0;text-align:center}
  .split,.two{grid-template-columns:1fr}
  .foot-grid{grid-template-columns:1fr}
  .hero-split{grid-template-columns:1fr}
  .method-step{grid-template-columns:1fr;gap:6px}
  .feature-grid{grid-template-columns:1fr}
  .stats{gap:26px}
}

/* ================= RICH PALETTE ADDITIONS ================= */
:root{--olive:#3c3a22;--ink:#2c2418}
/* soft grain overlay for depth */
.grain{position:relative}
.grain::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.5;mix-blend-mode:soft-light;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.grain>*{position:relative;z-index:1}
/* refined kicker with leading rule */
.kicker{display:inline-flex;align-items:center;gap:12px;color:var(--olive-gold)}
.kicker::before{content:"";width:26px;height:1px;background:currentColor;display:inline-block}
.sec-head .kicker,.cta-band .kicker,.center .kicker{justify-content:center}
.hero .kicker{color:var(--olive-gold)}
.hero.dark .kicker,.sec.navy .kicker,.sec.forest .kicker,.sec.burgundy .kicker,.sec.olive .kicker{color:var(--gold)}
/* more section colours */
.sec.burgundy{background:radial-gradient(120% 90% at 50% 0%,rgba(244,162,97,.22),transparent 55%),var(--burgundy);color:var(--cream)}
.sec.burgundy h2,.sec.burgundy h3,.sec.burgundy .say{color:var(--cream)}
.sec.olive{background:linear-gradient(160deg,var(--forest),var(--olive) 92%);color:var(--cream)}
.sec.olive h2,.sec.olive h3{color:var(--ivory)}
.sec.beige{background:var(--beige)}
.hero.warm{background:linear-gradient(155deg,var(--beige),var(--gold) 60%,var(--orange))}
.hero.warm h1,.hero.warm .kicker,.hero.warm .lead{color:var(--burgundy)}
.hero.warm .kicker{color:var(--burgundy)}
/* gradient image panels (colour, not grey placeholders) */
.fig{position:relative;border-radius:14px;min-height:300px;display:flex;align-items:flex-end;justify-content:flex-start;
  text-align:left;color:rgba(253,248,242,.9);font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;
  padding:24px;box-shadow:0 22px 52px rgba(80,42,31,.16);overflow:hidden}
.fig::after{content:"";position:absolute;inset:14px;border:1px solid rgba(253,248,242,.4);border-radius:8px;pointer-events:none}
.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:inherit;z-index:0}
.fig.has-img{background:var(--beige)}
.hero-split .hfig .ph{border-radius:0}
.fig.gold{background:linear-gradient(150deg,var(--beige),var(--gold) 55%,var(--orange))}
.fig.forest{background:linear-gradient(150deg,var(--forest),var(--olive-gold))}
.fig.burgundy{background:linear-gradient(160deg,var(--burgundy),var(--orange) 78%,var(--gold))}
.fig.olive{background:linear-gradient(150deg,var(--olive-gold),var(--forest))}
.fig.navy{background:linear-gradient(150deg,var(--navy),var(--forest))}
.fig.beige{background:linear-gradient(150deg,var(--beige),var(--gold));color:var(--burgundy)}
/* pull quote band */
.pullquote{background:var(--beige);text-align:center;padding:clamp(56px,8vw,96px) 0}
.pullquote blockquote{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:clamp(1.8rem,3.6vw,2.6rem);
  font-weight:400;max-width:24ch;margin:0 auto;line-height:1.35;color:var(--burgundy)}
.pullquote cite{display:block;margin-top:20px;font-style:normal;font-size:.7rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--olive-gold)}
/* the method steps */
.method-steps{max-width:780px;margin:0 auto}
.method-step{display:grid;grid-template-columns:auto 1fr;gap:32px;padding:28px 0;border-top:1px solid rgba(255,234,209,.18);align-items:start}
.method-step:last-child{border-bottom:1px solid rgba(255,234,209,.18)}
.method-step .stage{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:2.4rem;color:var(--gold);line-height:1;min-width:54px}
.method-step .q{font-size:.68rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--olive-gold);margin-bottom:8px}
.method-step h3{font-size:1.7rem;color:var(--ivory);margin-bottom:4px}
.method-step p{color:rgba(255,234,209,.82);margin:0}
/* stats row */
.stats{display:flex;gap:44px;flex-wrap:wrap;margin-top:20px}
.stats div{font-family:'Cormorant Garamond',serif}
.stats b{display:block;font-size:2.4rem;color:var(--accent-deep);font-weight:500;line-height:1}
.stats span{font-size:.68rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--olive-gold);font-family:'Montserrat',sans-serif}
.sec.navy .stats b,.sec.forest .stats b,.hero.dark .stats b{color:var(--gold)}
.sec.navy .stats span,.sec.forest .stats span,.hero.dark .stats span{color:var(--gold)}
/* feature cards w/ highlighted middle */
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:12px;text-align:left}
.feature{border-radius:14px;padding:40px 32px;background:var(--cream);border:1px solid var(--beige);transition:transform .35s,box-shadow .35s;box-shadow:0 14px 34px rgba(80,42,31,.06)}
.feature:hover{transform:translateY(-8px);box-shadow:0 26px 54px rgba(80,42,31,.14)}
.feature .num{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;color:var(--olive-gold)}
.feature h3{font-size:1.7rem;margin:8px 0 12px;color:var(--navy)}
.feature p{font-size:.95rem;margin-bottom:16px}
.feature ul{list-style:none;margin-bottom:18px}
.feature li{font-size:.85rem;letter-spacing:.4px;color:var(--burgundy);padding:6px 0;border-bottom:1px solid rgba(169,153,62,.2)}
.feature .more{font-size:.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent-deep);font-weight:600}
.feature.hl{background:var(--forest);border-color:var(--forest)}
.feature.hl h3{color:var(--ivory)}.feature.hl .num{color:var(--gold)}
.feature.hl p{color:rgba(255,234,209,.9)}.feature.hl li{color:rgba(255,234,209,.85);border-color:rgba(255,234,209,.18)}
.feature.hl .more{color:var(--gold)}
/* testimonial cards */
.quote-card{background:var(--ivory);border-radius:14px;padding:34px 32px;border:1px solid rgba(169,153,62,.25);box-shadow:0 16px 40px rgba(80,42,31,.08)}
.quote-card .stars{color:var(--gold);margin-bottom:12px;letter-spacing:3px}
.quote-card p{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.2rem;line-height:1.5;color:var(--navy);margin-bottom:14px}
.quote-card cite{font-style:normal;font-size:.66rem;letter-spacing:2px;text-transform:uppercase;color:var(--burgundy)}
/* trust strip (credibility above the fold) */
.trust{background:var(--beige);border-top:1px solid rgba(169,153,62,.25);border-bottom:1px solid rgba(169,153,62,.25)}
.trust .wrap{display:flex;align-items:center;justify-content:center;gap:clamp(22px,4vw,60px);flex-wrap:wrap;padding:20px 0;text-align:center}
.trust .ti{display:flex;flex-direction:column;gap:5px;align-items:center;max-width:420px}
.trust .stars{color:var(--gold);letter-spacing:3px;font-size:1rem}
.trust .rate{font-family:'Cormorant Garamond',serif;font-size:1.05rem;color:var(--navy)}
.trust .rate b{font-weight:600}
.trust .tq{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.12rem;line-height:1.45;color:var(--navy)}
.trust cite{font-style:normal;font-size:.62rem;letter-spacing:2px;text-transform:uppercase;color:var(--burgundy)}
.trust .tmark{font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;color:var(--olive-gold);font-family:'Montserrat',sans-serif;line-height:1.5}
/* lead-magnet opt-in */
.optin form{display:flex;gap:10px;flex-wrap:wrap;max-width:520px;margin:20px auto 0;justify-content:center}
.optin input[type=email]{flex:1;min-width:230px;padding:14px 20px;border-radius:40px;border:1px solid var(--olive-gold);background:var(--ivory);font-family:'Montserrat',sans-serif;font-size:.9rem;color:var(--navy)}
.optin input[type=email]:focus{outline:none;border-color:var(--gold)}
.optin .fine{font-size:.72rem;color:rgba(253,248,242,.7);margin-top:12px;text-align:center}
/* hero split with figure */
.hero:has(.hero-split){padding-top:clamp(24px,4vw,54px);padding-bottom:clamp(24px,4vw,54px)}
.hero-split{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(32px,5vw,64px);align-items:stretch;min-height:52vh}
.hero-split .hcopy{padding:clamp(24px,3.5vw,52px) 0;display:flex;flex-direction:column;justify-content:center}
.hero-split .hfig{position:relative;overflow:hidden;min-height:340px}
.hero-split .hfig .note{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;
  color:rgba(80,42,31,.55);font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;padding:0 14%}
.hero-split .hfig::after{content:"";position:absolute;inset:16px;border:1px solid rgba(253,248,242,.5)}
.hero-cred{margin-top:26px;font-size:.66rem;letter-spacing:2.5px;text-transform:uppercase;color:var(--olive-gold);border-top:1px solid var(--beige);padding-top:18px}
@media(max-width:900px){.hero-split .hcopy{padding:44px 0}.hero-split .hfig{order:-1}}
.hero-split .hcopy h1 em,.hero h1 em{font-style:italic;color:var(--orange);font-weight:400}
.hcopy h1{font-family:'Cormorant Garamond',serif;font-size:clamp(2.6rem,5.4vw,4.1rem);line-height:1.02;color:var(--navy);font-weight:600;letter-spacing:-.5px}
.hcopy>p{font-size:1.08rem;color:var(--ink);max-width:44ch;margin-top:20px;line-height:1.7}
.hcopy .btn-row{margin-top:30px}
/* ---- Start Here: ecosystem doorways ---- */
.doorways{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:8px}
.door{display:flex;flex-direction:column;background:#fff;border:1px solid var(--beige);border-radius:16px;
  padding:34px 32px;transition:transform .35s,box-shadow .35s,border-color .35s;box-shadow:0 14px 34px rgba(80,42,31,.05)}
.door:hover{transform:translateY(-6px);box-shadow:0 26px 54px rgba(80,42,31,.13);border-color:var(--gold)}
.door .intent{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.5rem;color:var(--olive-gold);line-height:1.2;margin-bottom:8px}
.door h3{font-size:1.55rem;color:var(--navy);margin-bottom:10px}
.door p{font-size:.95rem;margin-bottom:20px}
.door .go{margin-top:auto;font-size:.72rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent-deep);font-weight:600}
.door:hover .go{color:var(--orange)}
@media(max-width:760px){.doorways{grid-template-columns:1fr}}

/* ---- manifesto (short-line belief block) ---- */
.manifesto{max-width:720px;margin:0 auto;text-align:center}
.manifesto p{font-family:'Cormorant Garamond',serif;font-size:clamp(1.35rem,2.7vw,1.95rem);line-height:1.45;color:var(--navy);margin-bottom:20px}
.manifesto p.list{font-size:clamp(1.1rem,2vw,1.4rem);color:var(--burgundy);line-height:1.7}
.manifesto p.small{font-family:'Montserrat',sans-serif;font-size:1.05rem;line-height:1.8;color:var(--ink);max-width:56ch;margin:0 auto 20px}
.manifesto em{font-style:italic;color:var(--olive-gold)}
.sec.navy .manifesto p,.sec.burgundy .manifesto p{color:var(--cream)}
.sec.navy .manifesto p.small,.sec.burgundy .manifesto p.small{color:rgba(253,248,242,.85)}
.sec.navy .manifesto em,.sec.burgundy .manifesto em{color:var(--gold)}

/* ---- creed (We believe...) ---- */
.creed{max-width:780px;margin:0 auto}
.creed .cline{padding:28px 0;border-bottom:1px solid var(--beige)}
.creed .cline:last-child{border-bottom:0}
.creed .cbelief{font-family:'Cormorant Garamond',serif;font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.25;color:var(--navy)}
.creed .cbelief em{font-style:italic;color:var(--olive-gold)}
.creed .csub{margin-top:10px;font-size:1rem;line-height:1.75;color:var(--ink);max-width:62ch}

/* ---- long-form story ---- */
.story{max-width:720px;margin:0 auto}
.story .chapter{margin-bottom:50px}
.story .chapter:last-child{margin-bottom:0}
.story .cnum{font-family:'Montserrat',sans-serif;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;color:var(--olive-gold);font-weight:600;margin-bottom:10px}
.story h3{font-size:clamp(1.55rem,3vw,2.1rem);color:var(--navy);margin-bottom:16px;line-height:1.2}
.story p{font-size:1.06rem;line-height:1.85;color:var(--ink);margin-bottom:18px}
.story p:last-child{margin-bottom:0}
.story p.lead{font-size:1.22rem;line-height:1.7;color:var(--navy)}
"""

NAV_JS = """
<script>
document.querySelector('.nav-toggle').addEventListener('click',function(){
  document.querySelector('.main-nav').classList.toggle('open');
});
document.querySelectorAll('.main-nav .has-drop>a').forEach(function(a){
  a.addEventListener('click',function(e){
    if(window.innerWidth<=900){e.preventDefault();a.parentElement.classList.toggle('open');}
  });
});
</script>
"""

def esc(s): return html.escape(s, quote=True)

def build_nav(nav, current, brand_name, brand_sub):
    items=[]
    for entry in nav:
        if entry[0]=='link':
            _,label,href=entry
            cur=' class="current"' if href==current else ''
            items.append('<li%s><a href="%s">%s</a></li>'%(cur,href,label))
        elif entry[0]=='drop':
            _,label,subs=entry
            cur=any(h==current for _,h in subs)
            sub_html=''.join('<li><a href="%s">%s</a></li>'%(h,l) for l,h in subs)
            items.append('<li class="has-drop%s"><a href="#">%s</a><ul class="drop">%s</ul></li>'%(' current' if cur else '',label,sub_html))
        elif entry[0]=='cta':
            _,label,href=entry
            items.append('<li><a class="nav-cta" href="%s">%s</a></li>'%(href,label))
    return ('<header class="site-header"><div class="nav-inner">'
      '<a class="brand" href="index.html"><img src="%s" alt="%s logo">'
      '<span class="wtext">%s<small>%s</small></span></a>'
      '<button class="nav-toggle" aria-label="Open menu">&#9776;</button>'
      '<nav class="main-nav"><ul>%s</ul></nav></div></header>'
      )%(LOGO,esc(brand_name),brand_name,brand_sub,''.join(items))

def page(site, slug, title, desc, body, footer):
    canon="https://%s/%s"%(site['domain'], '' if slug=='index.html' else slug)
    ogimg="https://%s/og-image.jpg"%site['domain']
    doc=('<!DOCTYPE html><html lang="en-AU"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>%s</title><meta name="description" content="%s">'
      '<link rel="canonical" href="%s">'
      '<meta name="theme-color" content="#192b53">'
      '<link rel="icon" href="%s"><link rel="apple-touch-icon" href="%s">'
      '<meta property="og:site_name" content="%s">'
      '<meta property="og:title" content="%s"><meta property="og:description" content="%s">'
      '<meta property="og:url" content="%s"><meta property="og:image" content="%s">'
      '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
      '<meta property="og:locale" content="en_AU">'
      '<meta property="og:type" content="website"><meta name="robots" content="index,follow">'
      '<meta name="twitter:card" content="summary_large_image">'
      '<meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s">'
      '<meta name="twitter:image" content="%s">'
      '<link rel="stylesheet" href="assets/style.css">'
      '%s'            # JSON-LD structured data
      '%s'            # analytics slot
      '</head><body>'
      '%s<main>%s</main>%s%s</body></html>'
      )%(esc(title),esc(desc),canon,LOGO,LOGO,esc(site['brand']),
         esc(title),esc(desc),canon,ogimg,
         esc(title),esc(desc),ogimg,
         site.get('schema',''),ANALYTICS_SLOT,
         build_nav(site['nav'],slug,site['brand'],site['sub']),body,footer,NAV_JS)
    with open(os.path.join(site['dir'],slug),'w',encoding='utf-8') as f:
        f.write(doc)

# ---------------------------------------------------------------- analytics
# TODO before go-live: paste the GA4 Measurement ID and Meta Pixel ID below.
# Replace G-XXXXXXXXXX and PIXEL_ID_HERE, then uncomment each block.
ANALYTICS_SLOT = (
  '<!-- ANALYTICS: Google Analytics 4 -- paste Measurement ID and uncomment\n'
  '<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>\n'
  '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\n'
  'gtag(\'js\',new Date());gtag(\'config\',\'G-XXXXXXXXXX\');</script>\n'
  '-->\n'
  '<!-- ANALYTICS: Meta Pixel -- paste Pixel ID and uncomment\n'
  '<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?\n'
  'n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;\n'
  'n.push=n;n.loaded=!0;n.version=\'2.0\';n.queue=[];t=b.createElement(e);t.async=!0;\n'
  't.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,\n'
  '\'script\',\'https://connect.facebook.net/en_US/fbevents.js\');\n'
  'fbq(\'init\',\'PIXEL_ID_HERE\');fbq(\'track\',\'PageView\');</script>\n'
  '-->'
)

# ---------------------------------------------------------------- helpers
def hero(kicker,h1,sub,ctas,dark=False):
    btns=''.join('<a class="btn %s" href="%s">%s</a>'%(c[2],c[1],c[0]) for c in ctas)
    return ('<section class="hero%s"><div class="wrap"><div class="kicker">%s</div>'
      '<h1>%s</h1><p class="lead" style="margin-top:18px;font-size:1.15rem">%s</p>'
      '<div class="btn-row">%s</div></div></section>')%(' dark' if dark else '',kicker,h1,sub,btns)

def sec(inner,cls=''):
    return '<section class="sec %s"><div class="wrap">%s</div></section>'%(cls,inner)

def head(kicker,h2,sub=''):
    k='<div class="kicker">%s</div>'%kicker if kicker else ''
    s='<p>%s</p>'%sub if sub else ''
    return '<div class="sec-head">%s<h2>%s</h2>%s</div>'%(k,h2,s)

def cards(items):
    c=''.join('<div class="card">%s<h3>%s</h3><p>%s</p></div>'%(
        ('<div class="price">%s</div>'%it[2]) if len(it)>2 and it[2] else '',it[0],it[1]) for it in items)
    return '<div class="grid">%s</div>'%c

def imgph(t,tone='gold'): return '<div class="fig %s">%s</div>'%(tone,t)

def hero_split(kicker,h1,sub,ctas,fig_note,fig_tone='gold',cred='',stats=None,photo=None,pos=None):
    btns=''.join('<a class="btn %s" href="%s">%s</a>'%(c[2],c[1],c[0]) for c in ctas)
    st=''
    if stats:
        st='<div class="stats">'+''.join('<div><b>%s</b><span>%s</span></div>'%(b,s) for b,s in stats)+'</div>'
    credhtml='<div class="hero-cred">%s</div>'%cred if cred else ''
    figinner=img(photo,fig_note,pos) if photo else '<div class="note">%s</div>'%fig_note
    figcls=fig_tone+(' has-img' if photo else '')
    return ('<section class="hero"><div class="wrap"><div class="hero-split">'
      '<div class="hcopy"><div class="kicker">%s</div><h1>%s</h1>'
      '<p class="lead" style="margin-top:16px;font-size:1.15rem">%s</p>'
      '<div class="btn-row">%s</div>%s%s</div>'
      '<div class="hfig fig %s">%s</div>'
      '</div></div></section>')%(kicker,h1,sub,btns,st,credhtml,figcls,figinner)

def pullquote(q,cite='&mdash; Dawn Edwards-Jones'):
    return '<section class="pullquote"><div class="wrap"><blockquote>%s</blockquote><cite>%s</cite></div></section>'%(q,cite)

def method_steps(intro_kicker,intro_h2,intro_p,steps,close_say=None,close_cta=None,cls='olive'):
    body='<div class="sec-head">%s<h2>%s</h2>%s</div>'%(
        '<div class="kicker">%s</div>'%intro_kicker if intro_kicker else '',intro_h2,
        '<p>%s</p>'%intro_p if intro_p else '')
    rows=''
    for i,(q,title,text) in enumerate(steps,1):
        rows+=('<div class="method-step"><div class="stage">%02d</div>'
          '<div><div class="q">%s</div><h3>%s</h3><p>%s</p></div></div>')%(i,q,title,text)
    body+='<div class="method-steps">%s</div>'%rows
    if close_say:
        btn='<div class="btn-row" style="justify-content:center;margin-top:22px"><a class="btn btn-gold" href="%s">%s</a></div>'%(close_cta[1],close_cta[0]) if close_cta else ''
        body+='<div style="text-align:center;margin-top:46px"><p class="say" style="color:var(--gold);max-width:34ch;margin:0 auto">%s</p>%s</div>'%(close_say,btn)
    return '<section class="sec %s grain"><div class="wrap">%s</div></section>'%(cls,body)

def stats_row(items):
    return '<div class="stats">'+''.join('<div><b>%s</b><span>%s</span></div>'%(b,s) for b,s in items)+'</div>'

def feature_cards(items,highlight=1):
    c=''
    for i,it in enumerate(items):
        num,title,text,lis,more=it
        hl=' hl' if i==highlight else ''
        li=''.join('<li>%s</li>'%x for x in lis)
        m=('<a class="more" href="%s">%s &rarr;</a>'%(more[1],more[0])) if more else ''
        c+=('<div class="feature%s"><div class="num">%s</div><h3>%s</h3><p>%s</p>'
            '<ul>%s</ul>%s</div>')%(hl,num,title,text,li,m)
    return '<div class="feature-grid">%s</div>'%c

def quotes(items):
    c=''.join('<div class="quote-card"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>%s</p><cite>%s</cite></div>'%(p,who) for p,who in items)
    return '<section class="sec beige"><div class="wrap"><div class="sec-head"><div class="kicker">In their words</div><h2>Women who came home.</h2></div><div class="grid">%s</div></div></section>'%c

def cta_band(say,ctas,cls='cream'):
    btns=''.join('<a class="btn %s" href="%s">%s</a>'%(c[2],c[1],c[0]) for c in ctas)
    return ('<section class="sec %s cta-band"><div class="wrap"><p class="say">%s</p>'
      '<div class="btn-row" style="justify-content:center">%s</div></div></section>')%(cls,say,btns)

def faqs(items):
    f=''.join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>'%(q,a) for q,a in items)
    return '<section class="sec"><div class="wrap"><div class="sec-head"><div class="kicker">Questions</div><h2>Good to know</h2></div>%s</div></section>'%f

def crosslink(text,href,label):
    return '<section class="crosslink"><div class="wrap">%s <a href="%s">%s</a></div></section>'%(text,href,label)

def trust_strip(rating_html, quote, cite, mark):
    return ('<section class="trust"><div class="wrap">'
      '<div class="ti"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
      '<div class="rate">%s</div></div>'
      '<div class="ti"><p class="tq">&ldquo;%s&rdquo;</p><cite>%s</cite></div>'
      '<div class="ti"><div class="tmark">%s</div></div>'
      '</div></section>')%(rating_html,quote,cite,mark)

def optin(kicker,h2,text,button,fine,cls='forest'):
    return ('<section class="sec %s optin"><div class="wrap"><div class="sec-head">'
      '<div class="kicker">%s</div><h2>%s</h2>'
      '<p style="max-width:640px;margin:0 auto">%s</p></div>'
      '<form onsubmit="return false">'
      '<input type="email" placeholder="Your email address" aria-label="Email address">'
      '<button class="btn btn-gold" type="submit">%s</button></form>'
      '<p class="fine">%s</p></div></section>')%(cls,kicker,h2,text,button,fine)

def cards_link(items):
    c=''
    for it in items:
        title,text,href,label=it
        c+=('<div class="card"><h3>%s</h3><p style="margin-bottom:16px">%s</p>'
            '<a class="btn btn-ghost" style="padding:9px 20px;font-size:.7rem" href="%s">%s</a></div>')%(title,text,href,label)
    return '<div class="grid">%s</div>'%c

def doorways(items):
    c=''
    for intent,name,text,href,label in items:
        c+=('<a class="door" href="%s"><div class="intent">%s</div><h3>%s</h3>'
            '<p>%s</p><span class="go">%s &rarr;</span></a>')%(href,intent,name,text,label)
    return '<div class="doorways">%s</div>'%c

def manifesto(lines):
    # lines: list of (text, cls) where cls in '', 'list', 'small'
    c=''
    for text,cls in lines:
        klass=(' class="%s"'%cls) if cls else ''
        c+='<p%s>%s</p>'%(klass,text)
    return '<div class="manifesto">%s</div>'%c

def creed(items):
    # items: list of (belief_html, sub_html)
    c=''
    for belief,sub in items:
        s='<div class="csub">%s</div>'%sub if sub else ''
        c+='<div class="cline"><div class="cbelief">%s</div>%s</div>'%(belief,s)
    return '<div class="creed">%s</div>'%c

def story(chapters):
    # chapters: list of (num_label, heading, body_html)
    c=''
    for num,h,body in chapters:
        c+='<div class="chapter"><div class="cnum">%s</div><h3>%s</h3>%s</div>'%(num,h,body)
    return '<div class="story">%s</div>'%c

DEJ_URL="https://dawnedwards-jones.com"
NDW_URL="https://newdawnwellness.health"

SOC_ICON={
 'Instagram':'<path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.06 1.8.25 2.2.42.6.23 1 .5 1.4 1 .5.4.8.8 1 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-1 1.4-.4.5-.8.8-1.4 1-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-1-.5-.4-.8-.8-1-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 1-1.4.4-.5.8-.8 1.4-1 .4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.8.07-.9 0-1.4.2-1.7.3-.4.2-.7.3-1 .6-.3.3-.5.6-.6 1-.1.3-.3.8-.3 1.7C3.5 8.9 3.5 9.3 3.5 12s0 3.1.1 4.4c0 .9.2 1.4.3 1.7.1.4.3.7.6 1 .3.3.6.5 1 .6.3.1.8.3 1.7.3 1.3.1 1.7.1 4.8.1s3.5 0 4.8-.1c.9 0 1.4-.2 1.7-.3.4-.1.7-.3 1-.6.3-.3.5-.6.6-1 .1-.3.3-.8.3-1.7.1-1.3.1-1.7.1-4.4s0-3.1-.1-4.4c0-.9-.2-1.4-.3-1.7-.1-.4-.3-.7-.6-1-.3-.3-.6-.4-1-.6-.3-.1-.8-.3-1.7-.3-1.3-.07-1.7-.07-4.8-.07zm0 3.1a4.9 4.9 0 110 9.8 4.9 4.9 0 010-9.8zm0 8.1a3.2 3.2 0 100-6.4 3.2 3.2 0 000 6.4zm6.2-8.3a1.15 1.15 0 11-2.3 0 1.15 1.15 0 012.3 0z"/>',
 'Facebook':'<path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.5 1.49-3.89 3.77-3.89 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.78-1.63 1.57v1.87h2.78l-.45 2.91h-2.33V22c4.78-.79 8.44-4.94 8.44-9.94z"/>',
 'Google':'<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 1.8c1.5 0 2.9.45 4.06 1.22l-1.3 1.3A5.9 5.9 0 0012 5.4a6.6 6.6 0 100 13.2 6.3 6.3 0 006.2-5h-6.2v-1.9h8.1c.06.4.1.8.1 1.2A8.2 8.2 0 1112 3.8z"/>',
 'Spotify':'<path d="M12 2a10 10 0 100 20 10 10 0 000-20zm4.6 14.4a.78.78 0 01-1.07.26c-2.93-1.79-6.62-2.2-10.97-1.2a.78.78 0 11-.35-1.52c4.76-1.09 8.84-.62 12.13 1.39.37.23.49.7.26 1.07zm1.23-2.74a.97.97 0 01-1.34.32c-3.36-2.06-8.48-2.66-12.45-1.46a.97.97 0 11-.56-1.86c4.54-1.38 10.18-.71 14.04 1.66.46.28.6.88.31 1.34zm.1-2.85C14.1 8.42 7.6 8.2 4.1 9.27a1.17 1.17 0 11-.68-2.24c4.02-1.22 11.2-.98 15.4 1.52a1.17 1.17 0 01-1.19 2.01z"/>',
}
def social_row(items):
    if not items: return ''
    a=''
    for label,href in items:
        ic=SOC_ICON.get(label,'')
        a+=('<a href="%s" aria-label="%s" rel="me noopener" target="_blank">'
            '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg></a>')%(href,esc(label),ic)
    return '<div class="foot-social">%s</div>'%a

def footer(site):
    cols=''
    for heading,links in site['footer_cols']:
        li=''.join('<li><a href="%s">%s</a></li>'%(h,l) for l,h in links)
        cols+='<div><h5>%s</h5><ul>%s</ul></div>'%(heading,li)
    legal=('<span class="foot-legal"><a href="privacy.html">Privacy Policy</a>'
           '<a href="terms.html">Terms</a></span>')
    return ('<footer class="site-footer"><div class="wrap"><div class="foot-grid">'
      '<div><h4>%s</h4><p style="font-size:.9rem;color:rgba(255,234,209,.8);max-width:40ch">%s</p>'
      '<p style="font-size:.82rem;margin-top:14px;color:rgba(255,234,209,.7)">%s</p>%s</div>%s</div>'
      '<div class="foot-bottom"><span>&copy; 2026 %s</span>%s<span>%s</span></div></div></footer>'
      )%(site['brand'],site['foot_blurb'],site['foot_contact'],social_row(site.get('social')),
         cols,site['brand'],legal,site['foot_tag'])

# ================================================================ WELLNESS
ndw={'domain':'newdawnwellness.health','dir':os.path.join(SITES_DIR,'new-dawn-wellness'),
  'brand':'New Dawn Wellness','sub':'Cleveland, QLD'}
ndw['nav']=[
  ('link','Home','index.html'),
  ('drop','About',[('Our Story','our-story.html'),('Meet Dawn','meet-dawn.html'),('Our Space','our-space.html')]),
  ('drop','Move',[('Pilates &amp; Yoga','pilates-yoga.html'),('Class Timetable','timetable.html'),('Membership &amp; Class Options','membership.html'),('Our Instructors','instructors.html'),('The 6-Week Reset','6-week-reset.html')]),
  ('drop','Heal',[('Flow &amp; Glow Lymphatic Massage','flow-and-glow-massage.html'),('Soul Restore Reiki','soul-restore-reiki.html'),('The Adawning Experience &mdash; Hypnotherapy','adawning-experience.html')]),
  ('drop','Events &amp; Retreats',[('Wellness Events','wellness-events.html'),('Retreats','retreats.html')]),
  ('drop','Coaching',[('Soul Mastery Sanctuary &mdash; Group','soul-mastery-sanctuary.html'),('Soul Mastery Ascension &mdash; 1:1',DEJ_URL+'/soul-mastery-ascension.html'),('Nutrition Support','nutrition.html'),('Menopause Support','menopause-support.html')]),
  ('drop','Resources',[('The Adawning Podcast','podcast.html'),('Articles','articles.html'),('Free Resources','free-resources.html')]),
  ('link','Work with Dawn',DEJ_URL),
  ('link','Contact','contact.html'),
  ('cta','Book a Class','timetable.html'),
]
PLACE_ID   = "ChIJa5XOgsVmkWsRdwoK4EV4S0c"      # Google Business Profile place ID (from Tekmatix)
GMAPS_URL  = "https://www.google.com/maps/place/?q=place_id:"+PLACE_ID
GREVIEW_URL= "https://search.google.com/local/writereview?placeid="+PLACE_ID
IG_URL     = "https://www.instagram.com/newdawnpilates/"
FB_URL     = "https://www.facebook.com/newdawnpilates"
# TODO before go-live: confirm Dawn's public LinkedIn vanity URL and the Spotify show URL.
LI_URL     = ""
ndw['social']=[('Instagram',IG_URL),('Facebook',FB_URL),('Google',GMAPS_URL)]
dej_social =[('Facebook',FB_URL),('Instagram',IG_URL)]

# ---- structured data (local SEO + AI search visibility)
import json as _json
_NDW_SCHEMA={
  "@context":"https://schema.org","@type":["HealthAndBeautyBusiness","SportsActivityLocation"],
  "@id":NDW_URL+"/#business","name":"New Dawn Wellness",
  "alternateName":"New Dawn Pilates & Yoga",
  "description":"Pilates, yoga, lymphatic massage, reiki, breathwork, hypnosis and coaching for women in Cleveland, QLD.",
  "url":NDW_URL,"logo":LOGO,"image":NDW_URL+"/og-image.jpg",
  "telephone":PHONE,"email":EMAIL,"priceRange":"$$",
  "currenciesAccepted":"AUD","paymentAccepted":"Cash, Credit Card, EFTPOS",
  "address":{"@type":"PostalAddress","streetAddress":"4 Cross Street","addressLocality":"Cleveland",
    "addressRegion":"QLD","postalCode":"4163","addressCountry":"AU"},
  "geo":{"@type":"GeoCoordinates","latitude":-27.5261,"longitude":153.2654},
  "hasMap":GMAPS_URL,
  "areaServed":[{"@type":"City","name":n} for n in
    ["Cleveland","Ormiston","Raby Bay","Thornlands","Alexandra Hills","Wellington Point","Victoria Point","Redland City"]],
  "sameAs":[u for u in [IG_URL,FB_URL,DEJ_URL,GMAPS_URL] if u],
  "founder":{"@type":"Person","name":"Dawn Edwards-Jones","url":DEJ_URL},
  # TODO before go-live: confirm these opening hours against the live timetable.
  "openingHoursSpecification":[
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],
     "opens":"06:00","closes":"19:00"},
    {"@type":"OpeningHoursSpecification","dayOfWeek":["Saturday"],"opens":"07:00","closes":"12:00"}],
  "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n}} for n in
    ["Mat Pilates classes","Yin, restorative and slow flow yoga","Flow & Glow lymphatic massage",
     "Soul Restore Reiki","The Adawning Experience hypnosis session","Breathwork and sound healing",
     "The 6-Week Reset program","Soul Mastery Sanctuary group coaching","Menopause support",
     "Nutrition support","Wellness events and retreats"]],
}
_DEJ_SCHEMA={
  "@context":"https://schema.org","@type":"Person","@id":DEJ_URL+"/#person",
  "name":"Dawn Edwards-Jones","url":DEJ_URL,"image":DEJ_URL+"/og-image.jpg",
  "jobTitle":"Keynote Speaker, Author and Self-Leadership Coach",
  "description":"Keynote speaker, author and self-leadership coach helping women and organisations move from overwhelm to calm, embodied leadership.",
  "email":EMAIL,"telephone":PHONE,
  "address":{"@type":"PostalAddress","addressLocality":"Cleveland","addressRegion":"QLD","addressCountry":"AU"},
  "worksFor":{"@type":"Organization","name":"New Dawn Wellness","url":NDW_URL},
  "sameAs":[u for u in [FB_URL,IG_URL,NDW_URL,LI_URL] if u],
  "knowsAbout":["Nervous system regulation","Menopause in the workplace","Self-leadership",
    "Burnout prevention","Breathwork","Hypnosis","Embodiment coaching"],
}
def _ld(d): return '<script type="application/ld+json">%s</script>'%_json.dumps(d,separators=(',',':'))
ndw['schema']=_ld(_NDW_SCHEMA)   # dej['schema'] is assigned below, once dej exists

ndw['foot_blurb']="A Pilates, yoga and whole-wellness studio in Cleveland, QLD. Helping women come home to themselves through movement, breath, healing and support."
ndw['foot_contact']="%s &middot; %s<br>%s"%(ADDRESS,PHONE,EMAIL)
ndw['foot_tag']="New Dawn Wellness &middot; Cleveland QLD"
ndw['footer_cols']=[
  ('Move & Heal',[('Pilates & Yoga','pilates-yoga.html'),('Timetable','timetable.html'),('Membership & Class Options','membership.html'),('Flow & Glow Lymphatic Massage','flow-and-glow-massage.html'),('Soul Restore Reiki','soul-restore-reiki.html'),('The Adawning Experience','adawning-experience.html')]),
  ('Support',[('6-Week Reset','6-week-reset.html'),('Retreats','retreats.html'),('Wellness Events','wellness-events.html'),('Soul Mastery Sanctuary','soul-mastery-sanctuary.html'),('Soul Mastery Ascension &mdash; 1:1',DEJ_URL+'/soul-mastery-ascension.html'),('Nutrition Support','nutrition.html'),('Menopause Support','menopause-support.html')]),
  ('Resources',[('The Adawning Podcast','podcast.html'),('Articles','articles.html'),('Free Resources','free-resources.html'),('FAQ','faq.html')]),
  ('More',[('Our Story','our-story.html'),('Meet Dawn','meet-dawn.html'),('Our Space','our-space.html'),('Our Instructors','instructors.html'),('Contact','contact.html'),('Work with Dawn &rarr;',DEJ_URL)]),
]

# ================================================================ DEJ
dej={'domain':'dawnedwards-jones.com','dir':os.path.join(SITES_DIR,'dawn-edwards-jones'),
  'brand':'Dawn Edwards-Jones','sub':'Author &middot; Speaker &middot; Coach'}
dej['nav']=[
  ('link','Home','index.html'),
  ('link','Start Here','start-here.html'),
  ('link','About','about.html'),
  ('link','Philosophy','philosophy.html'),
  ('drop','Work With Me',[('Soul Mastery Sanctuary &mdash; Group (online)',NDW_URL+'/soul-mastery-sanctuary.html'),('Soul Mastery Ascension &mdash; 1:1','soul-mastery-ascension.html'),('Calm to Chaos &mdash; Business Coaching','calm-to-chaos.html')]),
  ('drop','Speaking',[('Keynote Speaking','speaking.html'),('Corporate Workshops','corporate-workshops.html'),('Menopause Policy Advisory','menopause-policy.html')]),
  ('drop','Publications',[('The Adawning Podcast','podcast.html'),('The Book','book.html')]),
  ('drop','New Dawn Wellness',[('The Studio',NDW_URL),('Pilates &amp; Yoga',NDW_URL+'/pilates-yoga.html'),('Retreats',NDW_URL+'/retreats.html'),('Wellness Events',NDW_URL+'/wellness-events.html'),('Massage &amp; Healing',NDW_URL+'/flow-and-glow-massage.html'),('The Adawning Experience',NDW_URL+'/adawning-experience.html')]),
  ('cta','Enquire','contact.html'),
]
dej['foot_blurb']="Author, keynote speaker and self-leadership coach helping women &mdash; and the organisations they work in &mdash; move from overwhelm to calm, embodied leadership."
dej['foot_contact']=EMAIL
dej['foot_tag']="Dawn Edwards-Jones &middot; Founder of The Adawning"
dej['footer_cols']=[
  ('Work With Dawn',[('Soul Mastery Sanctuary &mdash; Group',NDW_URL+'/soul-mastery-sanctuary.html'),('Soul Mastery Ascension &mdash; 1:1','soul-mastery-ascension.html'),('Calm to Chaos','calm-to-chaos.html'),('Contact','contact.html')]),
  ('Speaking',[('Keynote Speaking','speaking.html'),('Corporate Workshops','corporate-workshops.html'),('Menopause Policy Advisory','menopause-policy.html')]),
  ('Explore',[('About Dawn','about.html'),('The Adawning Podcast','podcast.html'),('The Book','book.html'),('New Dawn Wellness Studio &rarr;',NDW_URL)]),
]
dej['social']=dej_social
dej['schema']=_ld(_DEJ_SCHEMA)

# ================================================================ LEGAL PAGES
# Drafted to cover Australian Privacy Act / APP obligations. NOT legal advice:
# Dawn should have these reviewed before go-live. See the go-live gap list.
LEGAL_UPDATED = "1 October 2026"

def privacy_body(brand, domain, is_studio):
    studio_bits = ''
    if is_studio:
        studio_bits = (
          '<h3>Health and wellbeing information</h3>'
          '<p>If you book a class, a massage, a reiki session, a hypnosis session or a program with us, '
          'we may ask about injuries, medical conditions, pregnancy, medications or how you are feeling. '
          'Under Australian privacy law this is <strong>sensitive information</strong>, and we treat it that way. '
          'We collect it only so we can keep you safe and adapt what we do for your body. We only collect it '
          'with your consent, we do not use it for marketing, and we do not share it with anyone outside '
          'New Dawn Wellness unless you ask us to or we are required to by law.</p>'
          '<h3>Our premises</h3>'
          '<p>Classes are held at '+ADDRESS+'. Private sessions are held at a separate private studio and the '
          'address is given to you when you book.</p>')
    return (hero('Legal','Privacy Policy.',
        'How we collect, use and look after your personal information. Written in plain English, because you '
        'should be able to understand it without a lawyer.',
        [('Contact us','contact.html','btn-ghost')])
      + sec('<div class="legal-doc">'
        + '<div class="legal-note"><strong>Draft for review.</strong> This policy has been prepared for '
          + brand + ' and is awaiting final review. Last updated ' + LEGAL_UPDATED + '.</div>'
        + '<h2>Who we are</h2>'
        + '<p>' + brand + ' (&ldquo;we&rdquo;, &ldquo;us&rdquo;) operates ' + domain + '. We are based in '
          'Cleveland, Queensland, Australia. You can reach us at <a href="mailto:' + EMAIL + '">' + EMAIL
          + '</a> or on ' + PHONE + '.</p>'
        + '<p>We handle personal information in line with the Australian Privacy Principles in the '
          '<em>Privacy Act 1988</em> (Cth).</p>'

        + '<h2>What we collect</h2>'
        + '<ul>'
          '<li><strong>Things you give us:</strong> your name, email address, phone number, and anything you '
          'write in a form, an enquiry or a booking note.</li>'
          '<li><strong>Booking and payment details:</strong> what you booked, when, and what you paid. Card '
          'details are handled by our payment provider, not by us. We never see or store your full card number.</li>'
          '<li><strong>Information collected automatically:</strong> your IP address, browser, device type, '
          'which pages you looked at and how you found us. This comes through cookies and analytics tools.</li>'
          '</ul>'
        + studio_bits

        + '<h2>Why we collect it</h2>'
        + '<ul><li>To take your booking and deliver the class, session, program or event</li>'
          '<li>To keep you safe and adapt what we do to your body and circumstances</li>'
          '<li>To reply to you, send confirmations and reminders, and answer questions</li>'
          '<li>To send you emails about our offerings, if you have asked us to</li>'
          '<li>To understand what is useful on our website and improve it</li>'
          '<li>To meet our legal, tax and insurance obligations</li></ul>'

        + '<h2>Who we share it with</h2>'
        + '<p>We do not sell your personal information. Ever. We share it only with the service providers who '
          'help us run the business, and only to the extent they need it:</p>'
        + '<ul><li><strong>Tekmatix</strong> &ndash; our customer relationship, booking, email and payment platform</li>'
          '<li><strong>Google</strong> &ndash; website analytics and our Google Business Profile</li>'
          '<li><strong>Meta</strong> &ndash; if you reach us through Facebook or Instagram, or see our ads</li>'
          '<li>Our accountant, insurer or legal advisers, where genuinely necessary</li>'
          '<li>Anyone we are required to disclose to by law</li></ul>'
        + '<p>Some of these providers store data on servers outside Australia, including in the United States. '
          'Where that happens we take reasonable steps to make sure your information stays protected to a '
          'standard comparable to Australian law.</p>'

        + '<h2>Email and unsubscribing</h2>'
        + '<p>We only email you if you have signed up, bought something, or enquired. Every marketing email '
          'has an unsubscribe link, and we act on it promptly. Unsubscribing from marketing does not stop '
          'important messages about a booking you have made.</p>'

        + '<h2>Cookies</h2>'
        + '<p>Our website uses cookies to remember your preferences and to understand how people use the site. '
          'You can block or delete cookies in your browser settings. Some parts of the site may not work as '
          'well if you do.</p>'

        + '<h2>How we protect it</h2>'
        + '<p>We use reputable providers with their own security controls, we limit who on our side can see '
          'your information, and we keep it only as long as we need it or as long as the law requires. No '
          'system is perfectly secure, and we will not pretend otherwise. If something goes wrong in a way '
          'that is likely to cause you serious harm, we will tell you and notify the Office of the Australian '
          'Information Commissioner, as the law requires.</p>'

        + '<h2>Your rights</h2>'
        + '<p>You can ask us to:</p>'
        + '<ul><li>Tell you what personal information we hold about you</li>'
          '<li>Give you a copy of it</li>'
          '<li>Correct anything that is wrong or out of date</li>'
          '<li>Delete it, where we are not required to keep it</li>'
          '<li>Stop sending you marketing</li></ul>'
        + '<p>Email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a> and we will respond within 30 days. '
          'We may need to confirm who you are first.</p>'

        + '<h2>Children</h2>'
        + '<p>Our services are intended for adults. We do not knowingly collect information from anyone under '
          '16 without a parent or guardian involved.</p>'

        + '<h2>If you are not happy</h2>'
        + '<p>Tell us first, at <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>. We would rather hear it and '
          'fix it. If we cannot resolve it, you can complain to the Office of the Australian Information '
          'Commissioner at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener">oaic.gov.au</a> '
          'or on 1300 363 992.</p>'

        + '<h2>Changes</h2>'
        + '<p>If we change this policy we will update the date at the top. Material changes will be '
          'communicated to you.</p>'
        + '</div>'))

def terms_body(brand, domain, is_studio):
    studio_bits=''
    if is_studio:
        studio_bits=(
          '<h2>Classes and bookings</h2>'
          '<p>Classes are booked through our booking system. Spaces are limited, so please book ahead. '
          'Memberships have no lock-in contract and can be cancelled in line with the terms shown at the '
          'time you join.</p>'
          '<h3>Cancellations and no-shows</h3>'
          '<p>Please cancel as early as you can so someone on the waitlist can take your place. The '
          'cancellation window and any late-cancellation or no-show conditions are shown when you book. '
          'If something genuinely unavoidable comes up, talk to us. We are reasonable people.</p>'
          '<h3>Class passes and memberships</h3>'
          '<p>Class packs have an expiry period shown at purchase. Memberships bill on a recurring basis '
          'until you cancel. We do not offer refunds for unused classes, but we will always try to find a '
          'fair outcome if your circumstances change substantially.</p>'
          '<h2>Your health and safety</h2>'
          '<p>Movement, massage, breathwork and energy work carry some inherent risk. By taking part you '
          'confirm that:</p>'
          '<ul><li>You have told us about any injuries, conditions, pregnancy or medications relevant to '
          'your safety, and you will tell us if those change</li>'
          '<li>You have sought medical advice if you are unsure whether a class or session is right for you</li>'
          '<li>You will work at your own pace and stop if something does not feel right</li>'
          '<li>You take part at your own risk, and understand that our instructors cannot see inside your body</li></ul>'
          '<p>We will adapt and support you wherever we can. We are not able to supervise what you choose to '
          'push through.</p>'
          '<h2>Our services are not medical care</h2>'
          '<p>Our classes, massage, reiki, breathwork, hypnosis, coaching and nutrition support are '
          'complementary wellbeing services. They are not a substitute for medical or psychological care, '
          'and nothing we offer is a diagnosis or a replacement for advice from your doctor. Please keep '
          'your healthcare practitioners in the loop, and never stop prescribed medication on our account.</p>'
          '<h2>Studio conduct</h2>'
          '<p>This is a shared space built on safety and respect. We ask that you arrive on time, keep '
          'phones silent, respect other people&rsquo;s privacy and belongings, and treat our instructors and '
          'each other kindly. We reserve the right to end a membership or ask someone to leave if that is '
          'not happening.</p>')
    return (hero('Legal','Terms &amp; Conditions.',
        'The practical agreement between us. Clear, fair, and written so you can actually read it.',
        [('Contact us','contact.html','btn-ghost')])
      + sec('<div class="legal-doc">'
        + '<div class="legal-note"><strong>Draft for review.</strong> These terms have been prepared for '
          + brand + ' and are awaiting final review. Last updated ' + LEGAL_UPDATED + '.</div>'
        + '<h2>About these terms</h2>'
        + '<p>These terms apply when you use ' + domain + ', book with us, or buy anything from us. By doing '
          'any of those things you are agreeing to them. If you do not agree, please do not book.</p>'
        + '<p>' + brand + ' is based in Cleveland, Queensland, Australia. Contact us at '
          '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.</p>'
        + studio_bits

        + '<h2>Programs, events and retreats</h2>'
        + '<p>Programs, workshops, events and retreats have their own dates, inclusions, payment terms and '
          'cancellation conditions. These are set out at the point of booking and form part of these terms. '
          'Retreat and event deposits are generally non-refundable because we commit to venues and suppliers '
          'on your behalf, though places can often be transferred. Ask us.</p>'

        + '<h2>Coaching and memberships</h2>'
        + '<p>Coaching is a collaborative process. We bring our full attention, experience and care. We '
          'cannot and do not guarantee a particular outcome, because the results depend on your '
          'circumstances and your participation. Recurring memberships continue until cancelled in line '
          'with the terms shown when you join.</p>'

        + '<h2>Payments</h2>'
        + '<p>Prices are in Australian dollars and include GST where it applies. Payment is due as set out '
          'at booking. Payments are processed by our payment provider. If a payment fails we may pause '
          'access until it is resolved.</p>'

        + '<h2>Refunds and your consumer rights</h2>'
        + '<p>Nothing in these terms limits your rights under the Australian Consumer Law. You are always '
          'entitled to a remedy if a service is not delivered with due care and skill or does not match '
          'what we described. Outside of that, refunds are at our discretion and we will deal with you '
          'fairly. If you are unhappy, tell us.</p>'

        + '<h2>Our content</h2>'
        + '<p>The words, images, recordings, meditations, guides and program materials on this site and in '
          'our programs belong to us. You are welcome to use them for your own personal benefit. Please do '
          'not copy, resell, share or teach from them without our written permission.</p>'

        + '<h2>Your content</h2>'
        + '<p>If you send us a testimonial, review, photo or message, you give us permission to share it in '
          'our marketing, with your first name or initials. Tell us if you would rather we did not, and we '
          'will not.</p>'

        + '<h2>Liability</h2>'
        + '<p>To the extent the law allows, we are not liable for indirect or consequential loss arising '
          'from your use of this site or our services. Where we are liable, our liability is limited to '
          're-supplying the service or refunding what you paid for it. Nothing here excludes liability that '
          'cannot lawfully be excluded, including for death or personal injury caused by our negligence.</p>'

        + '<h2>Other websites</h2>'
        + '<p>We link to other sites and services. We do not control them and are not responsible for their '
          'content or their privacy practices.</p>'

        + '<h2>Changes</h2>'
        + '<p>We may update these terms. The current version is always the one on this page, with the date '
          'shown at the top. Changes do not affect a booking you have already made.</p>'

        + '<h2>Governing law</h2>'
        + '<p>These terms are governed by the laws of Queensland, Australia.</p>'

        + '<h2>Privacy</h2>'
        + '<p>How we handle your information is set out in our '
          '<a href="privacy.html">Privacy Policy</a>, which forms part of these terms.</p>'
        + '</div>'))

# ---------------------------------------------------------------- ENQUIRY FORM
# TODO before go-live: replace the whole <form> below with the Tekmatix form
# embed code. Tekmatix > Sites > Forms > build the form > Integrate > copy the
# iframe. Until then this form posts nowhere and simply shows a thank-you note.
def enquiry_form(kicker, h2, intro, options, button, tag):
    opts=''.join('<option>%s</option>'%o for o in options)
    return sec(head(kicker,h2,intro)
      + '<!-- TEKMATIX FORM SLOT: replace this form with the Tekmatix embed. Tag: '+tag+' -->'
      + '<form class="nd-form" id="enquiry" novalidate>'
        '<div class="row-2">'
          '<div><label for="f-name">First name</label>'
          '<input id="f-name" name="first_name" type="text" autocomplete="given-name" required></div>'
          '<div><label for="f-last">Last name</label>'
          '<input id="f-last" name="last_name" type="text" autocomplete="family-name"></div>'
        '</div>'
        '<div class="row-2">'
          '<div><label for="f-email">Email</label>'
          '<input id="f-email" name="email" type="email" autocomplete="email" required></div>'
          '<div><label for="f-phone">Phone (optional)</label>'
          '<input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>'
        '</div>'
        '<div><label for="f-about">What is this about?</label>'
        '<select id="f-about" name="enquiry_type">'+opts+'</select></div>'
        '<div><label for="f-msg">Your message</label>'
        '<textarea id="f-msg" name="message" placeholder="Tell us a little about where you are at. '
        'There is no right way to fill this in."></textarea></div>'
        '<div class="btn-row"><button class="btn btn-gold" type="submit">'+button+'</button></div>'
        '<p class="fine">We reply to everything, usually within one business day. Your details stay with us '
        'and are handled as set out in our <a href="privacy.html">Privacy Policy</a>. '
        'No newsletter signup happens here unless you ask for it.</p>'
        '<p class="fine" id="f-done" style="display:none"><strong>Thank you. Your message has not been sent '
        'yet because this form is still being connected. Please email '+EMAIL+' in the meantime.</strong></p>'
      '</form>'
      + '<script>(function(){var f=document.getElementById("enquiry");if(!f)return;'
        'f.addEventListener("submit",function(e){e.preventDefault();'
        'document.getElementById("f-done").style.display="block";});})();</script>','ivory')

_TONES=['forest','burgundy','navy','olive','gold','beige']
_tone_i=[0]
def _next_tone():
    t=_TONES[_tone_i[0]%len(_TONES)]; _tone_i[0]+=1; return t
def split(img_alt, text_html, reverse=False, tone=None, cls='', photo=None, pos=None):
    # legacy calls sometimes pass a section colour as the 3rd positional arg
    if isinstance(reverse,str): cls=cls or reverse; reverse=False
    img=photofig(photo,img_alt,tone or _next_tone(),pos) if photo else imgph(img_alt, tone or _next_tone())
    txt='<div>%s</div>'%text_html
    order=(txt+img) if reverse else (img+txt)
    return '<section class="sec %s"><div class="wrap"><div class="split">%s</div></div></section>'%(cls,order)

# ================================================================ WELLNESS PAGES
NDW_PAGES=[]
def W(slug,title,desc,body): NDW_PAGES.append((slug,title,desc,body))

# ---- Home
W('index.html',
  'New Dawn Wellness | Pilates, Yoga &amp; Whole-Body Healing in Cleveland QLD',
  'A holistic wellness studio in Cleveland, QLD for women in midlife. Pilates, yoga, massage, reiki, breathwork, events and coaching to help you feel like yourself again.',
  hero_split('Pilates, yoga &amp; whole-body healing &middot; women in midlife &middot; Cleveland QLD',
    'Come home <em>to yourself.</em>',
    'A calm, grounded studio for women navigating midlife. Move from wired, tired and starting-over to steady, strong and supported &mdash; through movement, breath, healing and real support, together.',
    [('Book a class','timetable.html','btn-gold'),('Explore the studio','pilates-yoga.html','btn-ghost')],
    'Warm studio light &mdash; movement, breath, calm','gold',
    cred='Pilates &middot; Yoga &middot; Breath &middot; Healing &nbsp;&middot;&nbsp; Cleveland QLD &nbsp;&middot;&nbsp; Your first class is on us',
    photo='main-studio.jpg')
  + trust_strip('Rated <b>5.0</b> &middot; Google &amp; Facebook',
      'My life has changed for the better since I joined New Dawn.',
      '&mdash; Suzy B. &middot; Pilates &amp; Yoga member',
      'Your first class<br>is on us')
  + sec(head('Welcome to New Dawn','You&rsquo;re not inconsistent. You&rsquo;ve been carrying too much, alone.',
      'Most women don&rsquo;t need more discipline or another hard reset. They need a body that feels safe enough to follow through. This is where you set some of it down &mdash; slowly, kindly, together.'),'cream')
  + split('Warm, light-filled New Dawn studio &mdash; soft light, a calm welcome',
      '<div class="kicker">Walk through the door</div><h2>You feel it before anyone says a word.</h2>'
      '<p>The noise of the day drops away at the threshold. The light is soft. There&rsquo;s the faint warmth of something calming in the air, a low hum of music, the quiet of a room that isn&rsquo;t asking anything of you.</p>'
      '<p>Nobody looks you up and down. Nobody expects you to be fitter, further along, or anyone other than who you are today. You&rsquo;re met with a smile, shown where to put your things, and given permission &mdash; maybe for the first time in a long while &mdash; to simply arrive.</p>'
      '<p>This is what a body feels like when it finally lets its shoulders drop. That&rsquo;s where we begin.</p>',
      photo='studio.jpg')
  + sec(head('Whole-woman wellness','Three ways we hold you.',
      'Whether you arrive through your body, your becoming, or simply the need to feel supported again &mdash; there&rsquo;s a doorway here for you.')
    + feature_cards([
        ('Move','Pilates &amp; Yoga','Strength, mobility and nervous-system calm &mdash; never punishment.',['Mat Pilates','Slow-flow yoga','Yin &amp; pins'],('See classes','pilates-yoga.html')),
        ('Heal','Healing Sessions','Release what your body has been holding.',['Flow &amp; Glow lymphatic massage','Soul Restore Reiki','The Adawning Experience'],('Explore healing','flow-and-glow-massage.html')),
        ('Belong','Coaching &amp; Events','Support that holds you beyond a single class.',['6-Week Reset','Soul Mastery Sanctuary','Events &amp; retreats'],('Find your path','6-week-reset.html')),
      ],highlight=1))
  + sec(head('Where to begin','Not sure where to start? Follow the path.',
      'You don&rsquo;t have to choose everything at once. Most women start with one door, and let the next one open when they&rsquo;re ready.')
    + cards_link([
      ('Weekly Classes','<strong>For you if</strong> you want to move, breathe and reset &mdash; drop in when life allows, no commitment.','pilates-yoga.html','Start with a class'),
      ('The 6-Week Reset','<strong>For you if</strong> you&rsquo;re done starting over and want structure, support and real accountability.','6-week-reset.html','Begin the Reset'),
      ('Soul Mastery Sanctuary','<strong>For you if</strong> you&rsquo;re ready to go deeper &mdash; the emotional and identity work, held in community.','soul-mastery-sanctuary.html','Go deeper'),
      ('1:1 with Dawn','<strong>For you if</strong> you want private, premium work at your own pace &mdash; over on Dawn&rsquo;s coaching site.','https://dawnedwards-jones.com/soul-mastery-ascension.html','Work 1:1'),
    ]),'beige')
  + pullquote('&ldquo;Your body isn&rsquo;t broken. It&rsquo;s overwhelmed.&rdquo;')
  + sec(head('Find your way in','Wherever you are, there&rsquo;s a door here for you.')
    + cards_link([
      ('Pilates &amp; Yoga','Mat Pilates and slow-flow classes for real bodies in midlife.','pilates-yoga.html','See classes'),
      ('The 6-Week Reset','Our signature program &mdash; movement, nervous-system support and accountability.','6-week-reset.html','Learn more'),
      ('Flow &amp; Glow Lymphatic Massage','Gentle, rhythmic hands-on work to ease puffiness, heaviness and fatigue.','flow-and-glow-massage.html','Book a session'),
      ('Soul Mastery Sanctuary','Ongoing group coaching for the emotional and identity work.','soul-mastery-sanctuary.html','Step inside'),
      ('Wellness Events','Breathwork, women&rsquo;s circles, menopause workshops and more.','wellness-events.html','What&rsquo;s on'),
      ('Retreats','Day immersions and longer resets to fully switch off.','retreats.html','Explore retreats'),
    ]),'ivory')
  + quotes([
      ('My life has changed for the better since I joined New Dawn Pilates &amp; Yoga. The classes are fabulous, the teachers are amazing, and the friendliness of the studio is incredible.','&mdash; Suzy B. &middot; Pilates &amp; Yoga member'),
      ('I felt held in a safe, supportive space where I could fully relax and let go. I left feeling calm, grounded and deeply restored &mdash; and I slept so well afterwards.','&mdash; Cate N. &middot; Yin &amp; Pins evening'),
      ('A beautiful, transformative experience. I left feeling lighter, like a weight had been lifted and my body was flowing again.','&mdash; Jorja Z. &middot; Healing session'),
    ])
  + optin('Free guide','The 3-Minute Nervous System Reset.',
      'A simple, practical way to calm an overwhelmed body &mdash; in three minutes, anywhere. Enter your email and we&rsquo;ll send it straight over, along with the occasional grounded note from the studio.',
      'Send me the guide','No pressure, no spam. Unsubscribe any time.','forest')
  + cta_band('You don&rsquo;t need to do more. You need to be supported properly.',
      [('Book your first class','timetable.html','btn-gold'),('Say hello','contact.html','btn-ghost')],'navy')
  + crosslink('Looking for Dawn&rsquo;s speaking, coaching or book?','https://dawnedwards-jones.com','Meet Dawn Edwards-Jones &rarr;'))

# ---- About: Our Story
W('our-story.html','Our Story | About New Dawn Wellness, Cleveland QLD',
  'The story behind New Dawn Wellness in Cleveland, QLD. A holistic studio helping women in midlife move from overwhelm to calm, embodied wellbeing.',
  hero('Our story','More than a studio.',
    'New Dawn began with a simple belief. Women aren&rsquo;t failing. They&rsquo;re trying to function in overwhelmed, under-supported bodies. This is the space we wished existed.',
    [('Meet Dawn','meet-dawn.html','btn-gold'),('See our space','our-space.html','btn-ghost')])
  + split('A calm treatment room, soft natural light',
      '<div class="kicker">What we believe</div><h2>Your body isn&rsquo;t broken. It&rsquo;s overwhelmed.</h2>'
      '<p>For years, women have been told to try harder, eat less and just be more disciplined. We see it differently. When the nervous system is stretched thin by stress, hormones, caretaking and constant doing, no amount of willpower holds.</p>'
      '<p>At New Dawn we start with safety. We calm the body first, then build strength, habits and consistency on top of it. That&rsquo;s why it lasts.</p>',
      photo='studio.jpg')
  + sec(head('How it began','A studio built from the inside out.',
      'New Dawn didn&rsquo;t start as a business plan. It started with one woman&rsquo;s own body, and the slow realisation that what had helped her was the thing most women were never offered.')
    + story([
      ('01','A back that wouldn&rsquo;t settle',
        '<p>Dawn lived with back pain for years. She tried everything, and eventually accepted that pain was simply part of her life now. Then an osteopath suggested Pilates. Within a few sessions the pain began to lift, and she never looked back.</p>'
        '<p>That was the first clue. Her body hadn&rsquo;t needed force. It had needed the right support.</p>'),
      ('02','The pattern in every conversation',
        '<p>As Dawn began teaching, the same story arrived in the room again and again. Capable, generous, high-functioning women who felt like they were failing at consistency. Women who had done the diets, the programs, the early alarms, and still ended up back at the start.</p>'
        '<p>They weren&rsquo;t lazy or undisciplined. They were depleted. Running a full life on a nervous system that had been in survival mode for years.</p>'),
      ('03','Movement alone wasn&rsquo;t enough',
        '<p>Pilates and yoga changed bodies. But Dawn kept noticing that the women who truly changed were the ones who also felt safe, seen and supported. The breath work mattered. The conversations after class mattered. Being known mattered.</p>'
        '<p>So the studio grew to hold more than movement. Breathwork, sound, hands-on healing, hypnosis, coaching, and community.</p>'),
      ('04','New Dawn as it is now',
        '<p>Today New Dawn is a whole-woman wellness studio in the heart of Cleveland. A place to move, release, learn and belong. Not a gym, not a trend, and never somewhere you have to earn your rest.</p>'
        '<p>Women come for a class. Many stay for years.</p>'),
    ]),'cream')
  + pullquote('&ldquo;You&rsquo;re not inconsistent. You&rsquo;ve been carrying too much, alone.&rdquo;','New Dawn Wellness')
  + sec(head('How we hold you','A whole-woman approach.',
      'Four parts of you, tended together. Most places look after one and hope the rest follows.')
    + cards([
      ('The physical body','Pilates and yoga to rebuild strength, mobility and steadiness.',''),
      ('The nervous system','Breathwork, reiki and hypnosis to move you out of survival mode.',''),
      ('The emotional body','Coaching and community for the identity work underneath the habits.',''),
      ('The whole life','Nutrition and menopause support so you feel resourced, not depleted.',''),
    ]),'ivory')
  + cta_band('This is a place where women feel seen, safe and supported.',
      [('Book a class','timetable.html','btn-gold'),('Come and see the space','our-space.html','btn-ghost')]))

# ---- About: Meet Dawn
W('meet-dawn.html','Meet Dawn Edwards-Jones | Founder of New Dawn Wellness',
  'Meet Dawn Edwards-Jones, founder of New Dawn Wellness in Cleveland QLD. Pilates and yoga teacher, breathwork facilitator and nervous system coach for women in midlife.',
  hero_split('Meet your teacher','Hello, I&rsquo;m Dawn.',
    'I teach Pilates and yoga, I hold breathwork and healing sessions, and I coach women through the midlife seasons that nobody prepares you for. Mostly, I hold the kind of space I spent years wishing someone would hold for me.',
    [('Book a class with me','timetable.html','btn-gold'),('Say hello','contact.html','btn-ghost')],
    'Dawn Edwards-Jones, founder of New Dawn Wellness','gold',
    cred='Pilates &middot; Yoga &middot; Breathwork &middot; Hypnosis &middot; Nervous system coaching',
    photo='dawn-portrait-smile.jpg',pos='center top')
  + split('Dawn teaching, hands guiding a student gently',
      '<div class="kicker">Why I do this</div><h2>I know what it&rsquo;s like to brace against your own body.</h2>'
      '<p>I lived with back pain for years. I&rsquo;d tried everything, and I&rsquo;d quietly accepted that this was simply my life now. Then an osteopath suggested Pilates. Within a few sessions the pain started to lift, and something else lifted with it.</p>'
      '<p>It wasn&rsquo;t just my back. It was the low hum of dread about what my body could and couldn&rsquo;t do. That&rsquo;s the thing I most want to hand to other women.</p>'
      '<p>So this isn&rsquo;t a class I run. It&rsquo;s the thing that changed what my days felt like.</p>',
      True,photo='studio.jpg')
  + sec(head('What I actually do','More than one thing, on purpose.',
      'Bodies don&rsquo;t separate neatly into physical, emotional and mental. So I don&rsquo;t teach as though they do.')
    + cards([
      ('Pilates &amp; yoga','Mat Pilates, yin, slow flow and restorative. Small classes, real attention, no ego.',''),
      ('Breathwork &amp; sound','Guided sessions that move you out of survival mode and into genuine rest.',''),
      ('Hands-on healing','Lymphatic massage and reiki, held privately and unhurried.',''),
      ('Hypnosis','The Adawning Experience, a personalised session you take home as a recording.',''),
      ('Coaching','Nervous system and identity work, in group and one to one.',''),
      ('Events &amp; retreats','Workshops, women&rsquo;s circles and day immersions across the Redlands.',''),
    ]),'cream')
  + split('Dawn leading a retreat, arms open, women gathered behind',
      '<div class="kicker">How I teach</div><h2>You will never be shouted at in my room.</h2>'
      '<p>I don&rsquo;t believe anyone changes because they were made to feel bad about themselves. I&rsquo;ve watched hundreds of women try that route and end up more depleted than when they started.</p>'
      '<p>In my classes, resting is a valid choice. Every movement has an easier version. If something hurts, we change it. If you&rsquo;ve had a week where getting through the door is the achievement, then getting through the door is the achievement.</p>'
      '<ul class="ticks"><li>Nobody watches you</li><li>Nobody expects you to keep up</li><li>You work in the body you actually have today</li><li>You tell me about your injuries and I build around them</li></ul>',
      photo='nd-dawn-leading.jpg')
  + quotes([
      ('The instructors are highly experienced and genuinely care about their students, creating a wonderful community atmosphere. I couldn&rsquo;t recommend it more highly.','Kirsty L. &middot; Yoga &amp; Pilates'),
      ('From the moment I walked in, her calm and nurturing energy made me feel completely safe and held.','Mel T. &middot; Lymphatic massage'),
      ('Dawn is an incredibly intuitive and caring healer.','Donna H. &middot; Healing session'),
    ])
  + cta_band('When you&rsquo;re ready, I&rsquo;m here.',
      [('Book your first class','timetable.html','btn-gold'),('Meet the full team','instructors.html','btn-ghost')],'navy')
  + crosslink('Looking for Dawn&rsquo;s speaking, coaching or book?',DEJ_URL,'Visit dawnedwards-jones.com &rarr;'))

# ---- About: Our Space
W('our-space.html','Our Space | Visit New Dawn Wellness, Cleveland QLD',
  'Find New Dawn Wellness at 4 Cross Street, Cleveland QLD 4163. Class studio, sound healing, breathwork and in-person events. Parking, what to bring and how to book.',
  hero('Our space','Come and see us.',
    'Our studio sits on the corner of North Street and Cross Street in Cleveland, just before the Grand View Hotel, in the old Op Shop building.',
    [('See the timetable','timetable.html','btn-gold')])
  + split('Warm, light-filled studio interior with soft natural light',
      '<div class="kicker">Walk through the door</div><h2>You feel it before anyone says a word.</h2>'
      '<p>The noise of the day drops away at the threshold. The light is soft. There&rsquo;s the faint warmth of something calming in the air, a low hum of music, the quiet of a room that isn&rsquo;t asking anything of you.</p>'
      '<p>Nobody looks you up and down. Nobody expects you to be fitter, further along, or anyone other than who you are today. You&rsquo;re met with a smile, shown where to put your things, and given permission to simply arrive.</p>',
      photo='studio.jpg')
  + sec('<div class="split">'
      + photofig('nd-studio-exterior.jpg','Exterior of the Cleveland studio with New Dawn flags flying','gold')
      + '<div><div class="kicker">The studio</div><h2>4 Cross Street, Cleveland</h2>'
        '<p>Our public studio is home to Pilates and yoga classes, sound healing, breathwork and in-person events. A warm, light-filled space designed to slow your whole system down the moment you walk in.</p>'
        '<ul class="ticks"><li>Cnr 41 North Street &amp; 4 Cross Street, Cleveland QLD 4163</li>'
        '<li>Street parking available nearby</li>'
        '<li>Mats and props provided, so just bring water and comfortable clothes</li>'
        '<li>Arrive 10 minutes early for your first visit</li></ul>'
        '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Get in touch</a></div></div></div>','cream')
  + sec('<div class="split">'
      + '<div><div class="kicker">Hands-on healing</div><h2>Private appointments</h2>'
        '<p>Flow &amp; Glow lymphatic massage, Soul Restore reiki and The Adawning Experience are held at a separate, private home studio for a quiet, undisturbed experience. The address is shared with you when you book.</p>'
        '<div class="btn-row"><a class="btn btn-ghost" href="flow-and-glow-massage.html">Flow &amp; Glow Massage</a><a class="btn btn-ghost" href="soul-restore-reiki.html">Soul Restore Reiki</a></div></div>'
      + photofig('nd-massage-room.jpg','Private healing room, candlelit and calm','olive')
      + '</div>')
  + faqs([
      ('Where exactly do I park?','There&rsquo;s street parking on Cross Street and North Street, and more a short walk away. On busier evenings give yourself a few extra minutes.'),
      ('What should I bring?','Water and something comfortable you can move in. Mats, blocks, bolsters and props are all here.'),
      ('Is the studio accessible?','The class studio is at street level. If you have specific access needs, send us a message before you come and we&rsquo;ll talk you through exactly what to expect.'),
      ('Can I come and look around first?','Of course. Get in touch and we&rsquo;ll find a quiet time for you to come in, see the space and ask anything you like.'),
    ])
  + cta_band('Come as you are. That&rsquo;s genuinely all we ask.',
      [('Book your first class','timetable.html','btn-gold'),('Message us first','contact.html','btn-ghost')],'navy'))

# ---- Pilates & Yoga
W('pilates-yoga.html','Pilates &amp; Yoga in Cleveland QLD | New Dawn Wellness',
  'Mat Pilates and slow, mindful yoga in Cleveland, QLD. Small, unhurried classes for women in midlife &mdash; strength, mobility and a calmer nervous system.',
  hero('Move','Pilates &amp; Yoga for real bodies.',
    'Strength without strain. Movement that steadies your nervous system as it builds your body. Small classes, real attention, no mirrors-and-ego gym energy &mdash; just a warm room, a good teacher, and your own pace.',
    [('View timetable &amp; book','timetable.html','btn-gold')])

  + sec(head('Why this, why here','Movement that regulates &mdash; not depletes.',
      'Most of us were taught to attack our bodies into shape: push harder, burn more, earn the rest. If you&rsquo;re a woman in midlife carrying a full life, that approach doesn&rsquo;t just stop working &mdash; it quietly makes things worse. More cortisol on an already-flooded system. Another thing to fail at. Here, movement does the opposite. It tells your body it&rsquo;s safe. And a body that feels safe is a body that gets stronger, sleeps better, and stops bracing all day long.')
    + manifesto([
        ('You don&rsquo;t need to be flexible to start.',''),
        ('You don&rsquo;t need to be fit to start.',''),
        ('You don&rsquo;t need to have &ldquo;kept it up.&rdquo;',''),
        ('You just need to walk through the door.',''),
        ('Everything else, we&rsquo;ll meet you where you are &mdash; on the day, in the body you actually have.','small'),
      ]),'cream')

  + split('Woman in her fifties doing mat Pilates in a calm, light-filled studio',
      '<div class="kicker">Pilates</div><h2>Strength from the inside out.</h2>'
      '<p>Pilates builds you from your centre &mdash; the deep core muscles that hold you upright, steady your spine and protect your back. It&rsquo;s low-impact and kind on joints, but don&rsquo;t mistake gentle for easy. You use your own body weight and small props to build real, functional strength: the kind that makes carrying shopping, getting off the floor and standing tall feel effortless again.</p>'
      '<p>We teach <strong>mat</strong> Pilates, across classes like Core &amp; Floor and Mat Sculpt &mdash; so whether you want to lengthen and release or build and control, there&rsquo;s a class that fits.</p>',
      photo='studio.jpg')

  + split('Woman on a mat in a calm, light-filled Pilates class',
      '<div class="kicker">Why I teach it</div><h2>It gave me my back &mdash; and my life &mdash; back.</h2>'
      '<p>I lived with a bad back for years. I&rsquo;d tried everything, and I&rsquo;d quietly accepted that pain was just part of my life now. Then an osteopath suggested Pilates. Within a few sessions the pain began to lift &mdash; and I never looked back.</p>'
      '<p>That&rsquo;s why this isn&rsquo;t just a class I run. It&rsquo;s the thing that changed what my days felt like. I know exactly what it&rsquo;s like to move through life braced against your own body &mdash; and I know what it feels like to be handed a way out.</p>'
      '<p class="attrib">&mdash; Dawn</p>',True)

  + sec(head('The six principles','What makes Pilates different.',
      'Every movement is built on the six principles Joseph Pilates&rsquo; students drew from his work. They&rsquo;re the reason a slow, controlled Pilates class does more for your body than an hour of frantic effort.')
    + cards([
      ('Concentration','Full attention on the movement &mdash; which, as it happens, is also a break for an overloaded mind.',''),
      ('Control','Every movement is deliberate. Nothing thrown, nothing forced &mdash; so nothing gets injured.',''),
      ('Centre','Everything begins in your core &mdash; the &ldquo;powerhouse&rdquo; that stabilises your whole body.',''),
      ('Breath','Full, intentional breathing that oxygenates the body and settles the nervous system.',''),
      ('Precision','Quality over quantity. A few precise reps beat dozens of sloppy ones.',''),
      ('Flow','Movements link smoothly and gracefully &mdash; strength and calm in the same breath.',''),
    ]),'ivory')

  + split('Older woman smiling mid-stretch, strong and at ease',
      '<div class="kicker">For every body &mdash; especially the wiser ones</div><h2>&ldquo;Someone supple and strong at 60 is still young.&rdquo;</h2>'
      '<p>Joseph Pilates said it best: <em>&ldquo;Anyone who is stiff and out of shape at 30 is old, while someone who is supple and strong at 60 is still young.&rdquo;</em> Pilates is one of the safest, most effective ways to keep a maturing body strong, mobile and confident on its feet.</p>'
      '<ul class="ticks">'
      '<li>Zero impact &mdash; easy on joints, safe with arthritis and old injuries</li>'
      '<li>Better circulation, flexibility and leaner, longer muscle</li>'
      '<li>Less stiffness and eased joint pain</li>'
      '<li>Lightweight but genuinely challenging &mdash; a whole-body workout</li>'
      '<li>Improved balance, which lowers the risk of falls and fractures</li>'
      '</ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="timetable.html">Find a class time</a></div>')

  + split('Woman in a calm, supported yoga pose at New Dawn studio',
      '<div class="kicker">Yoga</div><h2>Come back into your body.</h2>'
      '<p>This is yoga for a nervous system that&rsquo;s been running too hot for too long. Nothing to reach for, nobody to keep up with &mdash; just breath, support and permission to soften. Whatever style you land in, the aim is the same: to leave steadier than you arrived.</p>',
      True,photo='yoga.jpg')
  + sec(head('Yoga','Slow, mindful, and deeply restorative.',
      'Our yoga isn&rsquo;t about touching your toes or holding a perfect shape. It&rsquo;s about coming back into a body that&rsquo;s been running on adrenaline &mdash; and letting it soften. Each style below meets a different need. You don&rsquo;t have to choose perfectly; you just have to start.')
    + feature_cards([
      ('01','Yin Yoga',
        'Slow, floor-based poses held for three to five minutes, working deep into the hips, pelvis, inner thighs and lower spine &mdash; the places we store years of tension. Rooted in Taoist practice going back some two thousand years, and always supported with props so your body can truly let go.',
        ['Calms a busy mind and lowers stress','Builds flexibility in the connective tissue','Balances the nervous system','Improves circulation and mental focus'],None),
      ('02','Slow &amp; Mindful / Restorative',
        'The exact opposite of &ldquo;no pain, no gain.&rdquo; Fully supported poses held for five to twenty minutes on bolsters, blocks and blankets, so your body does nothing but rest &mdash; and resets straight into the parasympathetic, &ldquo;rest and digest&rdquo; state. Gentle enough for pregnancy, chronic pain, illness and recovery.',
        ['Soothes the nervous system','Lowers blood pressure and lifts mood','Improves sleep and supports immunity','Safe for almost every body and stage'],None),
      ('03','Vinyasa (Slow Flow)',
        'Breath-led movement where each pose flows into the next in time with your breathing. It builds real strength, mobility and energy &mdash; and, done at our unhurried pace, it clears the mind rather than draining you. New to yoga? Start with our meditation and intro class first, then flow.',
        ['Builds strength, core stability and mobility','Steadies the mind and reduces stress','Lifts energy and improves sleep','Grows focus and quiet confidence'],None),
      ('04','Yoga &amp; Meditation',
        'Movement and stillness woven together &mdash; the gentlest way in if you&rsquo;re brand new, or the deepest way to land if your mind never switches off. We finish settled, not stirred up.',
        ['A calm, judgement-free entry point','Trains the nervous system to downshift','Leaves you clearer, softer and rested'],None),
    ],highlight=-1),'cream')

  + sec(head('Pilates or yoga?','How they actually differ.',
      'People ask us this constantly, usually worried about picking the wrong one. You cannot. Most women end up doing both, because they do different jobs. Here is the honest difference.')
    + cards([
      ('Pilates builds','Controlled, repeatable strength from your deep core outwards. Think spine, pelvis, posture, stability. You leave feeling held together.',''),
      ('Yoga releases','Length, breath and softening. Longer holds, more stillness, more letting go. You leave feeling unwound.',''),
      ('Pilates feels like','Precise and deliberate. A steady count, small ranges, a quiet burn. Your attention is on the muscle doing the work.',''),
      ('Yoga feels like','Slower and more internal. Breath leads, props support you, and nothing is rushed. Your attention is on the breath.',''),
      ('Choose Pilates if','You have back pain, weak core, poor posture, or you want to feel physically stronger and more stable on your feet.',''),
      ('Choose yoga if','You cannot switch off, you are wired and exhausted at once, or your body is asking to rest rather than work.',''),
    ])
    + '<p style="max-width:720px;margin:22px auto 0;text-align:center">Still not sure? Come to either one. Your first class is free, and we will tell you honestly which room your body needs this week.</p>'
    + '<div class="btn-row" style="justify-content:center;margin-top:18px">'
      '<a class="btn btn-gold" href="timetable.html">See the timetable</a>'
      '<a class="btn btn-ghost" href="membership.html">Membership &amp; class options</a></div>','ivory')

  + split('Women mid-flow in a New Dawn class, daylight through the open door',
      '<div class="kicker">Your first class</div><h2>What actually happens when you arrive.</h2>'
      '<p>Arrive about ten minutes early. Wear something you can move in &mdash; no special gear needed. Tell your teacher about any injuries, aches or things you&rsquo;re nervous about; that&rsquo;s exactly what they want to know. Then you find a spot, and we begin, gently.</p>'
      '<p>Nobody watches you. Nobody expects you to know the moves. Everything is offered with an easier option, and &ldquo;rest here for a moment&rdquo; is always a valid choice. You&rsquo;ll leave looser than you came &mdash; and, most people tell us, calmer than they&rsquo;ve felt all week.</p>'
      '<p><strong>Your first class is free.</strong> No pressure to sign up to anything &mdash; just come and feel what it&rsquo;s like.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="timetable.html">Book your free first class</a></div>',
      True,photo='nd-yoga-flow.jpg')

  + pullquote('&ldquo;Your body isn&rsquo;t broken. It&rsquo;s overwhelmed.&rdquo;','&mdash; New Dawn Wellness')

  + quotes([
      ('Classes promoted a safe, non-judgmental atmosphere where individuals could work at their own pace. I&rsquo;d recommend New Dawn to anyone, complete beginner or experienced.','&mdash; Ann H. &middot; Mat Pilates &amp; Yoga'),
      ('After a fractured spine, I had enough faith in one of Dawn&rsquo;s classes to sit upright from a laying position for the first time since the injury. It was quite emotional.','&mdash; New Dawn member'),
      ('The instructors are highly experienced and genuinely care about their students, creating a wonderful community atmosphere. I couldn&rsquo;t recommend it more highly.','&mdash; Kirsty L. &middot; Yoga &amp; Pilates'),
    ])

  + faqs([
      ('I&rsquo;m not flexible or fit at all. Can I still come?','Yes &mdash; that&rsquo;s exactly who these classes are built for. You don&rsquo;t need to be flexible or fit to start; that&rsquo;s what the practice gives you over time. Every movement has an easier option and you work at your own pace.'),
      ('What&rsquo;s the difference between mat and reformer Pilates?','Mat Pilates uses your own body weight and small props on a mat. Reformer Pilates uses a spring-based machine that adds support and resistance. At New Dawn we teach <strong>mat</strong> Pilates &mdash; and it&rsquo;s the perfect place to start. Mat is where you learn the fundamentals: the core control, breath and precision that everything else is built on. Don&rsquo;t mistake it for the &ldquo;easy&rdquo; option, though &mdash; working against your own body weight, with nothing to hide behind, can be every bit as challenging as the machine. Master it here and you&rsquo;ll move well anywhere.'),
      ('Which yoga class should I start with?','If your mind never switches off or you&rsquo;re recovering from something, start with Slow &amp; Mindful or Yin. If you want to build a little strength and energy, ease into Slow Flow &mdash; ideally after our meditation and intro class. When in doubt, ask us; we&rsquo;ll point you to the right first class.'),
      ('I have an injury / arthritis / a bad back. Is it safe?','Very often yes &mdash; low-impact Pilates and restorative yoga are among the kindest things you can do for joints and old injuries. Always tell your teacher beforehand so we can adapt for you. (Dawn came to Pilates for her own back pain, so you&rsquo;re in understanding hands.)'),
      ('How big are the classes?','Small &mdash; deliberately. Everyone gets real attention and hands-on adjustment where helpful. Because spots are limited, it&rsquo;s best to reserve ahead.'),
      ('Do I have to commit to anything?','No. Your first class is free, and you&rsquo;re welcome to simply come as you like. There is no lock-in on any membership either. If you later want more structure and support, the 6-Week Reset is there when you&rsquo;re ready.'),
      ('What does it cost?','Your first class is free. After that you can come casually, buy a class pack, or take an unlimited weekly membership with no contract. All current pricing is on the membership page.'),
    ])

  + cta_band('Come once. See how your body feels afterwards. Decide from there.',
      [('Book your free first class','timetable.html','btn-gold'),('See pricing &amp; memberships','membership.html','btn-ghost')],'navy')

  + sec('<p class="local-seo">Proudly in the heart of the Redlands at 4 Cross St, Cleveland QLD &mdash; welcoming women from Cleveland, Ormiston, Raby Bay, Thornlands, Alexandra Hills, Wellington Point and Victoria Point.</p>','ivory')

  + crosslink('Want structure and support alongside your classes?','6-week-reset.html','Explore the 6-Week Reset &rarr;'))

# ---- Timetable
W('timetable.html','Class Timetable &amp; Bookings | New Dawn Wellness',
  'Book Pilates, yoga, breathwork and sound-healing classes at New Dawn Wellness, Cleveland QLD. View the weekly timetable and reserve your spot.',
  hero('Timetable','Book your spot.',
    'Classes are kept small so everyone gets attention. Reserve ahead to secure your place &mdash; and if it&rsquo;s your first visit, arrive ten minutes early.',
    [('Contact us to book','contact.html','btn-gold')])
  + sec(head('Weekly rhythm','A sample of the week.',
      'Live class times and online booking are managed through our booking system &mdash; contact us and we&rsquo;ll get you set up and send the current schedule.')
    + cards([
      ('Mornings','Mat Pilates to start the day strong and steady.',''),
      ('Middays','Slow-flow yoga and gentle mobility for a mid-week reset.',''),
      ('Evenings','Yin &amp; pins, breathwork and sound healing to unwind.',''),
    ]),'cream')
  + sec(head('Booking on your phone','Book, change and cancel from the app.',
      'Our timetable and bookings run through our studio booking system, which has an app so you can reserve a spot, join a waitlist or cancel in a few taps. Once you&rsquo;re set up, you never have to message anyone to book again.')
    + cards([
      ('1. Get set up','Contact us and we&rsquo;ll create your account and send you the link to download the app.',''),
      ('2. Book your spot','Open the app, pick your class, tap book. You&rsquo;ll see live availability.',''),
      ('3. Change your mind','Cancel or move a booking from the app. Please give us as much notice as you can so someone on the waitlist can take the spot.',''),
    ]),'ivory')
  + faqs([
      ('Do I have to book, or can I just turn up?','Please book. Classes are deliberately small, so spots go. Booking ahead means you&rsquo;re not turned away at the door.'),
      ('What if the class I want is full?','Join the waitlist in the app. If someone cancels, you&rsquo;ll be notified automatically.'),
      ('How do I cancel?','In the app, or message us. As much notice as you can manage is kindest, because it frees the spot for another woman.'),
      ('Is my first class really free?','Yes. One free class, no card details, no commitment. Come and feel what it&rsquo;s like before you decide anything.'),
      ('Are the times fixed all year?','The weekly rhythm is steady, but times do shift occasionally around school holidays and events. The app always shows the live schedule.'),
    ])
  + cta_band('New here? We&rsquo;ll help you find the right first class.',
      [('Get in touch','contact.html','btn-gold'),('See membership options','membership.html','btn-ghost')]))

# ---- Membership & Class Options
W('membership.html','Membership &amp; Class Options | New Dawn Wellness, Cleveland QLD',
  'Pilates and yoga membership, casual passes and class packs at New Dawn Wellness in Cleveland QLD. Bronze Membership from $39 a week with no lock-in contract.',
  hero('Membership &amp; class options','Choose what fits your life.',
    'No lock-in contracts, no joining fees, no penalty for being a human with a full life. Just a few simple ways to come and move, so you can pick the one that suits the season you&rsquo;re in.',
    [('Find a class','timetable.html','btn-gold'),('Book your first class','contact.html','btn-ghost')])
  + sec(head('Start here','Your first class is on us.',
      'Before you choose anything, come and try it. One free class, no card details, no pressure to sign up to a thing. We&rsquo;d rather you knew how the room feels first.')
    + '<div class="btn-row" style="justify-content:center"><a class="btn btn-gold" href="contact.html">Claim your free first class</a></div>','cream')
  + sec(head('The options','Simple, flexible, honest.',
      'Most women start casually, then move onto the membership once they realise they&rsquo;re coming anyway.')
    + cards([
      ('Bronze Membership','Unlimited mat Pilates and yoga classes, every week, with no tie-in. Pause it when life gets loud and pick it back up when you&rsquo;re ready. This is the best value if you come more than once a week.','$39 / week'),
      ('Casual Class','One class, whenever it suits. Perfect if your weeks are unpredictable or you&rsquo;re still finding your rhythm.','$25'),
      ('5-Class Pack','Five classes to use at your own pace. A gentle way to commit to yourself without committing to a schedule.','$[ TBC ]'),
      ('10-Class Pack','Ten classes to use at your own pace, at a better rate per class than casual. Our most popular pack.','$[ TBC ]'),
    ]),'ivory')
  + sec(head('Current offers','What&rsquo;s available right now.',
      'We run a small number of introductory and seasonal offers. This is where they live, so you don&rsquo;t have to hunt through social media for them.')
    + cards_link([
      ('Free first class','Always on. One class on us, for anyone who hasn&rsquo;t been to New Dawn before.','contact.html','Claim it'),
      ('[ Introductory offer ]','[ Placeholder: Dawn to confirm the current intro offer, what it includes and the price. ]','contact.html','Enquire'),
      ('[ Current special ]','[ Placeholder: Dawn to confirm any seasonal special running now, or we remove this card before go-live. ]','contact.html','Enquire'),
    ]),'cream')
  + pullquote('&ldquo;You don&rsquo;t need more discipline. You need the right support.&rdquo;','New Dawn Wellness')
  + sec(head('Beyond weekly classes','When you want more than a class.',
      'Classes are the doorway. If you want structure, accountability or deeper work, these are the next steps.')
    + cards_link([
      ('The 6-Week Reset','Movement, nervous system support, simple nutrition and real accountability, over six weeks.','6-week-reset.html','Explore the Reset'),
      ('Soul Mastery Sanctuary','Ongoing group coaching for the emotional and identity work, with women beside you.','soul-mastery-sanctuary.html','Step inside'),
      ('Healing sessions','Lymphatic massage, reiki and The Adawning Experience, held privately and unhurried.','flow-and-glow-massage.html','Explore healing'),
    ]),'ivory')
  + faqs([
      ('Is there a lock-in contract?','No. The Bronze Membership has no tie-in. You can pause or stop it, and nobody will make you feel awkward about it.'),
      ('Can I pause my membership?','Yes. Life happens. Tell us your dates and we&rsquo;ll suspend your membership and reactivate it when you&rsquo;re back.'),
      ('Do class packs expire?','Give us a shout if you&rsquo;re running short of time on a pack. We&rsquo;d far rather extend it than have you lose classes you&rsquo;ve paid for.'),
      ('Which option should I choose?','If you&rsquo;re coming once a week or less, casual or a pack. If you&rsquo;re coming twice a week or more, the Bronze Membership works out cheaper. Not sure? Start casual and change your mind later.'),
      ('What if I can&rsquo;t afford it right now?','Have a quiet word with us. We would rather find something that works than have you not come at all.'),
      ('Do memberships cover events and retreats?','No, those are booked separately, because they&rsquo;re longer and held outside the normal timetable. Members usually hear about them first.'),
    ])
  + sec('<p class="local-seo">Pilates and yoga memberships at 4 Cross St, Cleveland QLD, welcoming women from Cleveland, Ormiston, Raby Bay, Thornlands, Alexandra Hills, Wellington Point and Victoria Point.</p>','ivory')
  + cta_band('Still deciding? Come to a free class first. Then choose.',
      [('Find a class','timetable.html','btn-gold'),('Book your first class','contact.html','btn-ghost')],'navy'))

# ---- Our Instructors
W('instructors.html','Our Instructors | New Dawn Wellness, Cleveland QLD',
  'Meet the Pilates and yoga instructors at New Dawn Wellness in Cleveland QLD. Experienced, warm teachers who genuinely care about the women in their classes.',
  hero('Our instructors','The women who hold the room.',
    'Small classes only work if the teacher is actually watching. Ours are experienced, warm, and far more interested in how your body is doing today than in how it compares to anyone else&rsquo;s.',
    [('See the timetable','timetable.html','btn-gold')])
  + sec(head('Our team','Experienced hands, kind eyes.',
      'Every teacher here works the same way. They ask about your injuries, they offer an easier option before you have to ask for one, and they know your name.')
    + cards([
      ('Dawn Edwards-Jones','Founder. Mat Pilates, yin, slow flow, breathwork, sound and hypnosis. Came to Pilates through her own back pain and never left.',''),
      ('[ Instructor name ]','[ Placeholder: what they teach, their training, one real sentence about how they teach and why. Photo needed. ]',''),
      ('[ Instructor name ]','[ Placeholder: what they teach, their training, one real sentence about how they teach and why. Photo needed. ]',''),
      ('[ Instructor name ]','[ Placeholder: what they teach, their training, one real sentence about how they teach and why. Photo needed. ]',''),
    ]),'cream')
  + split('A teacher adjusting a student gently, both smiling',
      '<div class="kicker">How we teach</div><h2>The same promise, whoever is in front of you.</h2>'
      '<p>You shouldn&rsquo;t have to work out which teacher is safe to be a beginner with. So we hold every class the same way, whoever is leading it.</p>'
      '<ul class="ticks"><li>You tell us about injuries, and we build around them</li>'
      '<li>Every movement has an easier version, offered before you need to ask</li>'
      '<li>Resting is a valid choice, in every class, always</li>'
      '<li>Nobody is corrected in front of the room</li>'
      '<li>We learn your name, and we notice when you&rsquo;ve been away</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="timetable.html">Find a class</a></div>',
      True,photo='studio.jpg')
  + quotes([
      ('The instructors are highly experienced and genuinely care about their students, creating a wonderful community atmosphere. I couldn&rsquo;t recommend it more highly.','Kirsty L. &middot; Yoga &amp; Pilates'),
      ('Classes promoted a safe, non-judgmental atmosphere where individuals could work at their own pace. I&rsquo;d recommend New Dawn to anyone, complete beginner or experienced.','Ann H. &middot; Mat Pilates &amp; Yoga'),
      ('My life has changed for the better since I joined. The classes are fabulous and the teachers are amazing.','Suzy B. &middot; Pilates &amp; Yoga member'),
    ])
  + cta_band('Come and meet them. Your first class is on us.',
      [('Book your first class','contact.html','btn-gold'),('See the timetable','timetable.html','btn-ghost')],'navy'))

# ---- 6 Week Reset
W('6-week-reset.html','The 6-Week Reset | New Dawn Wellness',
  'The 6-Week Reset at New Dawn Wellness &mdash; movement, nervous-system support, habit and nutrition guidance, and real accountability for women in midlife.',
  hero('The 6-Week Reset &middot; for women stuck in the start-stop cycle',
    'This is where starting over ends.',
    'Six weeks to move from wired, tired and back at square one to steady, strong and finally consistent &mdash; through movement, nervous-system support, simple nutrition and real accountability. So following through stops costing you everything you have.',
    [('Enquire now','contact.html','btn-gold')])
  + sec(head('What&rsquo;s inside','More than a fitness challenge.')
    + cards([
      ('Movement','Regular Pilates and yoga scaled to you &mdash; building strength without burnout.',''),
      ('Nervous-system support','Breath and regulation tools so your body feels safe enough to change.',''),
      ('Habits that hold','Small, sustainable shifts instead of all-or-nothing rules.',''),
      ('Nutrition support','Gentle guidance for energy, sleep and cravings &mdash; support, not restriction.',''),
      ('Accountability','You&rsquo;re checked in on and cheered on. You won&rsquo;t drift.',''),
      ('Community','You do it alongside other women who get it.',''),
    ]),'cream')
  + split('Small group of women stretching together',
      '<div class="kicker">Who it&rsquo;s for</div><h2>For the woman who&rsquo;s tired of restarting.</h2>'
      '<p>If you&rsquo;ve tried every program and still feel like you&rsquo;re back at square one, this isn&rsquo;t another thing to fail at. It&rsquo;s a supported, doable path back to feeling like yourself.</p>'
      '<ul class="ticks"><li>You feel overwhelmed and inconsistent</li><li>You&rsquo;re high-functioning but exhausted</li><li>You start strong, then life happens, then you&rsquo;re back at zero</li><li>You want change that actually lasts</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Start a conversation</a></div>')

  + split('Woman resting between movements, calm and unhurried',
      '<div class="kicker">Who it&rsquo;s not for</div><h2>An honest word.</h2>'
      '<p>This isn&rsquo;t a shred, a bootcamp, or a &ldquo;transform your body in 42 days&rdquo; challenge. There&rsquo;s no shame, no weigh-ins, no punishing yourself for the weekend.</p>'
      '<p>If you want to be shouted at into shape, we&rsquo;re not your people. If you&rsquo;re quietly exhausted and you want to feel steady, strong and like yourself again &mdash; without burning out to get there &mdash; you&rsquo;re exactly who we built this for.</p>',True)

  + sec(head('How it works','Six weeks, gently structured.',
      'Enough structure to hold you. Enough flexibility to fit a real life. You&rsquo;re not left to &ldquo;stay motivated&rdquo; on your own &mdash; you&rsquo;re carried through.')
    + feature_cards([
      ('Weeks 1&ndash;2','Settle &amp; steady',
        'We start by calming the system, not flogging it. Gentle movement, breath and simple wins to rebuild trust with your own body and prove to yourself that you can show up.',
        ['Find your baseline without judgement','Nervous-system tools you&rsquo;ll use for life','Small, doable habits that actually stick'],None),
      ('Weeks 3&ndash;4','Build &amp; strengthen',
        'As your body feels safer, we build. Strength and mobility grow, energy lifts, sleep often improves &mdash; and the habits start feeling like yours rather than a to-do list.',
        ['Progressive Pilates and yoga, scaled to you','Support for energy, sleep and cravings','Accountability so you don&rsquo;t drift'],None),
      ('Weeks 5&ndash;6','Embody &amp; carry it forward',
        'By now it&rsquo;s not a program you&rsquo;re doing &mdash; it&rsquo;s becoming how you live. We lock in what&rsquo;s working and map how you keep going, so week seven isn&rsquo;t a cliff-edge back to square one.',
        ['A rhythm you can actually maintain','Confidence that doesn&rsquo;t vanish at the end','A clear, unpressured next step'],None),
    ],highlight=-1),'ivory')

  + pullquote('&ldquo;You&rsquo;re not inconsistent. You&rsquo;ve been carrying too much, alone.&rdquo;','&mdash; New Dawn Wellness')

  + quotes([
      ('I joined to get back into health and fitness after a break. Unlike other programs, it had a tailored approach for each participant while still providing accountability and all the tools to get the most out of it.','&mdash; Sarah C. &middot; Consistency challenge'),
      ('Exercise, guidance, goals, mindfulness and prioritising ME. I cannot wait to begin the next challenge to continue reaching my goal of being a better version of myself.','&mdash; Stef P. &middot; Consistency challenge'),
    ])

  + faqs([
      ('I&rsquo;ve failed every program I&rsquo;ve tried. Why would this be different?','Because you were never the problem &mdash; the approach was. Most programs demand more discipline from a body that&rsquo;s already overwhelmed. We do the opposite: we support your nervous system first, so consistency becomes possible instead of forced. You&rsquo;re held the whole way through, not left to white-knuckle it alone.'),
      ('I&rsquo;m not fit. Can I keep up?','Yes. Everything is scaled to where you are on the day. You&rsquo;re not competing with anyone, and there&rsquo;s no &ldquo;behind.&rdquo; We meet your body where it is and build from there.'),
      ('How much time does it take each week?','Enough to matter, little enough to be doable inside a full life. We&rsquo;ll be clear about what each week involves so you can plan &mdash; and we build in flexibility for the weeks life gets loud.'),
      ('Is this just exercise, or something more?','Something more. Movement is the doorway, but the reset also includes nervous-system support, gentle nutrition guidance, sustainable habits and genuine accountability &mdash; the pieces most programs leave out.'),
      ('What happens after the six weeks?','You won&rsquo;t fall off a cliff. We map a clear, unpressured next step &mdash; whether that&rsquo;s ongoing classes or the Soul Mastery Sanctuary &mdash; so what you&rsquo;ve built keeps going.'),
    ])

  + sec('<div class="split">'
    + '<div><div class="kicker">What comes next</div><h2>Week seven is not a cliff edge.</h2>'
      '<p>Six weeks is long enough to feel genuinely different and short enough to finish. But most women tell us the same thing near the end: they do not want the support to stop.</p>'
      '<p>So the Soul Mastery Sanctuary is there. It is the ongoing version of what you have just built. A weekly place to land, a group of women doing the same work, and the deeper emotional and identity piece that six weeks only begins.</p>'
      '<ul class="ticks"><li>No pressure to continue, and no awkward sales conversation</li>'
      '<li>Monthly, cancel whenever it stops serving you</li>'
      '<li>Designed to follow the Reset, not repeat it</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="soul-mastery-sanctuary.html">See the Sanctuary</a>'
      '<a class="btn btn-ghost" href="membership.html">Or just keep coming to class</a></div></div>'
    + photofig('nd-circle.jpg','Women gathered in a circle at New Dawn Wellness','forest')
    + '</div>','cream')

  + cta_band('You don&rsquo;t need more discipline. You need the right support.',
      [('Enquire about the next intake','contact.html','btn-gold')],'navy'))

# ---- Heal: Flow & Glow Lymphatic Massage
W('flow-and-glow-massage.html','Flow &amp; Glow Lymphatic Massage | Cleveland QLD | New Dawn Wellness',
  'Flow &amp; Glow lymphatic massage in Cleveland QLD. Gentle, rhythmic massage to ease puffiness, fatigue and that heavy, congested feeling. Held privately, by appointment.',
  hero_split('Heal','Flow &amp; Glow Lymphatic Massage.',
    'Gentle, rhythmic massage that supports your lymphatic system, easing puffiness, fatigue and that heavy, congested feeling. You leave lighter, clearer, and considerably more yourself.',
    [('Book a session','contact.html','btn-gold')],
    'Warm, candlelit treatment room in soft afternoon light','olive',
    cred='90 minutes &middot; Private studio in Cleveland &middot; Pay after your session',
    photo='nd-massage-room.jpg')
  + sec(head('Why lymphatic work','Your body has been keeping score.',
      'Your lymphatic system is how your body clears what it no longer needs. It has no pump of its own, so it relies on movement and breath, and when you&rsquo;ve been stressed, still and holding everything together, it slows. That&rsquo;s the heaviness. That&rsquo;s the puffiness and the fatigue that sleep doesn&rsquo;t fix.')
    + cards([
      ('Lighter, less puffy','Gentle rhythmic work encourages fluid to move, easing swelling in the face, hands, legs and belly.',''),
      ('Deeply calming','The slow, repetitive pressure is a direct signal to the nervous system that it&rsquo;s safe to let go.',''),
      ('Less heaviness','That congested, sluggish feeling begins to lift, often within a day or two.',''),
      ('Better sleep','Most women tell us they sleep unusually well the night of their session.',''),
    ]),'cream')
  + split('Treatment table dressed for a session, warm light therapy',
      '<div class="kicker">What a session is like</div><h2>Somewhere you don&rsquo;t have to hold anything.</h2>'
      '<p>You spend your days holding everyone and everything. This is the opposite. An hour and a half where you&rsquo;re the one being held.</p>'
      '<p>We talk briefly about how you&rsquo;ve been feeling and anything your body is dealing with. Then you get comfortable, warm and covered, and the room goes quiet. The pressure is light and rhythmic, nothing deep or painful. Many women drift off entirely.</p>'
      '<p>Afterwards, water, and no rush to be anywhere.</p>',
      True,photo='nd-redlight-table.jpg')
  + sec(head('Also available','Other hands-on sessions.',
      'Not sure which your body needs? Start with a conversation and we&rsquo;ll find it together.')
    + cards([
      ('Flow &amp; Glow Lymphatic Massage','Gentle, rhythmic lymphatic work to ease puffiness, fatigue and heaviness.','$130'),
      ('Indian Head &amp; Shoulder Massage with Hot Stones','Deep release for the head, neck and shoulders, where so much stress quietly lives. Warm stones melt the tension and drop your whole system into calm.','$[ TBC ]'),
      ('Soul Restore Reiki','A deeply restful energy healing session to settle an overstretched nervous system.','$[ TBC ]'),
      ('Cosmic Breathwork','Guided breath to move stuck energy and emotion, quiet the mind and bring you back into your body.','$[ TBC ]'),
    ]),'ivory')
  + pullquote('&ldquo;You don&rsquo;t have to earn rest. Your body has been asking for it all along.&rdquo;','Dawn Edwards-Jones')
  + quotes([
      ('From the moment I walked in, her calm and nurturing energy made me feel completely safe and held. I left feeling lighter, clearer and deeply relaxed.','Mel T. &middot; Lymphatic massage'),
      ('I felt lighter, standing taller and in less pain. Dawn is an incredibly intuitive and caring healer.','Donna H. &middot; Lymphatic massage'),
      ('I&rsquo;ve had many therapies over the years and can&rsquo;t recommend Dawn highly enough. If you feel the emotional weight is dragging you down, you deserve an hour with Dawn.','Kiran &middot; Massage &amp; energy healing'),
    ])
  + faqs([
      ('Where are sessions held?','At a quiet private studio in Cleveland, by appointment. The exact address is shared with you once your booking is confirmed, so your session stays undisturbed.'),
      ('Does it hurt?','No. Lymphatic work is light and rhythmic, closer to a slow stroke than a deep massage. If anything is uncomfortable, say so and we change it.'),
      ('Do I pay upfront?','No. You book a time and pay after your session.'),
      ('How will I feel afterwards?','Usually lighter and quite sleepy. Drink plenty of water, and don&rsquo;t schedule anything demanding straight after if you can avoid it.'),
      ('How often should I come?','It depends on what&rsquo;s going on for you. Some women come once when they feel congested, others monthly as ongoing support. We&rsquo;ll talk honestly about what you actually need.'),
      ('Is there anyone it isn&rsquo;t suitable for?','There are some conditions where lymphatic work isn&rsquo;t appropriate, so please tell us about your health history when you book and we&rsquo;ll let you know. If in doubt, check with your doctor first.'),
    ])
  + cta_band('An hour and a half where nothing is asked of you.',
      [('Book your session','contact.html','btn-gold'),('Explore Soul Restore Reiki','soul-restore-reiki.html','btn-ghost')],'navy'))

# ---- Heal: Soul Restore Reiki
W('soul-restore-reiki.html','Soul Restore Reiki | Energy Healing in Cleveland QLD | New Dawn Wellness',
  'Soul Restore Reiki in Cleveland QLD. A deeply restful energy healing session to settle an overstretched nervous system and help you feel gathered and whole again.',
  hero_split('Heal','Soul Restore Reiki.',
    'A deeply restful energy healing session to settle an overstretched nervous system, restore balance, and help you feel gathered and whole again. You do nothing at all. That&rsquo;s rather the point.',
    [('Book a session','contact.html','btn-gold')],
    'Candlelit private healing room, hands resting gently','burgundy',
    cred='Fully clothed &middot; Private studio in Cleveland &middot; Nothing required of you',
    photo='nd-redlight-table.jpg')
  + split('Woman resting fully clothed on a treatment table, deeply at ease',
      '<div class="kicker">What it is</div><h2>Rest, at a depth sleep doesn&rsquo;t always reach.</h2>'
      '<p>Reiki is gentle energy healing. You stay fully clothed and simply lie down, warm and covered, while Dawn works with light touch or hands held just above the body. There&rsquo;s nothing to do, nothing to understand and nothing to get right.</p>'
      '<p>What most women notice is how quickly the mind stops arguing. The breath drops lower. The jaw unclenches. Shoulders that have been up around the ears for weeks finally come down.</p>'
      '<p>Some women see colours, some feel warmth or tingling, some fall asleep, and some simply rest more deeply than they have in months. All of it is fine.</p>',
      True,photo='studio2-soundhealing.jpg')
  + sec(head('What it helps with','When your system has been running too hot.',
      'Reiki isn&rsquo;t a fix for anything. It&rsquo;s support, and it&rsquo;s particularly good support for a nervous system that has forgotten how to downshift.')
    + cards([
      ('Overwhelm','When everything feels like too much and you can&rsquo;t work out why.',''),
      ('Sleep that doesn&rsquo;t restore','When you sleep and wake up just as tired.',''),
      ('Emotional heaviness','Grief, worry or a weight you can&rsquo;t quite name or talk your way out of.',''),
      ('Burnout and depletion','When you&rsquo;ve been running on empty for so long it feels normal.',''),
      ('Big transitions','Menopause, loss, separation, a life that&rsquo;s changing shape around you.',''),
      ('Nothing in particular','You don&rsquo;t need a reason. Wanting an hour of deep rest is reason enough.',''),
    ]),'cream')
  + pullquote('&ldquo;Stillness can feel unfamiliar. That doesn&rsquo;t mean you don&rsquo;t need it.&rdquo;','Dawn Edwards-Jones')
  + quotes([
      ('I felt held in a safe, supportive space where I could fully relax and let go. I left feeling calm, grounded and deeply restored, and I slept so well afterwards.','Cate N. &middot; Restorative session'),
      ('A beautiful, transformative experience. I left feeling lighter, like a weight had been lifted and my body was flowing again.','Jorja Z. &middot; Healing session'),
      ('Dawn is an incredibly intuitive and caring healer.','Donna H. &middot; Healing session'),
    ])
  + faqs([
      ('Do I need to believe in it for it to work?','No. Plenty of women arrive sceptical and leave very relaxed. You don&rsquo;t have to believe anything or adopt any view. You just have to lie down.'),
      ('Do I get undressed?','No. You stay fully clothed. Wear something comfortable and warm.'),
      ('What if I fall asleep?','Then you needed the sleep. It happens often and it&rsquo;s completely fine.'),
      ('What if I feel emotional?','That happens too, and you&rsquo;re safe to. Sometimes when the body finally relaxes, something that has been held for a long time moves. You&rsquo;ll be supported, not rushed.'),
      ('Where are sessions held?','At a quiet private studio in Cleveland, by appointment. The address is shared with you once your booking is confirmed.'),
      ('How is this different from massage?','Massage works with the physical tissue and fluid. Reiki works more with your energy and your nervous system, with little or no pressure. If your body is sore and heavy, start with Flow &amp; Glow. If you&rsquo;re wired, frazzled and can&rsquo;t switch off, start here.'),
    ])
  + cta_band('You don&rsquo;t have to earn rest.',
      [('Book your session','contact.html','btn-gold'),('Explore Flow &amp; Glow Massage','flow-and-glow-massage.html','btn-ghost')],'navy'))

# ---- Hypnotherapy
# ---- The Adawning Experience (hypnotherapy + personalised recording, in person)
W('adawning-experience.html','The Adawning Experience&trade; | Personalised Hypnotherapy in Cleveland QLD',
  'The Adawning Experience&trade; &mdash; a personalised, in-person hypnotherapy session in Cleveland, QLD, crafted around you. You leave with your own 90-minute recording to return to again and again.',
  hero('Heal','The Adawning Experience&trade;',
    'A deeply personal, in-person hypnotherapy session &mdash; gentle guided work with the subconscious to soften old patterns of stress, self-doubt and racing thoughts. And you don&rsquo;t leave it in the room: you take home your own recording, crafted around you, to return to whenever you need it.',
    [('Book a single session','contact.html','btn-gold'),('Explore the 4-session journey','contact.html','btn-ghost')])
  + split('Woman resting deeply in a calm, candlelit private studio',
      '<div class="kicker">What it is</div><h2>Hypnotherapy, made just for you.</h2>'
      '<p>This is gentle, guided hypnotherapy that works with your subconscious to ease the patterns that keep you wired, tired and lying awake &mdash; stress, self-doubt, habits that no longer serve you. You stay aware and in control the whole time. It&rsquo;s closer to a deeply relaxed, supported rest where your mind becomes open to new, kinder patterns.</p>'
      '<p>Sessions are held privately and in person, by appointment, in a quiet home studio &mdash; so you can truly let go.</p>')
  + sec(head('How it works','In person with Dawn &mdash; then yours to keep.')
    + cards([
      ('1. We meet &amp; listen','A gentle conversation, in person, to understand what you want to shift and how you want to feel.',''),
      ('2. We do the work','Your personalised 90-minute hypnotherapy session, guided by Dawn and built around your name and intentions.',''),
      ('3. You take it home','You leave with your own recording of the session &mdash; so you can return to that calm, receptive state again and again.',''),
    ]),'cream')
  + split('Woman listening to her recording at home, calm and settled',
      '<div class="kicker">Why the recording matters</div><h2>The change keeps working after you leave.</h2>'
      '<p>One session softens things. Repetition is how the nervous system actually learns a new normal. That&rsquo;s why the in-person experience comes with your own recording to keep &mdash; not a generic app track, but the exact session made for you, in your session, around your intentions.</p>'
      '<p>It&rsquo;s yours for life. No subscription, no expiry. Something to come back to every time life gets loud.</p>',True)
  + sec(head('Options','Choose your depth.',
      'Every option is an in-person session with Dawn, and you take home the recording each time.')
    + cards([
      ('Single Session','One fully personalised in-person hypnotherapy session, built around your name and intentions &mdash; you leave with your 90-minute recording to keep and replay for as long as you need it.','$249'),
      ('4-Session Journey','Four in-person sessions that build week to week, each with its own recording, so a new, calmer normal has time to truly settle. Our deepest, most lasting work &mdash; and the best value per session.','$897'),
    ]))
  + faqs([
      ('Is this in person or a recording?','Both, in the best way. The session itself is in person with Dawn in a quiet private studio. Afterwards, you take home your own recording of it &mdash; so the work continues long after you leave the room.'),
      ('What actually happens in a session?','You settle in, we talk about what you want to shift, and then Dawn guides you into a deeply relaxed state and gently works with the subconscious. You stay aware and in control throughout &mdash; it feels like a supported, restful drift, not anything dramatic.'),
      ('Is it safe?','Yes. Hypnotherapy of this kind is deeply relaxing and completely safe. You remain in control the whole time and simply drift into a calm, receptive state.'),
      ('How often should I listen to my recording?','As often as you like. Many women listen daily to begin with &mdash; repetition is what helps the new patterns settle.'),
    ])
  + quotes([
      ('I was feeling tense with the weight of the world on my shoulders. Dawn helped me feel lighter and significantly calmer since the session. She is kind, gentle and very intuitive.','&mdash; Angela N. &middot; The Adawning Experience'),
      ('The session relaxed me so much. It felt like yoga meditation but took you deeper. Dawn understood what my body needed and helped me let go of unwanted emotions.','&mdash; Di G. &middot; The Adawning Experience'),
    ])
  + cta_band('Something you can come back to, every time life gets loud.',
      [('Enquire now','contact.html','btn-gold')],'navy'))

# ---- Wellness Events
W('wellness-events.html','Wellness Events &amp; Workshops | New Dawn Wellness',
  'Breathwork, women&rsquo;s circles, yin &amp; pins, menopause workshops and webinars at New Dawn Wellness, Cleveland QLD. Experiential events to reconnect and reset.',
  hero_split('Gather','Wellness Events.',
    'Come together for breath, stillness, learning and connection. Our events are experiences &mdash; not lectures &mdash; designed to leave you lighter than you arrived.',
    [('Enquire about upcoming events','contact.html','btn-gold')],
    'A New Dawn sound bath &mdash; women in savasana, crystal bowls at the centre','gold',
    photo='nd-sound-healing.jpg')
  + sec(head('What we run','A rhythm of gatherings.')
    + cards([
      ('Breathwork Journeys','Guided breath sessions to release, reset and feel deeply.',''),
      ('Women&rsquo;s Circles','A safe, held space to share, exhale and belong.',''),
      ('Menopause Workshops','Practical, compassionate sessions on navigating the change.',''),
      ('Yin &amp; Pins','Deep stretch and acupressure for full nervous-system release.',''),
      ('Sound Baths','Immersive sound to drop you into deep rest.',''),
      ('Webinars','Online sessions you can join from anywhere.',''),
    ]),'cream')
  + split('Women gathered in a warm, candlelit circle',
      '<div class="kicker">What to expect</div><h2>Experiences, not lectures.</h2>'
      '<p>Every gathering is designed to be felt in the body &mdash; not just understood in the head. You&rsquo;ll be warmly welcomed, gently guided, and given full permission to arrive exactly as you are. No experience needed, nothing to perform.</p>'
      '<ul class="ticks"><li>Small, intimate groups</li><li>Warm, expert facilitation</li><li>A safe space to exhale and belong</li><li>A gentle next step &mdash; never a hard sell</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Ask what&rsquo;s coming up</a></div>',
      photo='nd-circle.jpg')
  + pullquote('&ldquo;You don&rsquo;t need to do more. You need space to come back to yourself.&rdquo;','&mdash; New Dawn Wellness')
  + quotes([
      ('The breathwork and sound healing was profound &mdash; I didn&rsquo;t realise how much I was holding until I let it go. I left feeling lighter than I have in months.','&mdash; Debbie B. &middot; Breathwork &amp; sound'),
      ('The yin yoga and sound evening was pure magic. Beautifully held, deeply relaxing &mdash; exactly the reset I needed.','&mdash; Janette C. &middot; Yin &amp; sound'),
      ('Dawn&rsquo;s workshops are warm, grounded and genuinely useful. You leave feeling seen and with real tools, not just theory.','&mdash; Jodie H. &middot; Workshop'),
    ])
  + cta_band('Every event leads somewhere &mdash; a next gentle step, never a hard sell.',
      [('Join the next one','contact.html','btn-gold'),('See our retreats','retreats.html','btn-ghost')],'navy')
  + crosslink('Looking for a deeper reset?','retreats.html','Explore our retreats &rarr;'))

# ---- Retreats
W('retreats.html','Retreats &amp; Day Immersions | New Dawn Wellness',
  'Day immersions and longer wellness retreats with New Dawn. Movement, breath, healing and rest &mdash; a full reset for women who never truly switch off.',
  hero_split('Retreat','Fully switch off.',
    'For the woman who never stops. Our retreats and day immersions give you permission to put everything down and remember what calm feels like in your body.',
    [('Register your interest','contact.html','btn-gold')],
    'Dawn leading a retreat &mdash; arms open, women gathered behind','gold',
    photo='nd-dawn-leading.jpg')
  + split('Peaceful retreat setting, women resting',
      '<div class="kicker">The experience</div><h2>A reset for your whole system.</h2>'
      '<p>Woven from movement, breathwork, healing, nourishment and genuine rest, each retreat is paced to unwind you slowly &mdash; no rushing, no agenda to keep up with.</p>'
      '<ul class="ticks"><li>Gentle movement and breath</li><li>Sound healing and deep rest</li><li>Nourishing food and real connection</li><li>Space to hear yourself think again</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Ask about the next retreat</a></div>',
      photo='supported-women.jpg')
  + quotes([
      ('A beautiful day to pause, reset and step away from the busy-ness of everyday life &mdash; thoughtfully facilitated in a warm, supportive space held by women, for women. I left feeling calmer, more grounded and very grateful.','&mdash; Cynthia E. &middot; Day retreat'),
      ('One of the best retreats I&rsquo;ve been to &mdash; a great combination of learning, stimulation and restful moments. The environment was stunning and Dawn nurtured each one of us.','&mdash; Elizabeth M. &middot; Pilates &amp; Yoga retreat'),
    ])
  + cta_band('You&rsquo;re allowed to stop. We&rsquo;ll hold the space.',
      [('Register your interest','contact.html','btn-gold')],'navy'))

# ---- Soul Mastery Sanctuary
W('soul-mastery-sanctuary.html','Soul Mastery Sanctuary | Group Coaching | New Dawn Wellness',
  'Soul Mastery Sanctuary &mdash; ongoing group coaching and community from New Dawn Wellness. Emotional, identity and nervous-system work with weekly support.',
  hero('Soul Mastery Sanctuary &middot; Group coaching &amp; community',
    'The deeper work &mdash; and you&rsquo;re not doing it alone.',
    'For the woman who&rsquo;s done the surface work and can feel there&rsquo;s something underneath it. An ongoing membership of emotional, identity and nervous-system work, with a circle of women beside you week after week. This is where insight stops being a nice idea and becomes who you are.',
    [('Step inside','contact.html','btn-gold')])
  + sec(head('What&rsquo;s inside','Weekly support that holds.')
    + cards([
      ('Emotional &amp; identity work','Go beneath the habits to who you&rsquo;re becoming.',''),
      ('Nervous-system tools','Practices to keep coming back to safety and steadiness.',''),
      ('Weekly recalibration','Regular sessions to keep you resourced and on track.',''),
      ('Community','Continuity and belonging &mdash; you&rsquo;re not doing this alone.',''),
    ]),'cream')
  + split('Women connecting in a warm circle',
      '<div class="kicker">Who it&rsquo;s for</div><h2>Transformation isn&rsquo;t a one-off.</h2>'
      '<p>Real change needs continuity. The Sanctuary is where the insights from a class or event become who you are &mdash; supported, week after week, at a pace that feels human.</p>'
      '<p>It&rsquo;s for you if you&rsquo;ve done the surface work and know there&rsquo;s something deeper to tend to &mdash; and you&rsquo;re ready to be held while you do. It&rsquo;s not a quick fix or a course to complete; it&rsquo;s ongoing support for the long game.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Enquire about membership</a></div>')
  + crosslink('Ready for deeper, 1:1 work with Dawn?','https://dawnedwards-jones.com/soul-mastery-ascension.html','Discover Soul Mastery Ascension &rarr;'))

# ---- Nutrition
W('nutrition.html','Nutrition Support | New Dawn Wellness',
  'Gentle nutrition support at New Dawn Wellness &mdash; cellular and whole-body support for energy, sleep, cravings and hormones. Support, never restriction.',
  hero('Nourish','Nutrition Support.',
    'Not another diet. Gentle, body-first support for energy, sleep, cravings and hormones &mdash; so you feel resourced rather than depleted.',
    [('Enquire','contact.html','btn-gold')])
  + split('Simple, nourishing whole foods',
      '<div class="kicker">Our approach</div><h2>Support your body, not shrink it.</h2>'
      '<p>We focus on what your body needs to feel steady and energised &mdash; blood sugar, sleep, stress and simple nourishment &mdash; woven into real life. No rigid rules, no shame.</p>'
      '<ul class="ticks"><li>Energy and sleep support</li><li>Craving and blood-sugar balance</li><li>Hormone-friendly nourishment</li><li>Simple, sustainable habits</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Book a chat</a></div>')
  + crosslink('Nutrition works beautifully alongside the 6-Week Reset.','6-week-reset.html','See the 6-Week Reset &rarr;'))

# ---- Menopause Support
W('menopause-support.html','Menopause Support &amp; Coaching | New Dawn Wellness',
  'Compassionate menopause support at New Dawn Wellness &mdash; movement, nervous-system care, nutrition and coaching to help you navigate the change and feel like yourself.',
  hero('Support','Menopause Support.',
    'It&rsquo;s not just hormones &mdash; it&rsquo;s stress, load and a lack of support. We help you navigate menopause with movement, nervous-system care and real understanding.',
    [('Enquire','contact.html','btn-gold')])
  + sec(head('How we help','Whole-woman menopause care.')
    + cards([
      ('Movement','Strength and mobility work that respects a changing body.',''),
      ('Nervous-system support','Tools for the anxiety, overwhelm and sleep disruption.',''),
      ('Nutrition','Gentle guidance for energy, weight and hormonal balance.',''),
      ('Coaching &amp; community','Space to feel understood and supported, not dismissed.',''),
    ]),'cream')
  + cta_band('You&rsquo;re not losing yourself. You&rsquo;re being asked to meet yourself anew.',
      [('Reach out','contact.html','btn-gold')],'navy')
  + crosslink('Are you an employer wanting to support women through menopause?','https://dawnedwards-jones.com/menopause-policy.html','See workplace menopause advisory &rarr;'))

# ================================================================ RESOURCES
# TODO before go-live: replace SPOTIFY_URL with the real Adawning podcast link.
SPOTIFY_URL = '#spotify-link-tbc'

# ---- Podcast
W('podcast.html','The Adawning Podcast | New Dawn Wellness, Cleveland QLD',
  'The Adawning podcast with Dawn Edwards-Jones. Grounded conversations on the nervous system, menopause, self-leadership and coming home to yourself. Listen on Spotify.',
  hero('Listen','The Adawning Podcast.',
    'Honest conversations about the nervous system, menopause, overwhelm and what it actually takes to stop abandoning yourself. No hype, no fixing. Just real talk.',
    [('Listen on Spotify',SPOTIFY_URL,'btn-gold')])
  + split('Dawn recording the podcast, headphones on',
      '<div class="kicker">About the show</div><h2>Part insight, part permission slip.</h2>'
      '<p>Every episode is a conversation rather than a lecture. Some weeks it is nervous-system science. Some weeks it is lived experience, menopause, motherhood or the quiet exhaustion of holding everything together. Always something you can take into your week.</p>'
      '<p>Search &ldquo;The Adawning&rdquo; wherever you listen, or press play on Spotify below.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="'+SPOTIFY_URL+'">Listen on Spotify</a>'
      '<a class="btn btn-ghost" href="articles.html">Read the articles</a></div>',
      photo='nd-dawn-podcast.jpg')
  + sec(head('What you will hear','Topics we come back to.')
    + cards([
      ('The nervous system','Why your body keeps choosing survival mode, and how safety changes everything.',''),
      ('Menopause, honestly','The bit nobody prepared you for. Sleep, rage, brain fog, identity.',''),
      ('Self-leadership','Making decisions from calm instead of from pressure.',''),
      ('Real women, real stories','Guests who stopped performing and started telling the truth.',''),
    ]),'cream')
  + pullquote('You are not inconsistent. You have been trying to do all of it alone.')
  + cta_band('Press play, then come and sit in the room with us.',
      [('Listen on Spotify',SPOTIFY_URL,'btn-gold'),('See what we offer','index.html','btn-ghost')],'navy')
  + crosslink('Want Dawn on your stage or your podcast?',DEJ_URL+'/speaking.html','Speaking and media &rarr;'))

# ---- Articles
W('articles.html','Articles | Pilates, Yoga, Menopause &amp; Nervous System | New Dawn Wellness',
  'Articles from New Dawn Wellness in Cleveland, QLD. Practical reading on Pilates, yoga, menopause, the nervous system, lymphatic health and feeling like yourself again.',
  hero('Read','Articles.',
    'Plain-language reading on movement, menopause, the nervous system and the things women ask us most. Written to be useful, not to impress anyone.',
    [('Browse topics','#topics','btn-gold'),('Listen to the podcast','podcast.html','btn-ghost')])
  + sec('<a id="topics"></a>' + head('Browse by topic','Start where you are.')
    + cards_link([
      ('Pilates &amp; movement','How Pilates actually works for a body that is tired, sore or starting over after a long break.','pilates-yoga.html','Pilates and yoga &rarr;'),
      ('Menopause &amp; hormones','Sleep, weight, anxiety, brain fog and why it is rarely just hormones on their own.','menopause-support.html','Menopause support &rarr;'),
      ('The nervous system','Why rest feels impossible, what regulation really means, and how to build it in small doses.','soul-mastery-sanctuary.html','Soul Mastery Sanctuary &rarr;'),
      ('Lymphatic &amp; recovery','Puffiness, heaviness and fatigue, and what gentle lymphatic work does about it.','flow-and-glow-massage.html','Flow &amp; Glow massage &rarr;'),
      ('Nutrition &amp; energy','Blood sugar, cravings and energy, without a single rule about what you cannot eat.','nutrition.html','Nutrition support &rarr;'),
      ('Consistency &amp; habits','Why you keep starting over, and the support that finally makes it stick.','6-week-reset.html','The 6-Week Reset &rarr;'),
    ]),'cream')
  # TODO before go-live: replace the placeholder cards below with real published articles.
  + sec(head('Latest','Recent reading.')
    + cards([
      ('[ Article title ]','[ One or two sentences summarising the article. Add the published date and a link once the post is live. ]',''),
      ('[ Article title ]','[ One or two sentences summarising the article. Add the published date and a link once the post is live. ]',''),
      ('[ Article title ]','[ One or two sentences summarising the article. Add the published date and a link once the post is live. ]',''),
    ]))
  + optin('Free resource','The 3-Minute Nervous System Reset.',
      'A short, simple practice you can do in the car, at your desk or before you walk back in the door. No app, no equipment, nothing to download and forget about.',
      'Send it to me','We will email you occasionally. Unsubscribe any time.')
  + crosslink('Prefer to listen rather than read?','podcast.html','The Adawning Podcast &rarr;'))

# ---- Free Resources
W('free-resources.html','Free Resources | Meditations, Guides &amp; Practices | New Dawn Wellness',
  'Free resources from New Dawn Wellness. Guided meditations, breathwork practices, the 3-Minute Nervous System Reset and simple guides for women who are carrying a lot.',
  hero('Free','Start here, free.',
    'Small, usable things that help your body settle. Take what you need. Nothing here asks you to do more than you already are.',
    [('Get the Nervous System Reset','#reset','btn-gold')])
  + sec('<a id="reset"></a>'
    + '<div class="split">'
    + '<div><div class="kicker">Most popular</div><h2>The 3-Minute Nervous System Reset.</h2>'
      '<p>Three minutes. No app, no mat, nobody watching. A simple sequence of breath and attention that tells your body it is safe to come down out of survival mode.</p>'
      '<p>Use it in the car before you walk inside. Use it at 3pm when everything feels loud. Use it at 2am when your brain will not stop.</p>'
      '<ul class="ticks"><li>Three minutes, start to finish</li><li>Nothing to buy, nothing to set up</li>'
      '<li>Works sitting down, fully clothed, anywhere</li><li>Yours to keep</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="#signup">Send it to me</a></div></div>'
    + photofig('nd-circle.jpg','Women sitting in a circle at New Dawn Wellness','forest')
    + '</div>','cream')
  # TODO before go-live: wire each resource below to its Tekmatix form and delivery automation.
  + sec(head('More to take with you','Free practices and guides.')
    + cards([
      ('Guided meditations','Short recordings for sleep, overwhelm and coming back to your body. [ Tekmatix form slot ]',''),
      ('Breathwork practices','Simple breath patterns for when you are wired, flat or somewhere in between. [ Tekmatix form slot ]',''),
      ('[ Guide title ]','[ Short description of the guide or checklist. Tekmatix form slot. ]',''),
      ('[ Quiz or checklist ]','[ Short description. Tekmatix form slot. ]',''),
    ]))
  + pullquote('Stillness can feel unfamiliar. That does not mean you do not need it.')
  + sec('<a id="signup"></a>'
    + head('Get it now','Where should we send it?')
    # TODO before go-live: replace with the live Tekmatix embed form.
    + '<p style="max-width:640px;margin:0 auto;text-align:center">[ Tekmatix opt-in form embed goes here. '
      'Fields: first name, email. Tag: free-resource-nervous-system-reset. ]</p>','forest')
  + cta_band('When you are ready for more than three minutes, we are here.',
      [('See our classes','timetable.html','btn-gold'),('Explore the 6-Week Reset','6-week-reset.html','btn-ghost')],'navy')
  + crosslink('There is a whole room of women doing this alongside you.','soul-mastery-sanctuary.html','Soul Mastery Sanctuary &rarr;'))

# ---- Contact
W('contact.html','Contact New Dawn Wellness | Cleveland QLD',
  'Get in touch with New Dawn Wellness in Cleveland, QLD. Book a class, ask about programs, events or healing sessions. Phone, email and studio location.',
  hero('Say hello','Let&rsquo;s talk.',
    'Whether you&rsquo;re ready to book or just have a question, we&rsquo;d love to hear from you. There&rsquo;s no pressure here &mdash; only a warm welcome.',
    [('Email us','mailto:'+EMAIL,'btn-gold')])
  + sec('<div class="split">'
      + '<div><div class="kicker">Get in touch</div><h2>We&rsquo;re here.</h2>'
        '<ul class="ticks"><li>Studio: '+ADDRESS+'</li><li>Phone: '+PHONE+'</li><li>Email: '+EMAIL+'</li></ul>'
        '<p style="margin-top:14px">Hands-on healing sessions are held at a private studio &mdash; the address is shared when you book.</p>'
        '<div class="btn-row"><a class="btn btn-gold" href="timetable.html">Book a class</a><a class="btn btn-ghost" href="mailto:'+EMAIL+'">Email us</a></div></div>'
      + imgph('Warm welcome at the studio door')
      + '</div>')
  + enquiry_form('Send a message','Tell us what you need.',
      'Not sure which class, program or session is right for you? Write a few lines and we will point you '
      'in the right direction. No sales pitch, just a straight answer.',
      ['I am not sure yet, please guide me','Booking a class','Membership and class passes',
       'The 6 Week Reset','Soul Mastery Sanctuary','Flow &amp; Glow lymphatic massage',
       'Soul Restore Reiki','The Adawning Experience','Breathwork','Events and retreats',
       'Menopause support','Nutrition support','Something else'],
      'Send my message','website-contact-ndw'))

# ---- Privacy
W('privacy.html','Privacy Policy | New Dawn Wellness',
  'How New Dawn Wellness collects, uses, stores and protects your personal information, and how to access or correct it.',
  privacy_body('New Dawn Wellness','newdawnwellness.health',True))

# ---- Terms
W('terms.html','Terms &amp; Conditions | New Dawn Wellness',
  'The terms that apply when you book a class, program, event or session with New Dawn Wellness in Cleveland, QLD.',
  terms_body('New Dawn Wellness','newdawnwellness.health',True))

# ---- FAQ
W('faq.html','FAQ | New Dawn Wellness',
  'Frequently asked questions about New Dawn Wellness &mdash; classes, bookings, what to bring, healing sessions and programs in Cleveland, QLD.',
  hero('Questions','Good to know.',
    'The things women most often ask before their first visit. Can&rsquo;t find your answer? Just reach out &mdash; we&rsquo;re happy to help.',
    [('Contact us','contact.html','btn-gold')])
  + faqs([
      ('I&rsquo;m a total beginner &mdash; is that okay?','Absolutely. Our classes are designed for real bodies at every stage. You&rsquo;ll always be guided and never pushed beyond what feels right for you.'),
      ('What should I bring?','Just water and comfortable clothing you can move in. Mats and props are provided. Arrive ten minutes early for your first class.'),
      ('Do you offer online options?','Yes &mdash; alongside in-studio classes we run webinars and online support so you can join from anywhere.'),
      ('Where are massage, reiki and hypnosis sessions held?','Flow &amp; Glow lymphatic massage, Soul Restore Reiki and The Adawning Experience are held in a private studio. The address is shared with you when you book.'),
      ('How do I book?','Contact us and we&rsquo;ll get you set up in our booking system and send through the current timetable.'),
    ]))

print("wellness pages:", len(NDW_PAGES))

# ================================================================ DEJ PAGES
LOGOS=[('redland-city-council.svg','Redland City Council'),('qnmu-logo.png','Queensland Nurses &amp; Midwives&rsquo; Union'),
  ('faith-lutheran.png','Faith Lutheran College'),('corporate-protection.svg','Corporate Protection Australia'),
  ('redland-art-gallery.png','Redland Art Gallery'),('maybanke.png','Maybanke Association'),
  ('kensho-pilates.png','Kensho Boutique Pilates'),('ubx-birkdale.svg','UBX Birkdale'),
  ('bayside-women-in-business.png','Bayside Women in Business')]
def logo_row():
    imgs=''.join('<img src="logos/%s" alt="%s logo">'%(f,esc(a)) for f,a in LOGOS)
    return ('<section class="sec cream"><div class="wrap trusted"><div class="label">Trusted to speak &amp; work with</div>'
      '<div class="logo-row">%s</div></div></section>')%imgs

DEJ_PAGES=[]
def D(slug,title,desc,body): DEJ_PAGES.append((slug,title,desc,body))

# ---- Home
D('index.html','Dawn Edwards-Jones | Keynote Speaker, Author &amp; Self-Leadership Coach',
  'Dawn Edwards-Jones &mdash; keynote speaker, author and self-leadership coach. Bringing calm, embodied leadership to women, workplaces and organisations across Australia.',
  hero_split('Author &middot; Speaker &middot; Coach',
    'From overwhelm to <em>calm, embodied leadership.</em>',
    'If you&rsquo;re navigating menopause, stress or burnout &mdash; holding everything together while running on empty &mdash; I help you move out of survival mode and into steady, self-led calm. For women, and the organisations they work in.',
    [('Bring Dawn to your event','contact.html','btn-gold'),('Work with me 1:1','soul-mastery-ascension.html','btn-ghost')],
    'Dawn Edwards-Jones at home &mdash; warm, grounded, present.','burgundy',
    cred='Keynotes &middot; Corporate wellbeing &middot; 1:1 coaching &middot; The Adawning',
    photo='dawn-couch-relaxed.jpg',pos='center top')
  + trust_strip('Loved by clients &amp; audiences',
      'Dawn has an incredible gift for holding space. I left completely reset.',
      '&mdash; Angela N.',
      '30 years in leadership<br>16+ retreats led')
  + logo_row()
  + sec(head('Ways to work with me','Three ways in &mdash; wherever you&rsquo;re starting.',
      'Whether you&rsquo;re booking a stage, looking for ongoing support, or ready to go all in privately &mdash; there&rsquo;s a door here for you.')
    + cards_link([
      ('Bring Dawn to your event','<strong>For</strong> conferences, workplaces and women&rsquo;s events wanting a warm, grounded keynote or workshop.','speaking.html','See speaking'),
      ('Soul Mastery Sanctuary &mdash; Group','<strong>For</strong> women who want ongoing coaching and community, week after week.','https://newdawnwellness.health/soul-mastery-sanctuary.html','Join the group'),
      ('Soul Mastery Ascension &mdash; 1:1','<strong>For</strong> women ready for private, premium transformation with close proximity to Dawn.','soul-mastery-ascension.html','Work 1:1'),
    ]),'beige')
  + sec(head('Why this matters','Why women are running on empty.','')
    + manifesto([
      ('For years, women have been told the problem is them.',''),
      ('Push harder. Be more disciplined. Manage your time better. Build more resilience. Wake earlier. Meditate longer. Take another course. Read another book.','list'),
      ('But what if you were never the problem?',''),
      ('What if you&rsquo;ve simply become an expert at <em>surviving</em> &mdash; holding the family together, leading the team, building the business, caring for ageing parents, carrying everyone around you&hellip;',''),
      ('&hellip;while quietly abandoning yourself?',''),
      ('This is the work I care about most: helping women stop surviving &mdash; and start leading themselves from calm.','small'),
    ])
    + '<div class="cta-band" style="margin-top:14px"><div class="btn-row" style="justify-content:center"><a class="btn btn-gold" href="philosophy.html">Read what we believe &rarr;</a></div></div>','ivory')
  + sec(head('Why Dawn','Everything I teach, I have first lived.','')
    + '<div class="split">' + photofig('dawn-cup-stillness.jpg','Portrait of Dawn Edwards-Jones, holding a cup in a moment of stillness','forest','center top')
    + '<div><p class="lead" style="font-size:1.18rem">I spent 30 years in the corporate world before wellness &mdash; leadership roles across Deloitte, KPMG, government and universities &mdash; quietly holding everything together while running on empty.</p>'
      '<p>I know grief in my bones. I went from being a wife to a widow overnight, and I had to rebuild my life from the ground up. I later emigrated from Wales to Australia with my husband and three children, built businesses as an entrepreneur, and moved through trauma and menopause burnout along the way &mdash; the kind no amount of discipline fixes.</p>'
      '<p>What changed everything was learning to regulate my nervous system, come home to my body and lead from safety instead of force. Today I bring that lived experience to stages, boardrooms and private clients &mdash; because no woman should have to choose between success and her wellbeing.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="about.html">More about Dawn &rarr;</a></div></div></div>','cream')
  + pullquote('&ldquo;You&rsquo;re not inconsistent. You&rsquo;re unsupported.&rdquo;')
  + method_steps('The method','The Adawning Method&trade;',
      'The path I walk every woman through &mdash; on stage, in the room, and one to one.',
      [('Who am I?','01 &middot; Remember','Come back to the woman underneath the roles, the pressure and the performing.'),
       ('Body &middot; Breath &middot; Soul','02 &middot; Reconnect','Regulate the nervous system and feel safe in your own body again.'),
       ('Voice &middot; Worth &middot; Identity','03 &middot; Reclaim','Stop abandoning yourself. Reclaim your voice, your worth and your yes.'),
       ('Life &middot; Health &middot; Business','04 &middot; Rebuild','Rebuild your life from calm and clarity, not urgency and force.'),
       ('Lead &middot; Speak &middot; Inspire','05 &middot; Rise','Step into steady, self-led leadership &mdash; and light the way for others.')],
      close_say='This is the work. Lived first, then taught.',
      close_cta=('Work with me','soul-mastery-ascension.html'),cls='olive')
  + sec(head('For you','Support for the woman navigating it herself.',
      'Whether it&rsquo;s menopause, burnout or the quiet exhaustion of holding everything together &mdash; you don&rsquo;t need more discipline. You need the right support. Start where you feel ready.')
    + cards_link([
      ('Soul Mastery Sanctuary &mdash; Group','My online group membership: ongoing coaching and a community of women doing the deeper work together &mdash; emotional, identity and nervous-system support, week after week.',NDW_URL+'/soul-mastery-sanctuary.html','Join the group'),
      ('Soul Mastery Ascension &mdash; 1:1','The private, 1:1 version of the Sanctuary &mdash; my premium container for women ready to go all in, with close proximity and faster, deeper change.','soul-mastery-ascension.html','Work with me 1:1'),
    ]),'ivory')
  + sec(head('For organisations','Bring this work into your workplace.')
    + cards_link([
      ('Keynote Speaking','Warm, grounded keynotes on burnout, menopause, self-leadership and wellbeing that actually land.','speaking.html','See speaking'),
      ('Corporate Workshops &amp; Wellbeing','Workshops, wellbeing sessions and menopause policy advisory for teams and organisations.','corporate-workshops.html','For organisations'),
    ]),'cream')
  + sec('<div class="sec-head"><div class="kicker">On the stage</div><h2 style="color:var(--cream)">A voice that lands &mdash; and lasts.</h2></div>'
      + stats_row([('30','Years in corporate leadership'),('16+','Retreats led &mdash; Bali, Thailand &amp; QLD'),('2,000+','Largest stage')]),'burgundy grain')
  + quotes([
      ('The most powerful, deeply relaxing experience &mdash; Dawn has an incredible gift for holding space. I left feeling completely reset and reconnected to myself.','&mdash; Angela N. &middot; Hypno-meditation'),
      ('Dawn is warm, intuitive and genuinely transformational. I felt safe, seen and lighter than I have in years.','&mdash; Kiran &middot; Healing session'),
      ('Thoughtfully facilitated, calm and grounding &mdash; Dawn nurtured each one of us. I left calmer, more grounded and very grateful.','&mdash; Cynthia E. &middot; Day immersion'),
    ])
  + optin('Free guide','The 3-Minute Nervous System Reset.',
      'The first thing I teach every woman &mdash; a simple, practical way to calm an overwhelmed body in three minutes, anywhere. Enter your email and I&rsquo;ll send it over, with the occasional grounded note from me.',
      'Send me the guide','No pressure, no spam. Unsubscribe any time.','forest')
  + cta_band('Ready to bring calm, embodied leadership into your room?',
      [('Enquire now','contact.html','btn-gold'),('Listen to the podcast','podcast.html','btn-ghost')],'navy')
  + crosslink('Looking for Pilates, yoga, healing or events in Cleveland?','https://newdawnwellness.health','Visit New Dawn Wellness &rarr;'))

# ---- Start Here (ecosystem map)
D('start-here.html','Start Here | The Adawning &mdash; Dawn Edwards-Jones',
  'New here? Start here. A simple map of Dawn Edwards-Jones&rsquo; world &mdash; The Adawning &mdash; so you can find the right door, whether you&rsquo;re looking after your body, yourself, your business, your team or your next event.',
  hero('The Adawning','Start here.',
    'The Adawning is a movement helping women come home to themselves &mdash; in their bodies, their lives and their work. It&rsquo;s one philosophy with a few different doors. Wherever you are right now, there&rsquo;s a way in for you. Choose the one that fits &mdash; you can always come back for the others.',
    [('New to me? Start with the podcast','podcast.html','btn-ghost')])
  + sec(head('Find your door','Where would you like to begin?',
      'Six ways in &mdash; the same work, met wherever you are.')
    + doorways([
      ('I want to feel better in my body','New Dawn Wellness',
       'Pilates, yoga, massage, reiki, breathwork and events at our Cleveland studio &mdash; a calm place to come home to your body.',
       NDW_URL,'Visit the studio'),
      ('I want to come home to myself','Soul Mastery Sanctuary',
       'My online group &mdash; ongoing coaching and a community of women doing the deeper emotional, identity and nervous-system work together. Prefer 1:1? Soul Mastery Ascension is the private version.',
       NDW_URL+'/soul-mastery-sanctuary.html','Step inside'),
      ('I want to grow my business from calm','Soul-Led Business Coaching',
       'Build something meaningful without burning out &mdash; grounded strategy and nervous-system-first leadership for women in business.',
       'calm-to-chaos.html','Explore coaching'),
      ('I want to support the women on my team','Corporate Workshops &amp; Wellbeing',
       'Workshops, wellbeing days and menopause policy advisory that help your people manage stress, navigate menopause and stay well at work.',
       'corporate-workshops.html','For organisations'),
      ('I&rsquo;m looking for a speaker','Keynote Speaking',
       'Warm, grounded keynotes on menopause, burnout and self-leadership that land in the room &mdash; and last well beyond it.',
       'speaking.html','See speaking'),
      ('I&rsquo;ve just found you','Start with a listen or a read',
       'No commitment, no pressure. Begin with The Adawning podcast or my book, and simply come as you are.',
       'podcast.html','Listen to the podcast'),
    ]))
  + split('Dawn pausing with a warm cup, eyes closed',
      '<div class="kicker">Before you choose</div><h2>You don&rsquo;t have to have it figured out.</h2>'
      '<p>Most women arrive here unsure which door is theirs. That&rsquo;s normal. You don&rsquo;t need a plan or a label for what you&rsquo;re going through &mdash; you just need somewhere to start.</p>'
      '<p>Pick the one that sounds most like you today. If it turns out to be the wrong door, we&rsquo;ll find the right one together.</p>',
      True,photo='dawn-cup-eyes-closed.jpg',pos='center top')
  + pullquote('&ldquo;You don&rsquo;t need fixing. You need somewhere to exhale.&rdquo;')
  + cta_band('Not sure which door is yours? Tell me where you are &mdash; I&rsquo;ll point you the right way.',
      [('Start a conversation','contact.html','btn-gold'),('Read the book','book.html','btn-ghost')],'navy')
  + crosslink('Looking for Pilates, yoga, healing or events in Cleveland?','https://newdawnwellness.health','Visit New Dawn Wellness &rarr;'))

# ---- The Adawning Philosophy
D('philosophy.html','The Adawning Philosophy | What We Believe &mdash; Dawn Edwards-Jones',
  'The Adawning philosophy &mdash; the beliefs behind Dawn Edwards-Jones&rsquo; work. You&rsquo;re not broken. Your body isn&rsquo;t the enemy. And you deserve support long before breaking point.',
  hero('The Adawning','What we believe.',
    'Everything I teach &mdash; on stage, in the studio and one to one &mdash; comes back to a few simple truths. This is the ground it all stands on.',
    [('Find your way in','start-here.html','btn-ghost')])
  + sec(head('Our philosophy','We believe&hellip;',
      'Not as slogans. As the things I&rsquo;ve lived, and the things I&rsquo;ve watched change women&rsquo;s lives when they finally let themselves believe them too.')
    + creed([
      ('You don&rsquo;t need fixing.',
       'You&rsquo;re not broken. You&rsquo;re carrying more than any one person was built to hold &mdash; and doing it without enough support.'),
      ('Your body isn&rsquo;t broken &mdash; <em>it&rsquo;s overwhelmed.</em>',
       'The symptoms you&rsquo;re fighting are signals, not failures. Your body is asking for safety, not more pressure.'),
      ('Success was never meant to cost your wellbeing.',
       'Achievement and exhaustion don&rsquo;t have to arrive together. You can lead, and still feel like yourself.'),
      ('Rest is productive.',
       'Slowing down isn&rsquo;t falling behind. It&rsquo;s how a regulated body rebuilds the energy everything else depends on.'),
      ('Softness isn&rsquo;t weakness.',
       'Calm is a form of strength. The steadiest presence in the room is rarely the loudest one.'),
      ('Healing isn&rsquo;t selfish.',
       'Coming back to yourself is what makes you able to hold everyone else &mdash; without disappearing in the process.'),
      ('Your nervous system isn&rsquo;t the enemy.',
       'It has been protecting you. The work isn&rsquo;t to override it &mdash; it&rsquo;s to help it feel safe again.'),
      ('You deserve support <em>before</em> breaking point.',
       'Not once you&rsquo;ve collapsed. Before. Support isn&rsquo;t a reward for falling apart &mdash; it&rsquo;s how you never have to.'),
      ('Coming home to yourself changes everything.',
       'When you stop abandoning yourself, your health, your relationships and your work all begin to change from the inside out.'),
    ]),'cream')
  + split('Dawn standing in cream linen, hands at her heart',
      '<div class="kicker">Where this came from</div><h2>None of this is theory.</h2>'
      '<p>Every one of these beliefs was earned. Through grief, through burnout, through menopause, through rebuilding a life more than once.</p>'
      '<p>I don&rsquo;t teach women to override themselves, because overriding myself is exactly what broke me. I teach what actually brought me back.</p>',
      photo='dawn-white-linen-namaste.jpg')
  + pullquote('&ldquo;You&rsquo;re not inconsistent. You&rsquo;re unsupported.&rdquo;')
  + sec(head('The Adawning','This is the work.','')
    + manifesto([
      ('The Adawning is a movement &mdash; women choosing to stop surviving their own lives and start leading them from calm.',''),
      ('Not by doing more. By finally being supported properly.',''),
      ('If that&rsquo;s the woman you&rsquo;re becoming, you&rsquo;re already one of us.','small'),
    ]),'navy')
  + cta_band('There&rsquo;s a door here for wherever you are.',
      [('Find your way in','start-here.html','btn-gold'),('Listen to the podcast','podcast.html','btn-ghost')])
  + crosslink('Want to see how this becomes real, in a room?','https://newdawnwellness.health','Visit New Dawn Wellness &rarr;'))

# ---- About
D('about.html','About Dawn Edwards-Jones | Speaker &amp; Founder of The Adawning',
  'Meet Dawn Edwards-Jones &mdash; author, keynote speaker, self-leadership coach and founder of New Dawn Wellness and The Adawning. Her story, mission and approach.',
  hero_split('About Dawn','Hi, I&rsquo;m Dawn.',
    'Author, keynote speaker, self-leadership coach and founder of New Dawn Wellness and The Adawning. I help women stop abandoning themselves and lead their lives from calm.',
    [('Work with me','soul-mastery-ascension.html','btn-ghost')],
    'Dawn at a women&rsquo;s event &mdash; composed and present.','burgundy',
    photo='nd-dawn-event.jpg')
  + sec(head('My story','Everything I teach, I have first lived.',
      'I didn&rsquo;t arrive at this work through theory. I arrived through my own body &mdash; the long way.')
    + story([
      ('01 &middot; The corporate years','For thirty years, I was the woman who had it handled.',
       '<p class="lead">Leadership roles across Deloitte, KPMG, government and universities. Big responsibilities. Bigger expectations.</p>'
       '<p>I was good at it &mdash; the kind of good that means people stop asking if you&rsquo;re okay, because you always seem to be. On paper it looked like success. And in many ways, it was.</p>'
       '<p>But there&rsquo;s a particular kind of tired that comes from holding everything together for everyone else. It doesn&rsquo;t announce itself. You simply, slowly, forget what it feels like not to be bracing.</p>'),
      ('02 &middot; Losing the life I&rsquo;d planned','Then grief arrived in a way I couldn&rsquo;t manage or outwork.',
       '<p>I went from being a wife to a widow overnight. And the life I&rsquo;d built my plans around simply&hellip; stopped.</p>'
       '<p>I learned resilience the hard way &mdash; not as a concept, but as the thing that gets you out of bed when getting out of bed is the only goal you can manage. I rebuilt, slowly, because there was no other option. But I carried that loss in my body long after I&rsquo;d learned to function again.</p>'),
      ('03 &middot; Starting again','In time, I began again &mdash; on the other side of the world.',
       '<p>I emigrated from Wales to Australia with my husband and our three children. A new country, a new life, and all the invisible work of holding a family steady through enormous change.</p>'
       '<p>I built businesses. I raised children. I kept achieving. And I kept doing what so many women do without realising it &mdash; putting myself last on a list that never ended.</p>'),
      ('04 &middot; The breaking point','Eventually, my body stopped negotiating.',
       '<p>Menopause, trauma and years of quietly running on empty caught up with me all at once. The old strategy &mdash; try harder, manage it, push through &mdash; stopped working. If anything, it made everything worse.</p>'
       '<p>I did all the &ldquo;right&rdquo; things. More discipline. More routines. More willpower. And I still felt exhausted, anxious and disconnected from myself.</p>'
       '<p>That was when the truth finally landed: I wasn&rsquo;t failing. I was unsupported. My nervous system had been in survival mode for so long that no amount of effort could think its way out.</p>'),
      ('05 &middot; The turning point','What changed everything wasn&rsquo;t a course or a cure.',
       '<p>It was learning to regulate my nervous system. To come back into my body through breath, movement, yoga and Pilates. To feel safe again &mdash; not by doing more, but by finally letting myself be supported.</p>'
       '<p>For the first time in decades, I stopped bracing. And from that steadier place, so much of what I&rsquo;d been forcing began to come more easily.</p>'),
      ('06 &middot; Why I do this now','New Dawn Wellness grew out of that homecoming.',
       '<p>I built the space I&rsquo;d needed all along &mdash; somewhere women could put down what they carry, come back to their bodies, and remember who they are underneath the roles and the responsibility.</p>'
       '<p>Today I bring that lived experience to stages, boardrooms and private clients. I speak, I coach, I lead retreats, and I hold a community of women doing this work together.</p>'
       '<p>Because I know what it costs to hold everything alone &mdash; and I know what becomes possible when you finally don&rsquo;t have to. No woman should have to choose between her success and her wellbeing. My work exists so she doesn&rsquo;t have to.</p>'),
    ]),'cream')
  + split('Women resting at a wellness retreat',
      '<div class="kicker">Retreats</div><h2>Sixteen retreats and counting.</h2>'
      '<p>I&rsquo;ve designed and led over 16 retreats &mdash; from Thailand and Bali to Queensland, alongside intimate day retreats closer to home. Each one is built to do what modern life rarely allows: fully switch off, come back to your body, and remember who you are underneath everything you carry.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="https://newdawnwellness.health/retreats.html">Explore retreats &rarr;</a></div>',tone='beige')
  + sec(head('What I stand for','A few things I believe.')
    + cards([
      ('You&rsquo;re not inconsistent','You&rsquo;ve been trying to function without support. That&rsquo;s different &mdash; and fixable.',''),
      ('Safety before strategy','Lasting change is built on a regulated nervous system, not willpower.',''),
      ('Softness is strength','Calm, grounded leadership is the most powerful presence in any room.',''),
    ])
    + '<div class="cta-band" style="margin-top:8px"><div class="btn-row" style="justify-content:center"><a class="btn btn-ghost" href="philosophy.html">Read the full philosophy &rarr;</a></div></div>','cream')
  + cta_band('Everything I do points women back to themselves.',
      [('Bring Dawn to your event','contact.html','btn-gold'),('Read the book','book.html','btn-ghost')]))

# ---- Soul Mastery Ascension
D('soul-mastery-ascension.html','Soul Mastery Ascension | 1:1 Coaching with Dawn Edwards-Jones',
  'Soul Mastery Ascension &mdash; premium 1:1 coaching with Dawn Edwards-Jones. Deep identity and nervous-system work for women ready for lasting transformation.',
  hero('1:1 Coaching','Soul Mastery Ascension.',
    'The private, 1:1 version of the Soul Mastery Sanctuary &mdash; my premium container for women ready to go all in. Deep identity and nervous-system work, close proximity and faster, lasting transformation.',
    [('Enquire about working together','contact.html','btn-gold')])
  + sec(head('The work','Deep, personal, transformational.')
    + cards([
      ('Identity rewiring','Move beyond old patterns into who you&rsquo;re becoming.',''),
      ('Nervous-system mastery','Regulate at a deeper level so change holds under pressure.',''),
      ('Proximity to Dawn','Close, personal support &mdash; you&rsquo;re not another number.',''),
      ('Faster, deeper shifts','Private work moves you further, sooner.',''),
    ]),'cream')
  + split('Dawn writing, relaxed and smiling',
      '<div class="kicker">Who it&rsquo;s for</div><h2>For the woman ready to lead herself.</h2>'
      '<p>This is for high-functioning women who are done managing their lives from the outside and ready to transform from the inside. Places are intentionally limited so each woman gets my full attention.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Apply to work together</a></div>',
      photo='dawn-writing-smile.jpg')
  + crosslink('Not ready for 1:1? The Sanctuary is the group version &mdash; same work, in community.','https://newdawnwellness.health/soul-mastery-sanctuary.html','Explore Soul Mastery Sanctuary &rarr;'))

# ---- Calm to Chaos
D('calm-to-chaos.html','Calm to Chaos | Soul-Led Business Coaching with Dawn Edwards-Jones',
  'Calm to Chaos &mdash; soul-led business coaching for women building businesses without burning out. Grounded strategy and nervous-system-first leadership.',
  hero('Business Coaching','Calm to Chaos.',
    'Soul-led business coaching for women who want to grow something meaningful without sacrificing themselves to do it. Grounded strategy, nervous-system first.',
    [('Enquire','contact.html','btn-gold')])
  + split('Dawn writing quietly, head down and focused',
      '<div class="kicker">The approach</div><h2>Build from calm, not chaos.</h2>'
      '<p>Most business advice runs on urgency and hustle. I help you build the opposite way &mdash; sustainable growth rooted in clarity, self-leadership and a regulated nervous system, so your business supports your life instead of consuming it.</p>'
      '<ul class="ticks"><li>Clarity over busy-work</li><li>Aligned, invitation-based selling</li><li>Systems that protect your energy</li><li>Leadership from safety, not survival</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Start a conversation</a></div>',
      photo='dawn-writing-quiet.jpg')
  + cta_band('Your business should feel like ease, not another thing holding you together.',
      [('Enquire now','contact.html','btn-gold')],'navy'))

# ---- Speaking
D('speaking.html','Keynote Speaking | Dawn Edwards-Jones',
  'Book Dawn Edwards-Jones to speak. Warm, grounded keynotes on menopause, burnout, self-leadership and wellbeing for conferences, workplaces and women&rsquo;s events.',
  hero('Keynote Speaking','A voice that lands &mdash; and lasts.',
    'I speak on menopause, burnout, nervous-system health and self-leadership &mdash; warm, honest and grounded, with practical takeaways your audience will actually use.',
    [('Enquire about speaking','contact.html','btn-gold')],dark=True)
  + logo_row()
  + sec(head('Signature talks','Topics I&rsquo;m known for.')
    + cards([
      ('Menopause Confidence','Helping women &mdash; and the people around them &mdash; navigate the change with understanding.',''),
      ('Menopause &amp; Mental Health at Work','Why workplaces can&rsquo;t afford to ignore it, and what to do.',''),
      ('Self-Care &amp; Sustainable Success','For women entrepreneurs done running on empty.',''),
      ('You&rsquo;re Not Inconsistent, You&rsquo;re Unsupported','The nervous-system truth behind burnout and start-stop cycles.',''),
    ]),'cream')
  + split('Dawn with a warm, engaged room of women',
      '<div class="kicker">What you get</div><h2>Grounded, generous, memorable.</h2>'
      '<p>Behind every talk is 30 years in corporate leadership, a life rebuilt through trauma, grief and menopause burnout, and over 16 retreats held across Thailand, Bali and Queensland. I tailor every talk to your audience and outcome. Expect real stories, sound science and a room that leaves lighter, clearer and genuinely moved to change something.</p>'
      '<ul class="ticks"><li>Conferences &amp; summits</li><li>Corporate &amp; workplace wellbeing days</li><li>Women&rsquo;s events &amp; networks</li><li>Panels, workshops &amp; webinars</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Check availability</a></div>',
      photo='group1.jpg')
  + cta_band('Let&rsquo;s create a room your audience won&rsquo;t forget.',
      [('Enquire now','contact.html','btn-gold'),('Corporate workshops','corporate-workshops.html','btn-ghost')],'navy'))

# ---- Corporate Workshops
D('corporate-workshops.html','Corporate Workshops &amp; Wellbeing | Dawn Edwards-Jones',
  'Corporate wellbeing workshops and sessions with Dawn Edwards-Jones &mdash; menopause, burnout, nervous-system health and self-leadership for teams and organisations.',
  hero_split('For Workplaces',
    'Support the women who hold it all together.',
    'Practical, grounded workshops that help your people manage stress, navigate menopause and lead themselves &mdash; reframing wellbeing as performance, retention and care.',
    [('Enquire for your team','contact.html','btn-gold'),('Book a discovery call','contact.html','btn-ghost')],
    'Dawn leading a wellbeing workshop for a room of women','navy',
    cred='Menopause &middot; Burnout &middot; Nervous-system health &middot; Self-leadership',
    photo='group2.jpg')
  + logo_row()
  + sec(head('What I deliver','Sessions built for real workplaces.')
    + cards([
      ('Menopause at Work','Education and practical support for staff and managers &mdash; reducing stigma and absence.',''),
      ('Burnout &amp; Nervous-System Health','Give teams the tools to regulate stress and stay resourced.',''),
      ('Self-Leadership &amp; Wellbeing','Sustainable performance without the burnout culture.',''),
      ('Wellbeing Days &amp; Retreats','Movement, breathwork and restoration for your team.',''),
    ]),'cream')
  + split('A workshop in a modern workplace setting',
      '<div class="kicker">Why it matters</div><h2>Wellbeing is a business issue.</h2>'
      '<p>Unsupported stress and menopause cost organisations in absence, turnover and lost performance. I help you get ahead of it &mdash; with sessions that are warm and human, not clinical or preachy.</p>'
      '<ul class="ticks"><li>Reduce absence and turnover</li><li>Support women through midlife transitions</li><li>Build a genuinely caring culture</li><li>Practical tools people actually use</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Book a discovery call</a></div>')
  + cta_band('Ready to support the women who hold your organisation together?',
      [('Enquire now','contact.html','btn-gold'),('Book a discovery call','contact.html','btn-ghost')],'navy')
  + crosslink('Want to embed lasting change in your organisation?','menopause-policy.html','Explore Menopause Policy Advisory &rarr;'))

# ---- Menopause Policy
D('menopause-policy.html','Menopause Policy Advisory &amp; Implementation | Dawn Edwards-Jones',
  'Workplace menopause policy advisory and implementation with Dawn Edwards-Jones. I help management shape a menopause policy &mdash; then put it into practice across your organisation.',
  hero('For Workplaces','Menopause Policy Advisory &amp; Implementation.',
    'I work alongside your leadership to shape a meaningful workplace menopause policy &mdash; then help you put it into practice, so it becomes lived culture, not a document in a drawer.',
    [('Book a discovery call','contact.html','btn-gold')],dark=True)
  + sec(head('How we work together','From policy to practice.')
    + cards([
      ('1. Advisory','I work with management to shape a menopause policy that fits your people and your organisation &mdash; practical, compassionate and clear.',''),
      ('2. Implementation','We put the policy into practice &mdash; manager training, staff education and the everyday support that makes it real.',''),
      ('3. Embedding','Ongoing guidance so the policy becomes part of how your workplace actually operates.',''),
    ]))
  + split('Leadership team in a considered planning session',
      '<div class="kicker">Why it matters</div><h2>A policy is only as good as its practice.</h2>'
      '<p>Too many organisations write a menopause policy and stop there. My role is to make sure it lives &mdash; shaping the document with your leadership, then guiding the training, communication and everyday support that turn intention into culture.</p>'
      '<ul class="ticks"><li>Advisory partnership with management</li><li>Policy shaped to your organisation</li><li>Manager and staff education</li><li>Practical implementation and follow-through</li></ul>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Start the conversation</a></div>','cream')
  + cta_band('Let&rsquo;s build a workplace where women don&rsquo;t have to suffer in silence.',
      [('Enquire now','contact.html','btn-gold'),('See workshops','corporate-workshops.html','btn-ghost')],'navy'))

# ---- Podcast
D('podcast.html','The Adawning Podcast | Dawn Edwards-Jones',
  'The Adawning &mdash; the podcast from Dawn Edwards-Jones. Honest, grounded conversations on self-leadership, nervous-system health, menopause and coming home to yourself.',
  hero('Listen','The Adawning Podcast.',
    'Honest, grounded conversations on self-leadership, the nervous system, menopause and what it really takes to stop abandoning yourself. Come as you are.',
    [('Get in touch','contact.html','btn-ghost')])
  + split('Dawn recording, headphones on',
      '<div class="kicker">About the show</div><h2>Real talk for women coming home to themselves.</h2>'
      '<p>Each episode is a warm, no-fluff conversation &mdash; part insight, part permission slip. Expect nervous-system science, lived experience and the reframes that help you breathe a little easier.</p>'
      '<p>Search &ldquo;The Adawning&rdquo; on your favourite podcast app, or reach out to be a guest.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Be a guest</a></div>',
      photo='nd-dawn-podcast.jpg')
  + cta_band('Press play and come back to yourself.',
      [('Contact Dawn','contact.html','btn-gold')],'navy'))

# ---- Book
D('book.html','The Book | Dawn Edwards-Jones',
  'Dawn Edwards-Jones&rsquo; book &mdash; a grounded guide to self-leadership, nervous-system health and coming home to yourself. Register your interest.',
  hero('The Book','The book.',
    'Everything I teach &mdash; the nervous-system truth behind burnout, and the path back to calm, self-led living &mdash; distilled into one grounded, honest read.',
    [('Register your interest','contact.html','btn-gold')])
  + split('Dawn&rsquo;s hands writing in a journal',
      '<div class="kicker">Inside</div><h2>You&rsquo;re not inconsistent. You&rsquo;ve been unsupported.</h2>'
      '<p>This book is for the woman holding everything together while quietly running on empty. It offers a different way &mdash; not more discipline, but more support, safety and self-leadership.</p>'
      '<div class="btn-row"><a class="btn btn-gold" href="contact.html">Be first to know</a></div>',
      photo='dawn-journal-hands.jpg')
  + cta_band('Be the first to hear when it&rsquo;s out.',
      [('Register your interest','contact.html','btn-gold')],'navy'))

# ---- Contact
D('contact.html','Contact Dawn Edwards-Jones | Speaking &amp; Coaching Enquiries',
  'Contact Dawn Edwards-Jones for keynote speaking, corporate workshops, menopause policy advisory or 1:1 coaching enquiries. Let&rsquo;s create something meaningful together.',
  hero('Enquire','Let&rsquo;s work together.',
    'Whether you&rsquo;re booking a speaker, supporting your team, or ready for private coaching &mdash; I&rsquo;d love to hear what you&rsquo;re creating. No pressure, just a conversation.',
    [('Email Dawn','mailto:'+EMAIL,'btn-gold')])
  + sec('<div class="split">'
      + '<div><div class="kicker">Get in touch</div><h2>Start a conversation.</h2>'
        '<ul class="ticks"><li>Email: '+EMAIL+'</li><li>Keynote &amp; workshop enquiries welcome</li><li>Menopause policy advisory for organisations</li><li>1:1 coaching applications</li></ul>'
        '<div class="btn-row"><a class="btn btn-gold" href="speaking.html">Speaking</a><a class="btn btn-ghost" href="soul-mastery-ascension.html">1:1 Coaching</a></div></div>'
      + photofig('dawn-journaling-wide.jpg','Dawn journaling at home, warm and approachable','gold')
      + '</div>')
  + enquiry_form('Send an enquiry','Tell me what you are creating.',
      'Give me the shape of it and I will come back with whether I am the right fit, what it would look like '
      'and what it would cost. If I am not the right person, I will tell you that too.',
      ['Keynote speaking','Corporate workshop or wellbeing day','Menopause policy advisory',
       'Menopause policy implementation','Soul Mastery Ascension (1:1 coaching)',
       'Calm to Chaos (business coaching)','Podcast guest or interview','Media enquiry','Something else'],
      'Send my enquiry','website-contact-dej'))

# ---- Privacy
D('privacy.html','Privacy Policy | Dawn Edwards-Jones',
  'How Dawn Edwards-Jones collects, uses, stores and protects your personal information, and how to access or correct it.',
  privacy_body('Dawn Edwards-Jones','dawnedwards-jones.com',False))

# ---- Terms
D('terms.html','Terms &amp; Conditions | Dawn Edwards-Jones',
  'The terms that apply to speaking engagements, corporate workshops, advisory work and coaching with Dawn Edwards-Jones.',
  terms_body('Dawn Edwards-Jones','dawnedwards-jones.com',False))

print("dej pages:", len(DEJ_PAGES))

# ================================================================ BUILD
import base64, mimetypes

def ensure(d):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- OG IMAGE
# Builds the 1200x630 social share card referenced by og:image on every page.
# Uses Lora as the heading face because Cormorant Garamond is not installed here.
# TODO optional: if you want the exact brand font, make a 1200x630 card in Canva
# and drop it in as og-image.jpg. This one is a solid stand-in, not a compromise.
OG_SERIF = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
OG_SANS  = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"

def make_og_image(site, photo, headline, kicker):
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    except ImportError:
        print("  skipped og-image (PIL not available):", site['domain']); return
    src=os.path.join(PHOTO_DIR, photo)
    W_,H_=1200,630
    try:
        im=Image.open(src).convert('RGB')
    except Exception as e:
        print("  skipped og-image (%s): %s"%(photo,e)); return
    # cover-crop to 1200x630
    sw,sh=im.size
    scale=max(W_/sw, H_/sh)
    im=im.resize((int(sw*scale+1),int(sh*scale+1)), Image.LANCZOS)
    sw,sh=im.size
    im=im.crop(((sw-W_)//2,(sh-H_)//2,(sw-W_)//2+W_,(sh-H_)//2+H_))
    im=ImageEnhance.Color(im).enhance(.78)
    # navy scrim, heavier at the bottom so the text always reads
    scrim=Image.new('L',(1,H_))
    for y in range(H_):
        t=y/(H_-1)
        scrim.putpixel((0,y), min(248,int(96+185*(t**1.5))))
    scrim=scrim.resize((W_,H_))
    navy=Image.new('RGB',(W_,H_),(25,43,83))
    im=Image.composite(navy,im,scrim)
    d=ImageDraw.Draw(im)
    try:
        f_h=ImageFont.truetype(OG_SERIF,74)
        f_k=ImageFont.truetype(OG_SANS,25)
        f_s=ImageFont.truetype(OG_SANS,27)
    except Exception:
        f_h=f_k=f_s=ImageFont.load_default()
    # wrap the headline
    words=headline.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f_h)>1010 and cur: lines.append(cur); cur=w
        else: cur=t
    if cur: lines.append(cur)
    y=H_-96-len(lines)*84
    d.text((80,y-56),kicker.upper(),font=f_k,fill=(244,162,97))
    for ln in lines:
        d.text((80,y),ln,font=f_h,fill=(255,234,209)); y+=84
    d.text((80,y+16),site['domain'],font=f_s,fill=(233,203,167))
    # gold rule
    d.rectangle([80,H_-46,160,H_-42],fill=(244,162,97))
    im.save(os.path.join(site['dir'],'og-image.jpg'),'JPEG',quality=86,optimize=True)
    print("  og-image written:",site['domain'])

def build_site(site, pages):
    ensure(site['dir'])
    # remove stale HTML from earlier builds (renamed or deleted pages)
    keep={s for s,_,_,_ in pages}
    for f in os.listdir(site['dir']):
        if f.endswith('.html') and f not in keep:
            try:
                os.remove(os.path.join(site['dir'],f))
                print("  removed stale page:",site['domain'],f)
            except OSError:
                print("  WARNING stale page could not be removed, delete by hand:",site['domain'],f)
    ensure(os.path.join(site['dir'],'assets'))
    with open(os.path.join(site['dir'],'assets','style.css'),'w',encoding='utf-8') as f:
        f.write(BASE_CSS)
    ft=footer(site)
    for slug,title,desc,body in pages:
        page(site,slug,title,desc,body,ft)
    # sitemap
    urls=''.join('<url><loc>https://%s/%s</loc></url>'%(site['domain'],'' if s=='index.html' else s) for s,_,_,_ in pages)
    with open(os.path.join(site['dir'],'sitemap.xml'),'w',encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'%urls)
    with open(os.path.join(site['dir'],'robots.txt'),'w',encoding='utf-8') as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n"%site['domain'])

ensure(SITES_DIR)
build_site(ndw,NDW_PAGES)
build_site(dej,DEJ_PAGES)
make_og_image(ndw,'supported-women.jpg','You are not inconsistent. You have been unsupported.','New Dawn Wellness, Cleveland QLD')
make_og_image(dej,'dawn-journaling-wide.jpg','Helping women stop abandoning themselves.','Dawn Edwards-Jones')

# copy logos into DEJ site
src_logos=os.path.join(ROOT,'logos')
dej_logos=os.path.join(dej['dir'],'logos')
ensure(dej_logos)
logo_b64={}
if os.path.isdir(src_logos):
    for f,_ in LOGOS:
        sp=os.path.join(src_logos,f)
        if os.path.exists(sp):
            shutil.copy(sp,os.path.join(dej_logos,f))
            mime=mimetypes.guess_type(sp)[0] or 'image/png'
            with open(sp,'rb') as fh:
                logo_b64[f]='data:%s;base64,%s'%(mime,base64.b64encode(fh.read()).decode())

# ---------------------------------------------------------------- PREVIEWS
INTERCEPT="""<script>(function(){document.addEventListener('click',function(e){
var a=e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
if(h.indexOf('http')===0||h.indexOf('mailto')===0||h.charAt(0)==='#')return;
if(h.slice(-5)==='.html'){e.preventDefault();parent.postMessage({nav:h},'*');}
});})();</script>"""

def make_preview(site, pages, out_path):
    store={}
    for slug,title,desc,body in pages:
        # rebuild page html with inline CSS + intercept
        canon=""  # not needed in preview
        nav=build_nav(site['nav'],slug,site['brand'],site['sub'])
        doc=('<!DOCTYPE html><html lang="en-AU"><head><meta charset="UTF-8">'
          '<meta name="viewport" content="width=device-width,initial-scale=1">'
          '<style>%s</style></head><body>%s<main>%s</main>%s%s%s</body></html>'
          )%(BASE_CSS,nav,body,footer(site),NAV_JS,INTERCEPT)
        # inline logos
        for f,uri in logo_b64.items():
            doc=doc.replace('logos/'+f,uri)
        store[slug]=doc
    def enc(t):
        return t.replace('\\','\\\\').replace('`','\\`').replace('${','$\\{').replace('</script>','<\\/script>')
    js_store=';'.join('P[%r]=%s'%(s,'`'+enc(store[s])+'`') for s in store)
    shell=("""<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s &mdash; Preview</title>
<style>body{margin:0;font-family:-apple-system,Segoe UI,sans-serif;background:#192b53}
.bar{background:#192b53;color:#ffead1;padding:10px 18px;font-size:13px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.bar b{color:#f4a261;font-weight:600}.bar span{opacity:.75}
.bar select{background:#0f1c38;color:#ffead1;border:1px solid #f4a261;border-radius:6px;padding:6px 10px;font-size:12px}
iframe{width:100%%;height:calc(100vh - 42px);border:0;background:#fff;display:block}</style></head>
<body><div class="bar"><b>%s</b><span>Draft preview &mdash; click through the site normally. Jump to any page:</span>
<select id="jump">%s</select></div>
<iframe id="fr"></iframe>
<script>var P={};%s;
var fr=document.getElementById('fr');
function show(s){if(!P[s])s='index.html';fr.srcdoc=P[s];var j=document.getElementById('jump');if(j.value!==s)j.value=s;}
window.addEventListener('message',function(e){if(e.data&&e.data.nav)show(e.data.nav);});
document.getElementById('jump').addEventListener('change',function(){show(this.value);});
show('index.html');</script></body></html>""")%(
      site['brand'],site['brand'],
      ''.join('<option value="%s">%s</option>'%(s,t.split('|')[0].split('&mdash;')[0].strip()) for s,t,_,_ in pages),
      js_store)
    with open(out_path,'w',encoding='utf-8') as f:
        f.write(shell)

make_preview(ndw,NDW_PAGES,os.path.join(ROOT,'PREVIEW-new-dawn-wellness.html'))
make_preview(dej,DEJ_PAGES,os.path.join(ROOT,'PREVIEW-dawn-edwards-jones.html'))

print("DONE. NDW pages:",len(NDW_PAGES),"| DEJ pages:",len(DEJ_PAGES))
print("previews written to project root")
