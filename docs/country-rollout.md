# Country website governance and rollout

Verified GitHub organisation owners with a separate country `www`: skunkworks-aus, skunkworks-cameroon, skunkworks-malawi, skunkworks-nigeria, skunkworks-portugal, skunkworks-swaziland, skunkworks-uganda, skunkworks-usa.

The source of truth for design tokens and shared chrome is `dist/`. Publish changes to the theme via review and CI, then use scheduled/dispatch country sync PRs. Each country repository is responsible for local navigation copy, contact channels, country identity (including the header's country label), domain verification, bilingual pages where appropriate, accessibility, and country-specific legal claims. Domain/store links MUST NOT be invented, and the ecommerce catalogue and checkout remain on Shopify.

**Regions without a GitHub organisation**: Botswana, Rwanda, Mexico or others should be onboarded only when the owning organisation and repository are created through a GitHub administrator. A website in another organisation is not a substitute for explicit country ownership.
