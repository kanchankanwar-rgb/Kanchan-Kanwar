#!/usr/bin/env python3
"""Generates the Hemavik website from content.py.

Usage (from the hemavik/ folder):  python3 _build/build.py
Writes static HTML pages, sitemap.xml and robots.txt next to this folder.
"""
import html
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from content import SITE, CATEGORIES, SERVICES, INDUSTRIES, PROCESS, COMMITMENTS, INSIGHTS, PAGES, FOUNDER, CHANNELS  # noqa: E402
from visuals import visual, thumb  # noqa: E402

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YEAR = date.today().year


def e(s):
    return html.escape(s, quote=True)


def cat_of(slug):
    for c in CATEGORIES:
        if slug in c["services"]:
            return c
    raise KeyError(slug)


MARK = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="hv-mark" viewBox="0 0 64 64">
    <circle cx="32" cy="32" r="29" fill="none" stroke="currentColor" stroke-width="2.5"/>
    <rect x="19" y="18" width="5" height="28" rx="1" fill="currentColor"/>
    <rect x="40" y="18" width="5" height="28" rx="1" fill="currentColor"/>
    <rect x="19" y="32" width="26" height="4" fill="currentColor"/>
    <path d="M26 24 A6 6 0 0 0 38 24 A6 3.5 0 0 1 26 24 Z" fill="currentColor"/>
    <circle cx="32" cy="41" r="2.2" fill="currentColor"/>
  </symbol>
  <symbol id="hv-arrow" viewBox="0 0 16 16">
    <path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  </symbol>
</svg>"""

MOUNTAINS = """<svg class="peaks" viewBox="0 0 1440 360" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
  <path class="pk-far" d="M0 250 L110 190 L200 222 L320 128 L410 176 L520 96 L610 158 L720 70 L820 146 L930 104 L1010 150 L1090 58 L1170 140 L1260 112 L1360 160 L1440 130 V360 H0Z"/>
  <path class="pk-snow" d="M1090 58 L1062 100 L1078 94 L1090 108 L1104 92 L1120 100 Z M720 70 L698 104 L712 98 L724 110 L738 96 Z"/>
  <path class="pk-mid" d="M0 300 L140 232 L260 268 L380 196 L470 240 L600 176 L700 232 L800 160 L900 224 L1010 184 L1120 244 L1230 196 L1340 252 L1440 222 V360 H0Z"/>
  <path class="pk-cloud" d="M0 326 C120 296 220 318 320 304 C440 286 520 318 640 300 C760 282 860 312 980 296 C1100 280 1200 310 1320 296 C1380 290 1420 298 1440 294 V360 H0Z"/>
</svg>"""


ORG_ID = SITE["url"] + "/#organization"
OG = {}  # og image key -> (eyebrow, title); rendered by _build/og-images.cjs


def url_of(path):
    return SITE["url"] + "/" + path.replace("index.html", "")


def og_spec(key, eyebrow, title):
    OG[key] = {"eyebrow": eyebrow, "title": title}
    return key


def ld_org():
    return {
        "@context": "https://schema.org", "@type": "Organization", "@id": ORG_ID,
        "name": SITE["name"], "url": SITE["url"] + "/", "email": SITE["email"],
        "logo": SITE["url"] + "/assets/logo/hemavik-logo-512.png",
        "description": "Digital marketing, CRM and marketing automation, websites, AI workflows and Voice AI agents for growing businesses.",
        "slogan": SITE["tagline"],
        "areaServed": ["IN", "Worldwide"],
        "knowsAbout": [SERVICES[x]["title"] for c in CATEGORIES for x in c["services"]],
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": SITE["email"], "availableLanguage": ["English", "Hindi"]},
        "founder": ld_person(),
    }


def ld_person():
    return {"@type": "Person", "name": FOUNDER["name"], "jobTitle": FOUNDER["role"],
            "image": f'{SITE["url"]}/assets/img/{FOUNDER["photo"]}.jpg', "worksFor": {"@id": ORG_ID},
            "url": SITE["url"] + "/about.html#founder"}


def ld_website():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE["url"] + "/#website",
            "name": SITE["name"], "url": SITE["url"] + "/", "publisher": {"@id": ORG_ID}, "inLanguage": "en"}


def ld_crumbs(crumbs, path):
    items = []
    for i, (name, href) in enumerate(crumbs, 1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": url_of(href or path)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def ld_page(kind, name, desc, path):
    return {"@context": "https://schema.org", "@type": kind, "name": name, "description": desc,
            "url": url_of(path), "isPartOf": {"@id": SITE["url"] + "/#website"}, "publisher": {"@id": ORG_ID}}


def head(title, desc, r, path, ld=(), og="index", noindex=False, ogtype="website"):
    full = f"{title} | {SITE['name']}"
    canonical = url_of(path)
    img = f'{SITE["url"]}/assets/og/{og}.png'
    scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld
    )
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="{SITE['locale']}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(title)} · Hemavik">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#F5F8FB">
<link rel="icon" href="{r}assets/logo/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}assets/logo/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/logo/apple-touch-icon.png">
<link rel="manifest" href="{r}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{r}assets/css/hemavik.css">
<link rel="stylesheet" href="{r}assets/css/site.css">
{scripts}
</head>
<body>
{MARK}
<a class="skip" href="#main">Skip to content</a>
"""


def header(r, active=""):
    cols = []
    for c in CATEGORIES:
        links = "".join(
            f'<li><a href="{r}services/{s}.html">{e(SERVICES[s]["title"])}</a></li>' for s in c["services"]
        )
        cols.append(f'<div class="mega-col"><p class="mega-cat">{e(c["title"])}</p><ul>{links}</ul></div>')
    mega = "".join(cols)

    def cur(name):
        return ' aria-current="page"' if active == name else ""

    return f"""<header class="site-head">
  <div class="wrap head-row">
    <a class="logo" href="{r}index.html" aria-label="Hemavik home">
      <svg aria-hidden="true"><use href="#hv-mark"/></svg>
      <span class="logo-word"><b>HEMAVIK</b></span>
    </a>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <div class="nav-item has-mega">
        <button class="nav-link mega-btn" id="mega-btn" type="button" aria-expanded="false" aria-controls="mega"{cur("services")}>Services<svg aria-hidden="true"><use href="#hv-arrow"/></svg></button>
        <div class="mega" id="mega">
          <div class="wrap mega-grid">
            <div class="mega-intro">
              <p class="eyebrow">What we do</p>
              <p class="mega-lead">Marketing, automation and AI, delivered by one team on one connected platform.</p>
              <a class="text-link" href="{r}services.html">All services <svg aria-hidden="true"><use href="#hv-arrow"/></svg></a>
            </div>
            {mega}
          </div>
        </div>
      </div>
      <a class="nav-link" href="{r}industries.html"{cur("industries")}>Industries</a>
      <a class="nav-link" href="{r}insights.html"{cur("insights")}>Insights</a>
      <a class="nav-link" href="{r}about.html"{cur("about")}>About</a>
      <a class="btn btn-primary nav-cta" href="{r}contact.html">Talk to us</a>
    </nav>
  </div>
</header>
<main id="main">
"""


def cta_band(r, title="Let's build your growth system", text="Book a free assay. In 30 minutes we will map where your leads and hours are leaking, and what to fix first."):
    return f"""<section class="cta-band">
  {MOUNTAINS}
  <div class="wrap cta-row">
    <div class="cta-copy">
      <p class="eyebrow">Start with an assay</p>
      <h2>{e(title)}</h2>
      <p>{e(text)}</p>
    </div>
    <a class="btn btn-snow" href="{r}contact.html">Book a free strategy call <svg aria-hidden="true"><use href="#hv-arrow"/></svg></a>
  </div>
</section>
"""


def footer(r):
    cols = []
    for c in CATEGORIES:
        links = "".join(
            f'<li><a href="{r}services/{s}.html">{e(SERVICES[s]["title"])}</a></li>' for s in c["services"]
        )
        cols.append(f'<div class="foot-col"><p class="foot-h">{e(c["title"])}</p><ul>{links}</ul></div>')
    ind = "".join(f'<li><a href="{r}industries.html#{s}">{e(t)}</a></li>' for s, t, *_ in INDUSTRIES[:5])
    return f"""</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="logo logo-rev" href="{r}index.html" aria-label="Hemavik home">
          <svg aria-hidden="true"><use href="#hv-mark"/></svg>
          <span class="logo-word"><b>HEMAVIK</b></span>
        </a>
        <p>{e(SITE["tagline"])}</p>
        <p class="foot-mail">{e(SITE["email"])}</p>
      </div>
      <div class="foot-cols">
        {"".join(cols)}
        <div class="foot-col"><p class="foot-h">Industries</p><ul>{ind}<li><a href="{r}industries.html">All industries</a></li></ul></div>
        <div class="foot-col"><p class="foot-h">Company</p><ul>
          <li><a href="{r}about.html">About us</a></li>
          <li><a href="{r}insights.html">Insights</a></li>
          <li><a href="{r}contact.html">Contact</a></li>
        </ul></div>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© {YEAR} Hemavik. All rights reserved.</span>
      <span>Hema (हेम): gold. Pure systems, golden growth.</span>
    </div>
  </div>
</footer>
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
"""


def arrow():
    return '<svg class="arr" aria-hidden="true"><use href="#hv-arrow"/></svg>'


def faq_html(faqs):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)


def page_hero(eyebrow, title, lede, crumbs, r, extra="", side=""):
    bc = " <span>/</span> ".join(
        f'<a href="{r}{href}">{e(t)}</a>' if href else f'<span aria-current="page">{e(t)}</span>' for t, href in crumbs
    )
    return f"""<section class="page-hero">
  {MOUNTAINS}
  <div class="wrap page-hero-grid{' has-side' if side else ''}">
    <div class="page-hero-inner">
      <nav class="crumbs" aria-label="Breadcrumb">{bc}</nav>
      <p class="eyebrow">{e(eyebrow)}</p>
      <h1>{title}</h1>
      <p class="lede">{e(lede)}</p>
      {extra}
    </div>
    {f'<div class="hero-visual">{side}<p class="vis-note">Illustrative example</p></div>' if side else ''}
  </div>
</section>
"""


# ---------------------------------------------------------------- pages

def picture(r, name, alt, cls="", eager=False, sizes="(min-width: 900px) 420px, 90vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""<picture class="{cls}">
  <source type="image/webp" srcset="{r}assets/img/{name}-sm.webp 440w, {r}assets/img/{name}.webp 800w" sizes="{sizes}">
  <img src="{r}assets/img/{name}.jpg" srcset="{r}assets/img/{name}-sm.jpg 440w, {r}assets/img/{name}.jpg 800w" sizes="{sizes}" width="800" height="1000" alt="{e(alt)}" {load} decoding="async">
</picture>"""


HUB_POS = ["a", "b", "c", "d"]   # top-left, top-right, bottom-left, bottom-right
HUB_XY = {"a": (28.8, 22), "b": (131.2, 22), "c": (28.8, 78), "d": (131.2, 78)}


def what_we_do(r):
    nodes, panels, lines = [], [], []
    for i, c in enumerate(CATEGORIES):
        pos = HUB_POS[i]
        x, y = HUB_XY[pos]
        on = i == 0
        lines.append(f'<path class="hub-line{" on" if on else ""}" data-line="{i}" d="M{x} {y} L80 50"/>'
                     f'<path class="hub-pulse" style="--d:{i * 0.6}s" d="M{x} {y} L80 50" pathLength="100"/>')
        chips = "".join(f'<span>{e(SERVICES[x]["title"])}</span>' for x in c["services"])
        nodes.append(f"""<button class="hub-node pos-{pos}" type="button" role="tab" id="hub-tab-{i}" aria-controls="hub-panel-{i}" aria-selected="{str(on).lower()}" data-i="{i}">
        <span class="hub-stage">{i + 1:02d} · {e(c["stage"])}</span>
        <b>{e(c["title"])}</b>
        <span class="hub-chips">{chips}</span>
      </button>""")
        links = "".join(
            f'<li><a href="{r}services/{x}.html"><span><b>{e(SERVICES[x]["title"])}</b><small>{e(SERVICES[x]["short"])}</small></span>{arrow()}</a></li>'
            for x in c["services"])
        panels.append(f"""<div class="hub-panel" role="tabpanel" id="hub-panel-{i}" aria-labelledby="hub-tab-{i}"{"" if on else " hidden"}>
      <div class="hub-copy">
        <p class="eyebrow">Stage {i + 1:02d} · {e(c["stage"])}</p>
        <h3>{e(c["stage_line"])}</h3>
        <p>{e(c["blurb"])}</p>
        <ul class="cap-list">{links}</ul>
      </div>
      <div class="hub-vis" aria-hidden="true">{visual(CAP_VIS[c["slug"]])}</div>
    </div>""")
    return f"""<section class="section wwd" id="what-we-do">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">What we do</p><h2>Eleven services. One team. One connected system.</h2></div>
      <p class="lede">Most businesses buy marketing, software and automation from different suppliers, and leads fall through the gaps. With Hemavik, every service feeds one customer record, so each stage hands over to the next automatically.</p>
    </div>
    <div class="hub" data-hub>
      <div class="hub-map" role="tablist" aria-label="Capabilities">
        <svg class="hub-lines" viewBox="0 0 160 100" aria-hidden="true">{"".join(lines)}</svg>
        <div class="hub-core">
          <span class="ring"></span><span class="ring r2"></span>
          <svg aria-hidden="true"><use href="#hv-mark"/></svg>
          <b>One customer record</b>
          <small>Every lead, message, call, booking and payment in one place</small>
        </div>
        {"".join(nodes)}
      </div>
      <div class="hub-panels">{"".join(panels)}</div>
    </div>
  </div>
</section>
"""


def marquee():
    items = "".join(f"<li>{e(c)}</li>" for c in CHANNELS)
    return f"""<section class="channels" aria-label="Channels we connect">
  <div class="wrap"><p class="eyebrow">Connected with the channels your customers already use</p></div>
  <div class="marquee"><ul>{items}</ul><ul aria-hidden="true">{items}</ul></div>
</section>
"""


def founder_band(r):
    f = FOUNDER
    return f"""<section class="section founder">
  <div class="wrap founder-grid">
    <figure class="founder-photo">{picture(r, f["photo"], f'{f["name"]}, {f["role"]} of Hemavik')}</figure>
    <div class="founder-copy">
      <p class="eyebrow">Meet the founder</p>
      <blockquote><p>{e(f["quote"])}</p></blockquote>
      <p class="founder-name"><b>{e(f["name"])}</b><span>{e(f["role"])}, Hemavik</span></p>
      <a class="text-link" href="{r}about.html#founder">About Hemavik {arrow()}</a>
    </div>
  </div>
</section>
"""


def stat_html(n, t):
    num = "".join(ch for ch in n if ch.isdigit())
    count = f' data-count="{num}"' if num and "/" not in n else ""
    return f'<div class="stat"><b{count}>{e(n)}</b><span>{e(t)}</span></div>'


CAP_VIS = {"growth": "digital-marketing", "engagement": "marketing-automation", "experience": "website-development", "ai": "ai-workflows"}


def home():
    r = ""
    featured = [
        ("voice-ai", "AI & Automation", "Every call answered, every appointment booked, even at 2 a.m."),
        ("crm-automation", "Customer Engagement", "One inbox and one pipeline for every lead, from every channel."),
        ("google-meta-ads", "Growth & Marketing", "Ads measured by booked appointments, not by clicks."),
    ]
    feat = "".join(
        f"""<a class="feature" href="services/{s}.html">
      {thumb(s)}
      <span class="feature-tag">{e(tag)}</span>
      <h3>{e(SERVICES[s]["title"])}</h3>
      <p>{e(line)}</p>
      <span class="feature-go">Explore {arrow()}</span>
    </a>""" for s, tag, line in featured
    )
    stats = "".join(stat_html(n, t) for n, t in COMMITMENTS)
    inds = "".join(
        f'<a class="ind" href="industries.html#{s}"><h3>{e(t)}</h3><p>{e(p)}</p>{arrow()}</a>' for s, t, p, _ in INDUSTRIES
    )
    steps = "".join(
        f'<li><span class="step-no">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS)
    )
    ins = "".join(insight_card(a, r) for a in INSIGHTS)

    body = f"""<section class="hero">
  {MOUNTAINS}
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="hallmark"><span>999</span><span>MARKETING</span><span>AUTOMATION</span><span>AI</span></span>
      <h1>Pure systems.<br><em>Golden growth.</em></h1>
      <p class="lede">Hemavik helps growing businesses win more customers with less effort. We run your marketing, automate your sales and service, and put AI agents to work on every call and chat, all on one connected platform.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="contact.html">Talk to an expert</a>
        <a class="btn btn-ghost" href="services.html">Explore services</a>
      </div>
    </div>
    <figure class="flow" aria-label="Example: a lead from a Meta ad becomes a booked appointment automatically">
      <figcaption class="flow-top"><span class="eyebrow">A lead, end to end</span><span class="chip chip-live">Live</span></figcaption>
      <ol class="flow-nodes">
        <li class="node" style="--i:0"><i>ADS</i><span>Meta lead ad submitted<small>trigger · 21:41:02</small></span></li>
        <li class="node" style="--i:1"><i>CRM</i><span>Contact created, stage "New lead"<small>pipeline · source tracked</small></span></li>
        <li class="node" style="--i:2"><i>AI</i><span>Lead scored and enriched<small>score 82 / 100 · hot</small></span></li>
        <li class="node" style="--i:3"><i>MSG</i><span>WhatsApp and email reply sent<small>within 60 seconds</small></span></li>
        <li class="node" style="--i:4"><i>VOX</i><span>Voice AI calls back, books visit<small>calendar · Thu 11:30</small></span></li>
      </ol>
    </figure>
  </div>
</section>

<section class="featured" aria-labelledby="featured-h">
  <h2 class="sr-only" id="featured-h">Featured services</h2>
  <div class="wrap feature-grid">{feat}</div>
</section>

{marquee()}
{what_we_do(r)}
<section class="stats-band">
  <div class="wrap stats">{stats}</div>
</section>

<section class="section section-glacier" id="approach">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">How we deliver</p><h2>Refined like gold, in five steps</h2></div>
      <p class="lede">Gold is assayed, refined, cast, hallmarked and polished. We build your systems the same way.</p>
    </div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

{founder_band(r)}
<section class="section section-raised" id="industries">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">Industries</p><h2>Built for businesses that run on conversations</h2></div>
      <p class="lede">We adapt every system to how your industry wins and keeps customers.</p>
    </div>
    <div class="inds">{inds}</div>
  </div>
</section>

<section class="section" id="insights">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">Insights</p><h2>Perspectives on growth, automation and AI</h2></div>
      <a class="text-link" href="insights.html">All insights {arrow()}</a>
    </div>
    <div class="insight-grid">{ins}</div>
  </div>
</section>
"""
    return (
        head(*PAGES["index"], r, "index.html", ld=[ld_org(), ld_website()],
             og=og_spec("index", "Marketing · Automation · AI", "Pure systems. Golden growth."))
        + header(r) + body + cta_band(r) + footer(r)
    )


def services_index():
    r = ""
    blocks = []
    for i, c in enumerate(CATEGORIES):
        cards = "".join(
            f"""<a class="svc-card" href="services/{s}.html">
          {thumb(s)}
          <h3>{e(SERVICES[s]["title"])}</h3>
          <p>{e(SERVICES[s]["short"])}</p>
          <span class="feature-go">Learn more {arrow()}</span>
        </a>""" for s in c["services"]
        )
        blocks.append(f"""<section class="section{' section-raised' if i % 2 else ''}" id="{c["slug"]}">
  <div class="wrap">
    <div class="section-head split">
      <div><p class="eyebrow">{i + 1:02d} · Capability</p><h2>{e(c["title"])}</h2></div>
      <p class="lede">{e(c["blurb"])}</p>
    </div>
    <div class="svc-grid">{cards}</div>
  </div>
</section>""")
    jump = "".join(f'<a class="chip" href="#{c["slug"]}">{e(c["title"])}</a>' for c in CATEGORIES)
    crumbs = [("Home", "index.html"), ("Services", None)]
    hero = page_hero("Services", "Everything you need to grow, connected",
                     "From the first ad a customer sees to the invoice they pay, we design, build and run the systems in between.",
                     crumbs, r, f'<div class="jump">{jump}</div>')
    items = {"@context": "https://schema.org", "@type": "ItemList", "name": "Hemavik services",
             "itemListElement": [{"@type": "ListItem", "position": i, "name": SERVICES[x]["title"], "url": url_of(f"services/{x}.html")}
                                 for i, x in enumerate((x for c in CATEGORIES for x in c["services"]), 1)]}
    return (head(*PAGES["services"], r, "services.html",
                 ld=[ld_page("CollectionPage", "Services", PAGES["services"][1], "services.html"), items, ld_crumbs(crumbs, "services.html")],
                 og=og_spec("services", "Services", "Everything you need to grow, connected"))
            + header(r, "services") + hero + "\n".join(blocks) + cta_band(r) + footer(r))


def service_page(slug):
    r = "../"
    s = SERVICES[slug]
    c = cat_of(slug)
    deliver = "".join(f'<div class="deliv"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in s["deliver"])
    steps = "".join(
        f'<li><span class="step-no">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(s["steps"])
    )
    outcomes = "".join(f"<li>{e(o)}</li>" for o in s["outcomes"])
    tools = "".join(f'<span class="chip">{e(t)}</span>' for t in s["tools"])
    related = "".join(
        f"""<a class="svc-card" href="{x}.html">{thumb(x)}<span class="feature-tag">{e(cat_of(x)["title"])}</span><h3>{e(SERVICES[x]["title"])}</h3><p>{e(SERVICES[x]["short"])}</p><span class="feature-go">Learn more {arrow()}</span></a>"""
        for x in s["related"]
    )
    extra = f'<div class="hero-cta"><a class="btn btn-primary" href="{r}contact.html">Talk to an expert</a><a class="btn btn-ghost" href="#deliver">What we deliver</a></div>'
    crumbs = [("Home", "index.html"), ("Services", "services.html"), (s["title"], None)]
    hero = page_hero(c["title"], e(s["title"]), s["short"], crumbs, r, extra, visual(slug))
    body = f"""<section class="section intro-block">
  <div class="wrap intro-grid">
    <p class="eyebrow">Overview</p>
    <p class="intro-text">{e(s["intro"])}</p>
  </div>
</section>

<section class="section section-raised" id="deliver">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What we deliver</p><h2>Inside {e(s["title"])}</h2></div>
    <div class="deliv-grid">{deliver}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">How it works</p><h2>From first call to running system</h2></div>
    <ol class="steps steps-4">{steps}</ol>
  </div>
</section>

<section class="section section-slate">
  <div class="wrap outcome-grid">
    <div><p class="eyebrow">What changes</p><h2>What you can expect</h2></div>
    <ul class="outcomes">{outcomes}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Works with</p>
      <h2>Tools and channels</h2>
      <div class="tool-row">{tools}</div>
    </div>
    <div>
      <p class="eyebrow">FAQ</p>
      <h2>Common questions</h2>
      <div class="faq">{faq_html(s["faqs"])}</div>
    </div>
  </div>
</section>

<section class="section section-raised">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Related services</p><h2>Works well with</h2></div>
    <div class="svc-grid">{related}</div>
  </div>
</section>
"""
    path = f"services/{slug}.html"
    service_ld = {
        "@context": "https://schema.org", "@type": "Service", "name": s["title"], "serviceType": s["title"],
        "description": s["intro"], "url": url_of(path), "provider": {"@type": "Organization", "@id": ORG_ID, "name": SITE["name"], "url": SITE["url"] + "/"},
        "areaServed": ["IN", "Worldwide"], "category": c["title"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["title"],
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in s["deliver"]]},
    }
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faqs"]]}
    return (head(s["seo_title"], s["seo_desc"], r, path, ld=[service_ld, faq_ld, ld_crumbs(crumbs, path)],
                 og=og_spec(slug, c["title"], s["title"]))
            + header(r, "services") + hero + body
            + cta_band(r, f'Talk to us about {s["title"]}') + footer(r))


IND_VIS = {"healthcare": "voice-ai", "real-estate": "crm-automation", "education": "commerce-memberships", "home-services": "reputation-management", "retail": "conversational-ai", "professional-services": "appointment-automation", "wellness": "marketing-automation", "automotive": "google-meta-ads"}


def industries_page():
    r = ""
    rows = "".join(
        f"""<article class="ind-row" id="{s}">
      <div><span class="cap-no">{i + 1:02d}</span><h2>{e(t)}</h2>{thumb(IND_VIS[s])}</div>
      <p class="ind-challenge">{e(p)}</p>
      <ul class="ind-list">{"".join(f"<li>{e(x)}</li>" for x in sol)}</ul>
    </article>""" for i, (s, t, p, sol) in enumerate(INDUSTRIES)
    )
    hero = page_hero("Industries", "Built for businesses that run on conversations",
                     "Every industry wins customers differently. We shape marketing, automation and AI agents around the way yours works.",
                     [("Home", "index.html"), ("Industries", None)], r)
    body = f'<section class="section"><div class="wrap ind-rows">{rows}</div></section>'
    crumbs = [("Home", "index.html"), ("Industries", None)]
    return (head(*PAGES["industries"], r, "industries.html",
                 ld=[ld_page("CollectionPage", "Industries", PAGES["industries"][1], "industries.html"), ld_crumbs(crumbs, "industries.html")],
                 og=og_spec("industries", "Industries", "Built for businesses that run on conversations"))
            + header(r, "industries") + hero + body + cta_band(r) + footer(r))


def nice_date(iso):
    return date.fromisoformat(iso).strftime("%d %b %Y").lstrip("0")


def insight_card(a, r):
    return f"""<a class="insight" href="{r}insights/{a["slug"]}.html">
      <div class="cover cover-{a["slug"]}" aria-hidden="true">{MOUNTAINS}<span>{e(a["tag"])}</span></div>
      <span class="feature-tag">{e(a["tag"])} · <time datetime="{a["date"]}">{nice_date(a["date"])}</time> · {e(a["read"])}</span>
      <h3>{e(a["title"])}</h3>
      <p>{e(a["summary"])}</p>
      <span class="feature-go">Read {arrow()}</span>
    </a>"""


def insights_page():
    r = ""
    hero = page_hero("Insights", "Perspectives on growth, automation and AI",
                     "Practical thinking from the systems we build every day.",
                     [("Home", "index.html"), ("Insights", None)], r)
    body = f'<section class="section"><div class="wrap"><div class="section-head"><p class="eyebrow">Latest</p><h2>All articles</h2></div><div class="insight-grid">{"".join(insight_card(a, r) for a in INSIGHTS)}</div></div></section>'
    crumbs = [("Home", "index.html"), ("Insights", None)]
    return (head(*PAGES["insights"], r, "insights.html",
                 ld=[ld_page("CollectionPage", "Insights", PAGES["insights"][1], "insights.html"), ld_crumbs(crumbs, "insights.html")],
                 og=og_spec("insights", "Insights", "Perspectives on growth, automation and AI"))
            + header(r, "insights") + hero + body + cta_band(r) + footer(r))


def article_page(a):
    r = "../"
    paras = "".join(f"<p>{e(p)}</p>" for p in a["body"])
    others = "".join(insight_card(x, r) for x in INSIGHTS if x["slug"] != a["slug"])
    crumbs = [("Home", "index.html"), ("Insights", "insights.html"), (a["title"], None)]
    hero = page_hero(f'{a["tag"]} · {nice_date(a["date"])} · {a["read"]}', e(a["title"]), a["summary"],
                     [("Home", "index.html"), ("Insights", "insights.html"), (a["tag"], None)], r,
                     f'<p class="byline">By {e(SITE["author"])} · <time datetime="{a["date"]}">{nice_date(a["date"])}</time></p>')
    body = f"""<section class="section"><div class="wrap"><article class="article">{paras}</article></div></section>
<section class="section section-raised"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Keep reading</p><h2>More insights</h2></div>
  <div class="insight-grid insight-grid-2">{others}</div>
</div></section>
"""
    path = f'insights/{a["slug"]}.html'
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["title"], "description": a["summary"],
           "datePublished": a["date"], "dateModified": a["date"], "url": url_of(path), "mainEntityOfPage": url_of(path),
           "image": f'{SITE["url"]}/assets/og/{a["slug"]}.png', "articleSection": a["tag"], "inLanguage": "en",
           "wordCount": sum(len(p.split()) for p in a["body"]),
           "author": {"@type": "Organization", "name": SITE["author"], "url": SITE["url"] + "/about.html"},
           "publisher": {"@id": ORG_ID, "@type": "Organization", "name": SITE["name"],
                         "logo": {"@type": "ImageObject", "url": SITE["url"] + "/assets/logo/hemavik-logo-512.png"}}}
    return (head(a["seo_title"], a["seo_desc"], r, path, ld=[art, ld_crumbs(crumbs, path)],
                 og=og_spec(a["slug"], f'Insights · {a["tag"]}', a["title"]), ogtype="article")
            + header(r, "insights") + hero + body + cta_band(r) + footer(r))


def about_page():
    r = ""
    steps = "".join(
        f'<li><span class="step-no">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS)
    )
    hero = page_hero("About Hemavik", "Named for gold. Built for purity.",
                     "Hemavik is a digital marketing, automation and AI company. We build connected growth systems for businesses that are ready to stop running on spreadsheets and memory.",
                     [("Home", "index.html"), ("About", None)], r)
    body = f"""<section class="section">
  <div class="wrap about-grid">
    <div class="about-mark" aria-hidden="true"><svg><use href="#hv-mark"/></svg></div>
    <div class="about-copy">
      <p class="eyebrow">The name</p>
      <h2>What Hemavik means</h2>
      <p><strong>Hemavik</strong> comes from <em>hema</em> (हेम), the Sanskrit word for gold. It stands for three ideas that guide our work.</p>
      <div class="meaning">
        <div><h3>Made of gold</h3><p>Systems that hold their value and keep paying back long after launch.</p></div>
        <div><h3>Purity</h3><p>Like fine gold hallmarked 999: clean automations, clean data, nothing extra.</p></div>
        <div><h3>Lord Shiva</h3><p>Stillness at the centre of constant motion. Calm, reliable systems behind a busy business.</p></div>
      </div>
      <p>Our logo is a temple gateway shaped like an H, inside a coin for <em>hema</em>, with Shiva's crescent above and the third eye below. Our colours come from Kailash: snow, glacier ice and slate shadow.</p>
    </div>
  </div>
</section>

<section class="section section-raised founder-about" id="founder">
  <div class="wrap founder-grid">
    <figure class="founder-photo">{picture(r, FOUNDER["photo"], f'{FOUNDER["name"]}, {FOUNDER["role"]} of Hemavik')}</figure>
    <div class="founder-copy">
      <p class="eyebrow">Founder</p>
      <h2>{e(FOUNDER["name"])}</h2>
      {"".join(f"<p>{e(x)}</p>" for x in FOUNDER["bio"])}
      <blockquote><p>{e(FOUNDER["quote"])}</p></blockquote>
    </div>
  </div>
</section>

<section class="stats-band"><div class="wrap stats">{"".join(stat_html(n, t) for n, t in COMMITMENTS)}</div></section>

<section class="section">
  <div class="wrap">
    <div class="section-head split"><div><p class="eyebrow">Values</p><h2>How we work</h2></div></div>
    <div class="values">
      <div class="value"><h3>You own everything</h3><p>Accounts, data, workflows and ad accounts are in your name. You get documentation for all of it.</p></div>
      <div class="value"><h3>One connected system</h3><p>Marketing, sales, service and payments share one database, so nothing falls between tools.</p></div>
      <div class="value"><h3>Plain language</h3><p>Reports and recommendations you can understand without a technical dictionary.</p></div>
      <div class="value"><h3>Built and run by one team</h3><p>The people who design your system are the people who support it.</p></div>
    </div>
  </div>
</section>

<section class="section section-glacier">
  <div class="wrap">
    <div class="section-head split"><div><p class="eyebrow">Our approach</p><h2>Refined like gold, in five steps</h2></div></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>
"""
    crumbs = [("Home", "index.html"), ("About", None)]
    return (head(*PAGES["about"], r, "about.html",
                 ld=[ld_page("AboutPage", "About Hemavik", PAGES["about"][1], "about.html"), ld_org(), ld_crumbs(crumbs, "about.html")],
                 og=og_spec("about", "About Hemavik", "Named for gold. Built for purity."))
            + header(r, "about") + hero + body + cta_band(r) + footer(r))


def contact_page():
    r = ""
    opts = "".join(f"<option>{e(SERVICES[s]['title'])}</option>" for c in CATEGORIES for s in c["services"])
    hero = page_hero("Contact", "Let's talk about your growth",
                     "Tell us where your leads come from and what happens to them today. We reply within one working day.",
                     [("Home", "index.html"), ("Contact", None)], r)
    body = f"""<section class="section">
  <div class="wrap contact-grid">
    <div class="contact-copy">
      <div class="speak">
        {picture(r, FOUNDER["photo_alt"], FOUNDER["name"], "speak-photo", sizes="96px")}
        <p><small>You will speak with</small><b>{e(FOUNDER["name"])}</b><span>{e(FOUNDER["role"])}, Hemavik</span></p>
      </div>
      <h2>What happens next</h2>
      <ol class="next-steps">
        <li><b>We reply within one working day</b> with a time for a 30-minute call.</li>
        <li><b>Free assay call.</b> We review your current tools, lead flow and campaigns together.</li>
        <li><b>Written blueprint.</b> You receive a plan with scope, timeline and a fixed quote.</li>
      </ol>
      <dl class="contact-list">
        <div><dt>Email</dt><dd><span class="selectable">{e(SITE["email"])}</span></dd></div>
        <div><dt>Hours</dt><dd>{e(SITE["hours"])}</dd></div>
        <div><dt>Clients</dt><dd>India and worldwide, remotely</dd></div>
      </dl>
    </div>

    <!-- Set data-endpoint to your automation webhook URL to receive submissions. -->
    <form class="contact-form" id="contact-form" data-endpoint="" novalidate>
      <div class="field-row">
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <div class="field"><label for="f-service">What are you interested in?</label>
        <select id="f-service" name="service">{opts}<option>A complete growth system</option><option>Not sure yet</option></select>
      </div>
      <div class="field"><label for="f-msg">Where do your leads come from today?</label><textarea id="f-msg" name="message" rows="5"></textarea></div>
      <button class="btn btn-primary" type="submit" id="f-submit">Request my call</button>
      <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""
    crumbs = [("Home", "index.html"), ("Contact", None)]
    return (head(*PAGES["contact"], r, "contact.html",
                 ld=[ld_page("ContactPage", "Contact Hemavik", PAGES["contact"][1], "contact.html"), ld_crumbs(crumbs, "contact.html")],
                 og=og_spec("contact", "Contact", "Book a free strategy call"))
            + header(r) + hero + body + footer(r))


def not_found_page():
    r = "/"
    links = "".join(f'<a class="chip" href="/{h}">{e(t)}</a>' for t, h in
                    [("Home", ""), ("Services", "services.html"), ("Industries", "industries.html"), ("Insights", "insights.html"), ("Contact", "contact.html")])
    hero = page_hero("Error 404", "This page has moved or never existed",
                     "The link may be old or mistyped. These pages will get you back on track.",
                     [("Home", "index.html"), ("Page not found", None)], "/", f'<div class="jump">{links}</div>')
    return head("Page not found", "The page you are looking for could not be found.", r, "404.html", noindex=True) + header(r) + hero + footer(r)


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main():
    pages = [
        write("index.html", home()),
        write("services.html", services_index()),
        write("industries.html", industries_page()),
        write("insights.html", insights_page()),
        write("about.html", about_page()),
        write("contact.html", contact_page()),
    ]
    for c in CATEGORIES:
        for s in c["services"]:
            pages.append(write(f"services/{s}.html", service_page(s)))
    for a in INSIGHTS:
        pages.append(write(f"insights/{a['slug']}.html", article_page(a)))

    write("404.html", not_found_page())
    today = date.today().isoformat()
    urls = "".join(
        f"  <url><loc>{url_of(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in pages
    )
    write("site.webmanifest", json.dumps({
        "name": SITE["name"], "short_name": SITE["name"], "start_url": "/", "display": "browser",
        "background_color": "#F5F8FB", "theme_color": "#1F2E44",
        "icons": [{"src": "/assets/logo/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "/assets/logo/hemavik-logo-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=2) + "\n")
    write("_build/og-pages.json", json.dumps(OG, indent=2, ensure_ascii=False) + "\n")
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print(f"Built {len(pages)} pages")


if __name__ == "__main__":
    main()
