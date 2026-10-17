// Renders social share images (assets/og/*.png) and PNG icons with Playwright.
// Run after build.py:  node _build/og-images.cjs
// Needs Playwright with Chromium (npm i -D playwright, or a global install).
const fs = require('fs');
const path = require('path');

function loadPlaywright() {
  try { return require('playwright'); } catch (_) {}
  const { execSync } = require('child_process');
  const root = execSync('npm root -g').toString().trim();
  return require(path.join(root, 'playwright'));
}

const ROOT = path.resolve(__dirname, '..');
const pages = JSON.parse(fs.readFileSync(path.join(__dirname, 'og-pages.json'), 'utf8'));
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const MARK = `<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="none" stroke="currentColor" stroke-width="2.5"/>
<rect x="19" y="18" width="5" height="28" rx="1" fill="currentColor"/><rect x="40" y="18" width="5" height="28" rx="1" fill="currentColor"/>
<rect x="19" y="32" width="26" height="4" fill="currentColor"/><path d="M26 24 A6 6 0 0 0 38 24 A6 3.5 0 0 1 26 24 Z" fill="currentColor"/>
<circle cx="32" cy="41" r="2.2" fill="currentColor"/></svg>`;

const PEAKS = `<svg class="peaks" viewBox="0 0 1440 360" preserveAspectRatio="xMidYMax slice">
<path fill="#94A9BF" opacity=".45" d="M0 250 L110 190 L200 222 L320 128 L410 176 L520 96 L610 158 L720 70 L820 146 L930 104 L1010 150 L1090 58 L1170 140 L1260 112 L1360 160 L1440 130 V360 H0Z"/>
<path fill="#F5F8FB" opacity=".9" d="M1090 58 L1062 100 L1078 94 L1090 108 L1104 92 L1120 100 Z M720 70 L698 104 L712 98 L724 110 L738 96 Z"/>
<path fill="#A5BED4" opacity=".6" d="M0 300 L140 232 L260 268 L380 196 L470 240 L600 176 L700 232 L800 160 L900 224 L1010 184 L1120 244 L1230 196 L1340 252 L1440 222 V360 H0Z"/>
<path fill="#F5F8FB" d="M0 326 C120 296 220 318 320 304 C440 286 520 318 640 300 C760 282 860 312 980 296 C1100 280 1200 310 1320 296 C1380 290 1420 298 1440 294 V360 H0Z"/></svg>`;

const FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=JetBrains+Mono:wght@500&display=block">';

const card = ({ eyebrow, title }) => `<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;color:#1F2E44;
  background:linear-gradient(180deg,#C9D6E3 0%,#DCE6F0 55%,#F5F8FB 100%);font-family:Marcellus,Georgia,serif}
.peaks{position:absolute;left:0;right:0;bottom:0;width:100%;height:46%}
.in{position:relative;padding:64px 72px;height:100%;display:flex;flex-direction:column}
.logo{display:flex;align-items:center;gap:16px;color:#1F2E44}
.logo svg{width:60px;height:60px;color:#3F6189}
.logo b{font-weight:400;font-size:34px;letter-spacing:.22em}
.eb{margin-top:auto;font:500 22px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#3F6189}
h1{font-weight:400;font-size:${title.length > 48 ? 58 : 72}px;line-height:1.06;max-width:980px;margin-top:18px}
.url{position:absolute;right:72px;top:78px;font:500 20px 'JetBrains Mono',monospace;color:#536379;letter-spacing:.06em}
.thread{height:3px;width:120px;background:#A97C22;margin-top:28px;margin-bottom:150px}
</style></head><body>${PEAKS}<div class="in">
<div class="logo">${MARK}<b>HEMAVIK</b></div><span class="url">hemavik.com</span>
<p class="eb">${esc(eyebrow)}</p><h1>${esc(title)}</h1><div class="thread"></div></div></body></html>`;

const icon = (size, bg, fg, pad) => `<!doctype html><html><head><style>*{margin:0}
body{width:${size}px;height:${size}px;background:${bg};display:grid;place-items:center}
svg{width:${size - pad * 2}px;height:${size - pad * 2}px;color:${fg}}</style></head><body>${MARK}</body></html>`;

(async () => {
  const { chromium } = loadPlaywright();
  const opts = fs.existsSync('/opt/pw-browsers/chromium') ? { executablePath: '/opt/pw-browsers/chromium' } : {};
  const browser = await chromium.launch(opts);
  const outDir = path.join(ROOT, 'assets/og');
  fs.mkdirSync(outDir, { recursive: true });

  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [key, spec] of Object.entries(pages)) {
    await page.setContent(card(spec), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(outDir, `${key}.png`) });
  }
  for (const [file, size, bg, fg, pad] of [
    ['apple-touch-icon.png', 180, '#1F2E44', '#A5BED4', 26],
    ['favicon-32.png', 32, '#1F2E44', '#A5BED4', 3],
    ['hemavik-logo-512.png', 512, '#F5F8FB', '#3F6189', 64],
  ]) {
    const p = await browser.newPage({ viewport: { width: size, height: size } });
    await p.setContent(icon(size, bg, fg, pad));
    await p.screenshot({ path: path.join(ROOT, 'assets/logo', file) });
    await p.close();
  }
  await browser.close();
  console.log(`Rendered ${Object.keys(pages).length} share images and 3 icons`);
})();
