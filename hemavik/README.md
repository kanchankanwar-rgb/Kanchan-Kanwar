# Hemavik website & brand board

Static website and brand identity for **Hemavik**: GoHighLevel, n8n automation and marketing.

The name comes from the Sanskrit *hema* (gold) and stands for three ideas: **made of gold** (lasting value), **purity** (clean systems, the 999 hallmark), and **Lord Shiva** (stillness behind motion: crescent, third eye, Neelkanth indigo).

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The website (one page: hero, services, process, about, FAQ, contact) |
| `brand-board.html` | Brand guidelines: name, logo, colour, type, voice, components, applications |
| `assets/css/hemavik.css` | Brand tokens (colours, fonts, buttons, chips, hallmark). Shared by both pages |
| `assets/css/site.css` | Website layout |
| `assets/js/site.js` | Mobile menu and contact form |
| `assets/logo/` | Logo lockups (dark, light), mark (gold, indigo), favicon |

## Brand at a glance

| Token | Hex | Use |
| --- | --- | --- |
| Neelkanth | `#0E1630` | Primary background |
| Hema Gold | `#D4A63A` | Logo, buttons, highlights |
| Kailash Ivory | `#F6F1E4` | Text on dark, light sections |
| Bhasma Ash | `#A7ADBD` | Secondary text |
| Deep Gold | `#9C7420` | Gold on ivory |
| Ganga Teal | `#3FA7A0` | Live / success states |

Fonts (Google Fonts): **Marcellus** (headlines), **Manrope** (body), **JetBrains Mono** (labels).

## Before going live

1. **Email**: `hello@hemavik.com` is a placeholder. Replace it in `index.html`, `assets/js/site.js` and `brand-board.html` if you use a different address.
2. **Contact form**: set `data-endpoint` on `<form id="contact-form">` in `index.html` to an n8n Webhook node URL (or a GoHighLevel inbound webhook). The form POSTs JSON: `name, email, phone, service, message, source, submittedAt`. Until it is set, the form tells visitors to email you.
3. **Logo SVGs**: the lockup files use live text in Marcellus. For print, open them in Figma/Illustrator and convert text to outlines.

## Deploy

No build step. Upload the `hemavik/` folder to any static host (Netlify, Vercel, Cloudflare Pages, GitHub Pages, or your cPanel `public_html`) and point `hemavik.com` at it. To preview locally:

```bash
cd hemavik && python3 -m http.server 8000
```
