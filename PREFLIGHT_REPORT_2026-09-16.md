# HTML PRE-FLIGHT REPORT

**Project:** 心理学研究者的 AI Start Guide  
**Version:** v0.10 render-ready  
**Date:** 2026-09-16

## Passed

- `_quarto.yml` YAML parse: PASS
- `products.yml`: PASS
- `providers.yml`: PASS
- `tools.yml`: PASS
- Public render set: 26 reader-facing pages
- Public source-link existence check: PASS
- Pandoc structural pre-render: 26/26 pages parsed
- Generated-preview internal HTML links: 0 missing
- Python teaching script syntax: previously PASS

## Fixed in this pass

- Stale sidebar filenames after API chapter insertion
- Missing API research-script page in sidebar
- Wrong Code Agent / Work Agent / Privacy / Checklist chapter numbers
- Internal audit pages still exposed in public sidebar
- DeepSeek product page linking to internal field-test page
- Invalid future GitHub username placeholders in local preview config

## Pending real Quarto render

Quarto-specific rendering still requires local verification for:

- Mermaid diagram rendering
- Search index
- Quarto callout styling
- Code-copy buttons
- navbar/sidebar responsive behavior
- table behavior at mobile width

Use `docs/FIRST_RENDER_WINDOWS.md` for the next step.
