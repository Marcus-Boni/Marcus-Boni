# Design

## Source of truth
- Status: Active
- Last refreshed: 2026-11-25
- Primary surfaces: GitHub profile README and its Portuguese translation.
- Evidence: the approved chrome portrait, its extracted glyph grid, and the public project READMEs.
- Direction chosen by Marcus: a graphite and silver terminal drawn from the same chrome portrait as the GitHub avatar. English first, with a Portuguese translation.

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
- Header → introduction and contact → selected work with source links → optional further work → visible engineering approach → contact.
- English: `README.md`; Portuguese: `README.pt-BR.md`; implementation notes: `PROFILE.md`.
- GitHub's native pins and activity remain separate profile surfaces.

## Design principles
- Show work through a problem and a concrete implementation choice.
- Use the terminal as identity, with native Markdown for important content and links.
- Prefer a short curated selection to an exhaustive inventory.
- Keep secondary content expandable using native `details`.

## Visual language
- The terminal frame uses graphite and cool silver in dark mode and pale silver in light mode. Both render the chrome as bright glyphs on a dark plate.
- The name carries the hierarchy. Terminal commands and the portrait use system monospace, and the README body uses native GitHub typography.
- Desktop places the text beside the portrait. Mobile gives the artwork its own full-width plate so the curls, eyes and jaw hold up in a narrow profile column.
- The glyph grid comes from the luminance of the approved avatar. Preserve the image's downward gaze and reflection pattern across themes.
- The glyph rows assemble once. A continuous angled reflection moves across the silver in a 5.4-second cycle while the terminal frame and typography stay fixed. Reduced motion shows the complete still frame.

## Components
- Header: `scripts/render_profile_header.py` owns four versioned SVG variants (desktop/mobile × dark/light).
- Project entry: linked heading, one short problem/implementation paragraph, compact technology line and one descriptive source permalink.
- Contact row: native links which wrap naturally.
- Further work: a native expandable section; the engineering approach remains visible below it.
- Historical art generators remain available for intentional manual use.

## Accessibility
- Essential content and navigation remain selectable native text.
- SVG variants have `title`, `desc`, and meaningful image alternative text.
- Use readable contrast in both themes; verify with browser rendering.
- Native links and details retain GitHub keyboard/focus behavior.
- No required animation, hover interaction, or icon-only link. Reduced-motion viewers receive the complete static composition.

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
- Keep source links pinned to the reviewed revision; their labels must explain what visitors can inspect.
- Keep implementation credits out of the visible README footer, as requested by Marcus.

## Implementation constraints
- GitHub Flavored Markdown and supported HTML only; no custom README CSS or JavaScript.
- Self-contained SVGs generated with Python's standard library; no new dependencies.
- Keep header generation deterministic and validate committed assets against the generator.
- Validate actual GitHub Markdown output and visual layouts before publication.
- Retain historical generators without automatic daily metric commits.

## Open questions
- None blocking. Review project selection when the public work changes.
