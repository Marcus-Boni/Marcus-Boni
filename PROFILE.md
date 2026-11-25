# How this profile is built

The README combines minimalist native GitHub Markdown with two self-contained monochrome animated ASCII SVG figures generated deterministically with Python's standard library:

- **Hero Terminal** (`scripts/render_profile_header.py`) — Monochrome graphite-and-silver terminal pairing a concise stack readout with the 82×39 liquid-chrome ASCII portrait (`assets/chrome-portrait.txt`), white-silver raster assembly, and dual continuous specular sweeps.
- **Systems Architecture** (`scripts/render_systems_blueprint.py`) — Minimalist monochrome four-layer ASCII schematic (`Interfaces` → `Applied AI` → `Systems & Data` → `Cloud & Ship`) with traveling silver signal packets and synchronized layer illumination.

The visual and editorial contract lives in [DESIGN.md](./DESIGN.md).

## Generate and validate

Python 3.11 or newer is enough for all active profile assets. No packages, credentials, external fonts, or network access are needed.

```sh
python scripts/render_profile_header.py
python scripts/render_systems_blueprint.py
python scripts/validate_profile.py
```

The generators produce eight responsive theme-aware SVG assets:

| Figure | Asset | Use |
| :--- | :--- | :--- |
| Hero | `assets/hero-terminal-v3.svg` | Desktop, dark theme & fallback |
| Hero | `assets/hero-terminal-v3-light.svg` | Desktop, light theme |
| Hero | `assets/hero-terminal-v3-mobile.svg` | Mobile, dark theme |
| Hero | `assets/hero-terminal-v3-mobile-light.svg` | Mobile, light theme |
| Architecture | `assets/systems-blueprint-v2.svg` | Desktop, dark theme & fallback |
| Architecture | `assets/systems-blueprint-v2-light.svg` | Desktop, light theme |
| Architecture | `assets/systems-blueprint-v2-mobile.svg` | Mobile, dark theme |
| Architecture | `assets/systems-blueprint-v2-mobile-light.svg` | Mobile, light theme |

Both README languages select the right variant using `<picture>` and `<source>`. Every animation lives inside `@media (prefers-reduced-motion: no-preference)`, so reduced-motion viewers immediately receive the complete static artwork.

A new visual edition gets fresh versioned filenames in both READMEs because GitHub's asset proxy can serve stale SVG bytes if filenames remain unchanged.

## Edit the content

- Update `README.md` and `README.pt-BR.md` together so both languages stay in parity.
- Keep project descriptions grounded in their linked public repositories and pinned commit SHAs.
- Edit hero or architecture copy in `scripts/render_profile_header.py` or `scripts/render_systems_blueprint.py`, then regenerate.
- Never hand-edit generated SVGs: `scripts/validate_profile.py` enforces byte-for-byte reproducibility against both generators.

`Validate profile` runs on pull requests and pushes to `main`. It checks local references, bilingual project parity, SVG safety, monochrome consistency, reduced-motion compliance, and reproducible asset generation.
