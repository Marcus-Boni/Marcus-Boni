# Design

## Source of truth
- Status: Active
- Last refreshed: 2026-11-25
- Primary surfaces: GitHub profile README and its Portuguese translation.
- Evidence: the approved chrome portrait, its extracted glyph grid, and the public project repositories (`ISPer`, `OptTime`, `chatbot-template`, `Marcus-Boni-Portfolio`).
- Direction: graphite and liquid-silver terminal typography paired with a surgical signal-ember accent (echoing `marcusboni.com.br`) and two original animated ASCII engineering figures (`FIG.01` hero terminal + `FIG.02` systems topology). English first, with a Portuguese translation.

## Brand
- Personality: systems-minded, precise, modern, verifiable.
- Trust signals: inspectable source permalinks, release history, modular architecture details, automated evaluation and contract-testing discipline.
- Avoid: invented metrics or seniority claims, generic third-party stat cards, shields.io badge walls, repeated contribution calendars, tiny illegible diagrams.

## Product goals
- Communicate Marcus's engineering range and technical depth within seconds of landing on the profile.
- Showcase original self-hosted ASCII animation craft (`FIG.01` and `FIG.02`) without breaking responsiveness, theme support, or reduced-motion accessibility.
- Make flagship source code, live sites, and direct contact routes effortless to inspect.
- Success: legible at 320px and 390px mobile as well as desktop in dark and light themes; useful even with images disabled; every capability backed by concrete repository proof.

## Information architecture
- `FIG.01` Animated Chrome Terminal Hero → positioning & direct links → `Selected systems` (`01`–`04` with pinned deep links) → `Systems topology` (`FIG.02` animated ASCII schematic + native text index) → expandable `More shipped tools & experiments` → visible `How I engineer` → closing contact line.
- English: `README.md`; Portuguese: `README.pt-BR.md`; maintenance notes: `PROFILE.md`.

## Visual language
- Obsidian graphite (`#0e1014`) and liquid silver in dark mode; crisp paper silver (`#f6f7f9`) and deep ink in light mode.
- One surgical ember accent (`#ff5a26` dark, `#c8370b` light for AA contrast) marks active signal points: terminal prompts, blinking cursor, raster scanline, and live data packets in the systems bus.
- `FIG.01` pairs an animated CLI boot & capability readout beside the 82×39 liquid-chrome ASCII bust portrait with a top-to-bottom raster scanline assembly and dual specular reflections.
- `FIG.02` visualizes four interconnected engineering layers (`INTERFACES` → `APPLIED AI` → `SYSTEMS & DATA` → `CLOUD & SHIP`) with traveling ASCII signal packets and sequential layer illumination.
- Reduced motion renders both figures immediately at 100% static clarity.

## Components
- Hero terminal (`FIG.01`): `scripts/render_profile_header.py` owns four versioned SVG variants (`assets/hero-terminal-v2*.svg`).
- Systems blueprint (`FIG.02`): `scripts/render_systems_blueprint.py` owns four versioned SVG variants (`assets/systems-blueprint-v1*.svg`).
- Project entry: numbered linked heading, concrete architecture summary grounded in public source files, compact monospace stack, and descriptive pinned permalinks.
- Native text stack index directly below `FIG.02` guarantees Ctrl+F searchability, screen-reader parity, and zero-image resilience.
- Further work uses native `<details>`; engineering principles stay visible below it.

## Accessibility & constraints
- GitHub Flavored Markdown and supported HTML only; zero external dependencies, zero JavaScript, zero third-party widgets.
- All SVGs include `role="img"`, `<title>`, `<desc>`, meaningful image `alt` text, and wrap every CSS animation inside `@media (prefers-reduced-motion: no-preference)`.
- Every new visual edition uses fresh versioned filenames so GitHub's asset proxy never serves stale cached bytes.
- Keep implementation credits out of the visible README footer, as requested by Marcus.
