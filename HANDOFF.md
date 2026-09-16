# HANDOFF — Psych AI Start Guide

**Project:** 心理学研究者的 AI Start Guide  
**Repository:** `https://github.com/How-Tze/psych-ai-start-guide`  
**Public site:** `https://How-Tze.github.io/psych-ai-start-guide/`  
**Current stage:** First public HTML deployment completed  
**Last handoff:** 2026-09-16

## 1. Project purpose

This is a dynamic companion guide to the frozen v1.1 handbook 《心理学研究的 AI 进阶手册》.

The main handbook explains relatively stable research-workflow principles. This Start Guide explains the current product layer: what a psychology researcher should open, when to use it, what an API is, how product/API/Harness/workflow relate, and how to begin with real tools without turning the site into a product manual.

Primary audience:

- psychology / social-science students and researchers;
- many readers are in mainland China;
- readers may know ChatGPT-style chat but have little understanding of Projects, Deep Research, APIs, Code Agents, Harnesses, BYOK tools, or deployment workflows.

## 2. Frozen editorial logic

Do **not** reorganize the site around vendors.

The primary navigation is task-oriented:

1. ordinary chat;
2. Project / Workspace;
3. source-grounded paper reading;
4. Deep Research;
5. API basics and first configuration;
6. API for reproducible / batch research work;
7. Code Agent / Harness;
8. Work Agent / local multi-file workflows;
9. privacy and sensitive materials;
10. a short start checklist.

Product pages are the secondary navigation.

Core conceptual chain:

> Product UI → API → Harness → Workflow

Important distinctions to preserve:

- product subscription ≠ API billing;
- model ≠ product;
- model ≠ Harness;
- Code Agent capability is partly created by the environment, tools, permissions and execution loop, not only by the underlying model;
- “later in the stack” does not mean “better” or “more advanced for everyone”. Upgrade only when the current layer creates friction.

## 3. Core product ecosystems currently in scope

International:

- ChatGPT / OpenAI;
- Claude / Anthropic;
- Gemini / Gemini Notebook;

China / mainland-accessible ecosystems:

- DeepSeek;
- Kimi;
- Qwen;
- GLM;
- Tencent WorkBuddy.

Do not expand the core list merely to be comprehensive. Add a product only when it has clear teaching value for at least one of these:

- research discovery;
- persistent file/project work;
- API / extensibility;
- code or agent workflows;
- local or multi-file work.

## 4. API teaching logic

API is a mainline topic, not an appendix-only topic.

Explain API at three practical levels:

1. no-code BYOK use — e.g. DeepSeek API in Immersive Translate;
2. BYOK clients — e.g. Chatbox-like clients, only as a concept, not detailed click-by-click tutorials;
3. research scripting — batch/reproducible calls via Python/R/JS.

Editorial principle:

> Explain usage decisions; do not reproduce vendor documentation.

Avoid over-testing trivial product flows. Real-user friction, billing separation, model/provider/Harness relationships, security, and reproducibility matter more than exact button labels.

The minimal research API example currently demonstrates:

> synthetic CSV → Python script → API → model response → append-only JSONL + run metadata + error logging + resumable rerun

The example is pedagogical. It must not imply that LLM thematic coding is validated merely because an API call is reproducible.

## 5. Open-science backlog for the main handbook

A future handbook revision should add a section on AI and open science.

Key idea:

> AI can reduce the maintenance cost of turning a well-managed local research project into a public, non-sensitive, reusable research release.

Potential AI-assisted tasks:

- prepare data dictionaries;
- organize analysis code;
- generate README / environment notes;
- maintain version and decision records;
- identify local absolute paths, temporary files, API keys, or other obvious release hazards;
- identify downstream public artifacts that may need updating after analysis changes.

Human-only / high-accountability decisions remain:

- whether participant data are sufficiently de-identified;
- whether consent permits sharing;
- whether third-party data can be redistributed;
- whether a public release is scientifically and ethically appropriate.

Do not edit the frozen v1.1 handbook merely because this backlog exists.

## 6. Current deployment state

Local Quarto preview and render were manually checked successfully on Windows.

First GitHub Pages deployment succeeded using:

```powershell
quarto publish gh-pages
```

Public site:

`https://How-Tze.github.io/psych-ai-start-guide/`

Current deployment model:

- `main` = Quarto source;
- `gh-pages` = rendered publication branch;
- `_site/` should not be committed to `main`;
- GitHub Actions automation has **not** yet been intentionally introduced.

Keep this simple until there is a clear maintenance benefit from CI deployment.

## 7. Dynamic-information policy

Product capabilities, availability, pricing, plan limits, product names, account requirements and regional access can change quickly.

For any substantive update to dynamic product information:

- verify against current official sources first;
- record / preserve a `last_checked` date;
- prefer capability descriptions over exact button coordinates;
- avoid hard-coding prices into evergreen prose when a structured data field or dynamic table is more appropriate;
- when official sources conflict, do not guess. State the uncertainty or choose the currently stable documented route.

Community reports may be used for real-world friction / experience, but must not override official documentation for product facts.

## 8. Security rules

Never commit or expose:

- API keys;
- `.env` files;
- credential exports;
- payment details;
- private account screenshots;
- participant-identifiable or sensitive research data;
- unpublished manuscripts or collaborator materials unless explicitly authorized.

Before any push, inspect:

```powershell
git status
```

and, when appropriate:

```powershell
git diff --cached
```

If a secret is accidentally committed, removing it from the latest file is not enough; treat it as exposed and rotate/revoke it.

## 9. Content/style rules

The desired voice is concise, practical, and research-oriented.

Prefer:

- concrete examples;
- decision rules;
- small diagrams;
- short product cards;
- “when to stay here / when to upgrade” guidance.

Avoid:

- AI-product hype;
- vendor rankings;
- long feature catalogs;
- step-by-step instructions that merely duplicate current vendor help pages;
- unnecessary engineering jargon;
- implying that more automation is inherently better;
- presenting one platform as the default for all readers.

China and international ecosystems should be presented in parallel where useful.

## 10. Engineering / Quarto rules

Before publishing changes:

```powershell
quarto preview
```

Check at least:

- homepage;
- task-selection page;
- first API setup page;
- API research script page;
- one product page;
- API tools appendix;
- narrow/mobile-width layout if practical.

Then:

```powershell
quarto render
```

For manual publication:

```powershell
quarto publish gh-pages
```

Do not change deployment architecture without a concrete maintenance reason.

## 11. Recommended next tasks

Priority order:

1. Perform an online QA pass of the live GitHub Pages site.
2. Improve public-facing repository metadata and README only where needed.
3. Continue editorial integration of the Start Guide rather than adding more tools.
4. Consider structured product/API data rendering if manual duplication becomes costly.
5. Introduce CI/GitHub Actions only after the manual workflow becomes annoying.
6. Later, prepare a release / citation strategy and coordinate it with the main handbook publication.

## 12. Relationship to the main handbook

The main handbook v1.1 is currently frozen as the stable conceptual document.

The Start Guide is intentionally more dynamic.

Do not silently move volatile product details back into the main handbook. Instead:

- stable principle → main handbook;
- current product choice / configuration / availability → Start Guide;
- experimental field notes → internal project material, not necessarily public navigation.

