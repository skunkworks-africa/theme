# Country website registry and onboarding

This inventory is derived from accessible GitHub installations as of 2026-10-30. Every listed **country-specific organisation** has a dedicated public `www` repository. It does not include other Skunkworks business-unit organisations (Academy, Commerce, Media, Domains, Labs, etc.).

| Country | GitHub repository | Canonical currently configured | Shared theme sync |
|---|---|---|---|
| Australia | [skunkworks-aus/www](https://github.com/skunkworks-aus/www) | https://www.skunkworksau.com.au/ | corporate |
| Cameroon | [skunkworks-cameroon/www](https://github.com/skunkworks-cameroon/www) | https://skunkworks-cameroon.github.io/www/ | corporate |
| Malawi | [skunkworks-malawi/www](https://github.com/skunkworks-malawi/www) | https://skunkworks.mw/ | corporate |
| Nigeria | [skunkworks-nigeria/www](https://github.com/skunkworks-nigeria/www) | https://skunkworks-nigeria.github.io/www/ | corporate |
| Portugal | [skunkworks-portugal/www](https://github.com/skunkworks-portugal/www) | https://skunkworks-portugal.github.io/www/ | tokens-only |
| Eswatini / Swaziland | [skunkworks-swaziland/www](https://github.com/skunkworks-swaziland/www) | https://skunkworks-swaziland.github.io/www/ | corporate |
| Uganda | [skunkworks-uganda/www](https://github.com/skunkworks-uganda/www) | https://www.skunkworks.ug/ | corporate |
| United States | [skunkworks-usa/www](https://github.com/skunkworks-usa/www) | https://skunkworksus.com/ | corporate |

## Theme distribution

All countries run `.github/workflows/sync-skunkworks-theme.yml` on Mondays at 05:23 UTC and manually via `workflow_dispatch`. The workflow pins the reviewed theme commit and proposes CSS-only updates through pull requests. Corporate sites share `styles.css`, `adaptive-shell.css`, `hero-chat.css`, and `tokens.css`. Portugal retains an existing bilingual site and consumes the shared tokens, with an additional locally governed monochrome alignment stylesheet.

## Country ownership and launch gates

1. Preserve the approved skunk logo, and use the exact country name in the header and footer rather than the African parent name. Eswatini uses **Swaziland** as its header designation per brand instructions.
2. Keep accurate self-referencing canonical URLs; do not switch a CNAME without confirmed DNS and HTTPS.
3. Never invent offices, legal entities, local resellers, vendor accreditations, taxes, or Shopify storefronts. Global commerce may be linked with a regional eligibility disclosure.
4. Mobile navigation, keyboard focus, content contrast, reduced motion, accessible buttons, and 320px responsive layout must pass testing.
5. Run `node scripts/validate-site.mjs`, check GitHub Pages release status and actual public HTTP response.
6. To onboard another country, a GitHub administrator must create the country organisation and `www` repo first, then install the connector, provide verified domain/contact details and enroll it in this registry.

Known separate expansion interests without a corresponding accessible country organisation include Botswana, Rwanda and Mexico; do **not** represent these as deployed country sites.

## Operational exception
Australia is currently configured on `www.skunkworksau.com.au`. Requested `www.skunkworksau.au` must not replace the live CNAME until DNS/HTTPS and redirects are ready. See https://github.com/skunkworks-aus/www/issues/2.
