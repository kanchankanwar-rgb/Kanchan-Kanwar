# Hemavik website & brand board

Website and brand identity for **Hemavik**: digital marketing, paid ads, CRM and marketing automation, websites, AI workflows and Voice AI.

The name comes from the Sanskrit *hema* (gold) and stands for three ideas: **made of gold** (lasting value), **purity** (clean systems, the 999 hallmark) and **Lord Shiva** (stillness behind motion: crescent, third eye, Kailash colours).

## Site map (20 pages)

| Page | File |
| --- | --- |
| Home | `index.html` |
| All services | `services.html` |
| 11 service pages | `services/*.html` |
| Industries | `industries.html` |
| Insights + 3 articles | `insights.html`, `insights/*.html` |
| About | `about.html` |
| Contact | `contact.html` |
| Brand guidelines (internal) | `brand-board.html` |

Services are grouped into four capabilities:

- **Growth & Marketing**: Digital Marketing, Google & Meta Ads, Reputation & Reviews
- **Customer Engagement**: CRM & Sales Automation, Marketing Automation, Appointments & Booking
- **Digital Experience**: Website & Funnel Development; Payments, Courses & Communities
- **AI & Automation**: AI-Powered Workflows, Voice AI Agents, Conversational AI & Chat

## Editing content

All copy (services, industries, articles, FAQs, contact details) lives in **`_build/content.py`**. The pages are generated from it, so header, mega-menu and footer stay identical everywhere.

```bash
cd hemavik
python3 _build/build.py      # regenerates every page, sitemap.xml and robots.txt
```

Do not edit the generated `.html` files by hand (except `brand-board.html`); changes would be overwritten on the next build. Styles live in `assets/css/hemavik.css` (brand tokens) and `assets/css/site.css` (layout).

## Brand at a glance

Colours are sampled from an image of Shiva meditating on Kailash: snow, clouds, glacier ice and slate shadow. Gold remains only as a small highlight for *hema*.

| Token | Hex | Use |
| --- | --- | --- |
| Kailash Snow | `#F5F8FB` | Page background |
| Cloud Mist | `#E7EEF5` | Cards, panels, form fields |
| Glacier | `#A5BED4` | Section bands, logo on slate |
| Himalaya Sky | `#94A9BF` | Gradients, atmosphere |
| Marble | `#A0A3A9` | Dividers, icons |
| Neelkanth Blue | `#3F6189` | Logo, buttons, links |
| Shila Slate | `#1F2E44` | Text, dark bands, footer |
| Hema Gold | `#A97C22` | 999 stamp, one highlight per page |

Fonts (Google Fonts): **Marcellus** (headlines), **Manrope** (body), **JetBrains Mono** (labels).

## Before going live

1. **Email**: `hello@hemavik.com` is a placeholder. Change `SITE["email"]` in `_build/content.py` and the `email` variable in `assets/js/site.js`, then rebuild.
2. **Contact form**: set `data-endpoint` on the form in the `contact_page()` template in `_build/build.py` to your automation webhook URL, then rebuild. The form POSTs JSON: `name, company, email, phone, service, message, source, page, submittedAt`. Until it is set, the form asks visitors to email you.
3. **Logo SVGs**: the lockups use live text in Marcellus. For print, convert text to outlines in Figma or Illustrator.

## Deploy

No server code. Upload the `hemavik/` folder (you can leave out `_build/`) to any static host such as Netlify, Vercel, Cloudflare Pages or cPanel `public_html`, and point `hemavik.com` at it. Preview locally:

```bash
cd hemavik && python3 -m http.server 8000
```
