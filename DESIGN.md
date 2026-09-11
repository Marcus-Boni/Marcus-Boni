# Design

## Source of truth
- Status: Active
- Last refreshed: 2026-09-10
- Primary surfaces: GitHub profile README and its Portuguese translation.
- Evidence: original README, `assets/ascii-portrait.svg`, `scripts/make_info_card.py`, public project READMEs, and the existing portfolio's charcoal / warm accent palette.
- Direction chosen by Marcus: a more refined, readable authorial terminal; English first, Portuguese available.

## Brand
- Personality: technical, deliberate, approachable.
- Trust signals: inspectable projects, specific engineering choices, honest project context.
- Avoid: invented seniority or impact, generic slogans, badge walls, repeated contribution calendars, tiny text.

## Product goals
- Make the developer's focus and strongest work clear within a short scan.
- Make project source code and contact links easy to find.
- Keep the existing ASCII identity and remove competing visual panels.
- Success: legible at 320px, useful with images unavailable, four focused project summaries before optional details.
- Non-goals: a JavaScript website inside a README, gamified statistics, or changing project implementation.

## Personas and jobs
- Engineering peers and hiring teams: understand scope, inspect technical decisions, open repositories.
- Potential collaborators: find relevant interests and a direct contact route.
- Context: GitHub desktop or mobile, light or dark appearance, sometimes without images.

## Information architecture
- Header → introduction and contact → selected work → engineering interests → optional further work.
- English: `README.md`; Portuguese: `README.pt-BR.md`; implementation notes: `PROFILE.md`.
- GitHub's native pins and activity remain separate profile surfaces.

## Design principles
- Show work through a problem and a concrete implementation choice.
- Use the terminal as identity, with native Markdown for important content and links.
- Prefer a short curated selection to an exhaustive inventory.
- Keep secondary content expandable using native `details`.

## Visual language
- Color: charcoal, warm white, restrained copper accent and a terminal green signal; explicit light variants.
- Typography: system monospace inside SVG, GitHub native typography for prose.
- Layout: one column; generous but restrained spacing; no fixed-width table for core content.
- Shape: one terminal frame, quiet dividers, no stacked dashboard cards.
- Motion: new header is static; no blinking or delayed essential information.
- Imagery: reuse the original ASCII portrait as vector text, no external font/image requests.

## Components
- Header: `scripts/render_profile_header.py` owns four versioned SVG variants (desktop/mobile × dark/light).
- Project entry: linked heading, one short problem/implementation paragraph, compact technology line.
- Contact row: native links which wrap naturally.
- Further work: a native expandable section.
- Historical art generators remain available for intentional manual use.

## Accessibility
- Essential content and navigation remain selectable native text.
- SVG variants have `title`, `desc`, and meaningful image alternative text.
- Use readable contrast in both themes; verify with browser rendering.
- Native links and details retain GitHub keyboard/focus behavior.
- No required animation, hover interaction, or icon-only link.

## Responsive behavior
- Verify at 320px and 390px mobile, a narrow desktop profile column, and a wide repository view.
- Use `picture` sources for mobile and color scheme; fallback is the dark desktop SVG.
- Core content uses no horizontal tables and must not overflow the page.

## Interaction states
- Images loading/unavailable: native introduction and project links still explain the work.
- Offline: versioned sources and assets remain available in a clone.
- Empty/error/disabled: no live widgets or asynchronous data states in the README.
- Success: image render and native text agree.

## Content voice
- Plain English with equivalent Portuguese content, first person, specific and concise.
- Describe projects as projects, prototypes or demonstrations according to their sources.
- Never infer expertise from commit counts, repository counts, or language percentages.
- Never add customers, adoption, commercial results, or private project details without a public source.

## Implementation constraints
- GitHub Flavored Markdown and supported HTML only; no custom README CSS or JavaScript.
- Self-contained SVGs generated with Python's standard library; no new dependencies.
- Keep header generation deterministic and validate committed assets against the generator.
- Validate actual GitHub Markdown output and visual layouts before publication.
- Retain historical generators without automatic daily metric commits.

## Open questions
- None blocking. Review project selection when the public work changes.
