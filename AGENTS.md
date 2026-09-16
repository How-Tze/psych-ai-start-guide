# AGENTS.md

This file contains repository-level instructions for coding / research agents working on **psych-ai-start-guide**.

## Mission

Maintain and improve a task-oriented Quarto Start Guide for psychology and social-science researchers learning to use current AI products, APIs, Harnesses and research workflows.

The site is a dynamic companion to a separate, more stable handbook. Optimize for clarity, maintainability, factual freshness and realistic research use — not product coverage.

## Non-negotiable editorial architecture

Keep the primary reader flow task-oriented, not vendor-oriented:

> chat → Project/Workspace → source-grounded reading → Deep Research → API → Code Agent/Harness → Work Agent → privacy/checklist

Product pages are secondary reference pages.

Preserve the conceptual distinction:

> Product UI → API → Harness → Workflow

Never collapse these into a single concept.

## What to optimize for

- A new psychology researcher can decide what to use next.
- Mainland-China readers have realistic domestic options.
- International products are still represented accurately.
- Readers understand why APIs exist and when they are worth using.
- Readers understand that model choice and work environment are different decisions.
- The guide remains useful even as product interfaces change.

## What NOT to do

Do not:

- turn the site into a vendor encyclopedia;
- add tools merely because they are popular;
- create “best AI” rankings;
- copy long vendor setup instructions;
- hard-code volatile pricing into evergreen prose unless necessary;
- add engineering complexity without a maintenance benefit;
- modify the frozen main-handbook files unless explicitly asked;
- expose credentials or private research materials;
- infer undocumented product behavior when official sources disagree.

## Dynamic fact verification

Any substantive claim about a current product, plan, model, API, pricing, regional availability, project limit, or feature must be checked against current sources before editing.

Preferred evidence order:

1. official product / API docs;
2. official help center / release notes;
3. official engineering / product blog;
4. community reports for real-world friction only.

When dynamic data are updated, preserve or update the relevant `last_checked` field/date.

If official sources conflict, do not silently resolve the conflict. Either:

- state the uncertainty;
- choose the clearly documented stable route and note why;
- or leave the disputed detail out.

## API guidance rules

Teach APIs through practical decisions, not protocol trivia.

Three useful levels:

1. no-code BYOK tool;
2. BYOK multi-model client as a conceptual example;
3. reproducible research scripting / batch processing.

The research-script example should emphasize:

- fixed inputs;
- explicit prompt/model configuration;
- raw model output preservation;
- append-only or otherwise auditable result storage;
- error logging;
- resumability;
- run metadata;
- separation between reproducibility and substantive validity.

Never imply that reproducible LLM output automatically constitutes valid psychological measurement or qualitative coding.

## Security and privacy

Never create or commit:

- real API keys;
- `.env` contents;
- tokens / cookies;
- payment information;
- private screenshots with account identifiers;
- participant-identifiable data;
- confidential manuscripts or collaborator files.

Before commits that add examples or screenshots, inspect for secrets and local absolute paths.

Prefer placeholders such as:

```text
YOUR_API_KEY
```

or environment-variable examples.

## Open-science principle

The project supports a future connection between AI-assisted local project maintenance and open science.

AI may help prepare shareable research assets, but do not automate or assert decisions about:

- de-identification sufficiency;
- participant consent scope;
- redistribution rights;
- ethical suitability of release.

Those remain researcher decisions.

## Quarto workflow

Before finalizing a content or layout change:

```powershell
quarto preview
```

Check representative pages, then:

```powershell
quarto render
```

Current publication workflow:

```powershell
quarto publish gh-pages
```

Repository:

`https://github.com/How-Tze/psych-ai-start-guide`

Site:

`https://How-Tze.github.io/psych-ai-start-guide/`

Do not commit `_site/` to `main` unless the publication architecture is intentionally changed.

## Git discipline

Use small, descriptive commits. Examples:

```text
Clarify API billing explanation
Update DeepSeek product status
Fix mobile table layout
Add open-science backlog note
```

Before committing:

```powershell
git status
git diff
```

Before pushing staged files, when useful:

```powershell
git diff --cached
```

Do not rewrite public history or force-push unless explicitly requested.

## Style

Use concise Chinese prose for reader-facing pages.

Prefer:

- short paragraphs;
- direct definitions;
- decision tables;
- callouts for risk or common confusion;
- real research examples;
- minimal jargon.

Avoid repetitive rhetorical contrasts, hype language, and excessive English terminology when a stable Chinese term works.

For technical English terms that matter (API, Agent, Harness, BYOK), define once and then use consistently.

## Internal vs public material

Keep internal audit / field-test / maintenance material out of the public navigation unless it is intentionally promoted into reader-facing content.

Public pages should contain conclusions and useful guidance, not the entire internal audit trail.

## When unsure

If a requested change would alter the core architecture, add a new product family, change deployment strategy, or move material between the Start Guide and the main handbook, stop and surface the decision instead of silently implementing it.

