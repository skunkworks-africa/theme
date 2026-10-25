# Skunkworks Global Web Design System

Central brand, design and governance repository for Skunkworks corporate and country reseller websites. Shopify storefronts remain separate commerce implementations.

**Public documentation:** https://theme.skunkworks.africa/ (subject to GitHub Pages and DNS activation).

## Sources
- Primary: https://github.com/skunkworks-africa/www/tree/c71e2f71d4d48e5c7d575e7927cc966c0e4df2fb
- Brand assets: `www/assets` at the pinned commit, indexed in `brand/assets.json`.
- Secondary Shopify reference: https://github.com/skunkworks-africa/shopify

## Files
- `tokens.css` — monochrome brand tokens and button/shell primitives.
- `brand/assets.json` — original pinned logos and favicons.
- `docs/standards.md` — country-site standards and QA criteria.
- `scripts/validate.mjs` — no-dependency validation.
- `.github/workflows/validate.yml` — automated checks.
- `index.html` — public reference site.

Run `node scripts/validate.mjs`. GitHub Pages should publish from `main` repository root. Country-specific domain, locale, legal information and Shopify links belong to each country's website repository.
