# Skunkworks global country-theme distribution

Authoritative theme snapshot for all Skunkworks country `www` sites. Sync the immutable templates into country repositories through the `Country theme synchronisation` GitHub Actions workflow.

- `styles.css` — universal corporate layout and component primitives
- `adaptive-shell.css` — monochrome global header, mobile shell and footer
- `hero-chat.css` — shared assistant element design
- `tokens.css` — monochrome tokens, typography, focus and motion controls

## Synchronisation contract
The `skunkworks-africa/theme` repository is the canonical distributor; `skunkworks-africa/www` is the reference implementation. The `dist` directory snapshots approved corporate CSS until the main site is wired to consume the same version. Country websites fetch these CSS files from `dist` and open pull requests with the updated assets. They must not sync their `index.html`, local service descriptions, legal notices, custom domains, CNAME, store URLs, or contacts.

Country `www` repos may select `corporate` mode (all four stylesheets) or `tokens-only` (Portugal maintains its own Portuguese bilingual presentation). Use the site CSS order `styles.css`, `adaptive-shell.css`, `hero-chat.css`; `tokens.css` is independent. Existing local files must be aligned before enabling updates.

Scheduled checks create pull requests rather than silently modifying production. GitHub Actions must allow read/write access and pull-request creation; ensure this setting is enabled for each repository, otherwise the workflow will fail visibly. Validate accessible links, light/dark mode, locale and local SEO before merging.
