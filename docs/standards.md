# Skunkworks corporate and reseller web standards

## Authority and separation
The corporate `www` pinned commit is the authoritative design reference. The Shopify repository is a secondary cross-channel reference, **not** the website template. Store catalogue, prices, cart and checkout remain within Shopify.

## Brand
Use only approved original black/white logos and favicons from `brand/assets.json`; preserve aspect ratio, clear space and legibility. Never stretch, recolour, add flags inside the logo, or substitute an unapproved wordmark. Country designation is text adjacent to the shared brand, not a modification to the logo.

## Visual tokens
Corporate reference: white `#fff`, black `#000`, muted foreground opacity 0.66, subtle lines, 1240px content shell, 74px desktop header, 20px cards, 12px controls, Inter with system fallbacks. Automatic dark mode, explicit theme overrides where supported, no blue or colored header/footer. Use `tokens.css`.

## Components
Responsive sticky header, branded logo home link, accessible navigation and scrolling mobile menu, skip-to-content link, compact viewport-aware hero, consistent service cards, primary/secondary CTAs, consistent global footer. Use semantic landmarks and keyboard-operable controls. Avoid fixed heights that crop content. No nonfunctional placeholder controls or sample customer data.

## Regionalization
Each country site owns its localized domain, locale (`lang`), region-specific services, legal entity claims, contacts, currency where displayed, privacy notices, canonical/hreflang and local SEO. Only state partner status and legal registrations that are verified for that specific entity. Country site Store links must lead to its assigned Shopify domain; do not embed Shopify checkout or replicate catalogue data.

## Quality gates
WCAG 2.2 AA targets: normal text contrast >=4.5:1; large text >=3:1; keyboard focus visible; 320px reflow without horizontal overflow; labels, alt text and navigation semantics; reduced-motion support. Check light/dark, desktop/tablet/mobile, functional links and forms, Lighthouse and axe where browser automation is available. CI validates local files; external site compliance requires separate deployment/browser audits.

## Change governance
Update the shared design system first, review through pull requests, tag releases, then roll out versioned changes to country sites. Preserve source attribution and do not automatically deploy design changes to every reseller without site-specific verification.

## Country theme synchronisation
Country repositories sync versioned corporate CSS from `dist/` using a scheduled and manually dispatchable GitHub Actions workflow that opens a review PR. HTML pages, contacts, country labels, CNAME, localized policies and Shopify destinations are never overridden. Each site must run local conformance checks on PRs before merging. The parent brand mark is shared; the country label next to it must refer to the actual location.
