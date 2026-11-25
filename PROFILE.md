# How this profile is built

The README combines native GitHub Markdown with two self-contained animated ASCII SVG figures generated deterministically from Python's standard library:

- **`FIG.01` Hero Terminal** (`scripts/render_profile_header.py`) — Dual-pane graphite-and-silver terminal pairing an animated CLI capability readout with the 82×39 liquid-chrome ASCII portrait (`assets/chrome-portrait.txt`), laser raster assembly, and dual continuous specular sweeps.
- **`FIG.02` Systems Topology** (`scripts/render_systems_blueprint.py`) — Animated four-layer ASCII hardware/software schematic (`Interfaces` → `Applied AI` → `Systems & Data` → `Cloud & Ship`) with traveling signal packets and synchronized layer illumination.

The visual and editorial contract lives in [DESIGN.md](./DESIGN.md).

## Generate and validate

Python 3.11 or newer is enough for all active profile assets. No third-party packages, credentials, external fonts, or network access are required.

```sh
python scripts/render_profile_header.py
python scripts/render_systems_blueprint.py
python scripts/validate_profile.py
```

The generators produce eight responsive theme-aware SVG assets:

| Figure | Asset | Use |
| :--- | :--- | :--- |
| `FIG.01` | `assets/hero-terminal-v2.svg` | Desktop, dark theme & fallback |
| `FIG.01` | `assets/hero-terminal-v2-light.svg` | Desktop, light theme |
| `FIG.01` | `assets/hero-terminal-v2-mobile.svg` | Mobile, dark theme |
| `FIG.01` | `assets/hero-terminal-v2-mobile-light.svg` | Mobile, light theme |
| `FIG.02` | `assets/systems-blueprint-v1.svg` | Desktop, dark theme & fallback |
| `FIG.02` | `assets/systems-blueprint-v1-light.svg` | Desktop, light theme |
| `FIG.02` | `assets/systems-blueprint-v1-mobile.svg` | Mobile, dark theme |
| `FIG.02` | `assets/systems-blueprint-v1-mobile-light.svg` | Mobile, light theme |

Both README languages select the right variant using `<picture>` and `<source>` media queries. Every animation lives inside `@media (prefers-reduced-motion: no-preference)`, so reduced-motion viewers immediately receive the complete static artwork.

A new visual edition gets fresh versioned filenames in both READMEs because GitHub's asset proxy can cache old SVG bytes when filenames stay unchanged.

## Edit the content

- Update `README.md` and `README.pt-BR.md` together so both languages stay in parity.
- Keep project descriptions grounded in their linked public repositories and pinned commit SHAs.
- Edit hero or blueprint copy in `scripts/render_profile_header.py` or `scripts/render_systems_blueprint.py`, then regenerate.
- Never hand-edit generated SVGs: `scripts/validate_profile.py` checks byte-for-byte reproducibility against both generators.

`Validate profile` runs on pull requests and pushes to `main`. It verifies local references, bilingual project parity, SVG safety, reduced-motion compliance, and reproducible asset generation.

## Replace the chrome portrait

`assets/chrome-portrait.png` is the 500 × 500 upload for the GitHub avatar and the source for `assets/chrome-portrait.txt`:

```sh
python -m pip install -r scripts/requirements-local.txt
python scripts/make_ascii_svg.py --chrome assets/chrome-portrait.png assets/chrome-portrait.txt
python scripts/render_profile_header.py
python scripts/validate_profile.py
```

The legacy portrait, neofetch card, calendar, and language bar remain archived in the repository.
