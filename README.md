# The Dead Media Vault — website

Static marketing/funnel site for the Dead Media Vault project, published via
GitHub Pages at **https://ultimatejordan.github.io/dead-media-vault/**.

## What's here

- `index.html` — vault home: four brand cards, how-it-works, free teaser CTA
- `brands/gilt-grotesque.html` — Vintage Design Archive (botanicals LIVE, ukiyo-e soon)
- `brands/dread-archive.html` — Public Domain Horror Art (Pulp Terror soon)
- `brands/primary-source.html` — Historical Documents Archive (antique maps soon)
- `brands/dead-wax-society.html` — Public Domain Sample Packs (in the works)
- `privacy.html` — plain-language privacy policy (needed for platform API reviews)
- `assets/img/gallery/` — 40 web-optimized teaser plates (1200px, ~7.5MB total)
- `assets/downloads/` — 4 free teaser ZIPs (258MB total; the already-built dist zips)

## Buy-link policy

Only products **verified live on Gumroad** get buy links:
- Personal $16 → https://tacatshi.gumroad.com/l/xvmoil
- Commercial $59 → https://tacatshi.gumroad.com/l/victorian-botanicals-commercial
- Free sampler → https://tacatshi.gumroad.com/l/free-victorian-botanicals-sampler

Pulp Terror / Ukiyo-e / Antique Maps are queued for the Gumroad retry and are
marked "being shelved" with free teaser downloads — buy links get added the
moment each pack goes live. Never link a dead URL.

## Brand separation

This repo is fully separate from `tacatshi-books`. One repo per brand.
Nothing secret lives here — all assets are public-facing.

## Deploy

Push to `main`; GitHub Pages serves from the repo root. Verify with:
`curl -sI https://ultimatejordan.github.io/dead-media-vault/` → 200.
