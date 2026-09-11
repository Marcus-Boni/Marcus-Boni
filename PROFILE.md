# How this profile is built

The README uses native GitHub Markdown and a self-contained SVG terminal. The
portrait comes from the original ASCII artwork in this repository. Project
descriptions, technology choices and contact links remain native text.

The visual and editorial contract lives in [DESIGN.md](./DESIGN.md).

## Generate and validate

Python 3.11 or newer is enough for the current header. No packages, credentials,
external fonts, image services or network access are needed.

```sh
python scripts/render_profile_header.py
python scripts/validate_profile.py
```

The generator creates four assets from the existing portrait:

| Asset | Use |
| :--- | :--- |
| `assets/profile-header.svg` | Desktop, dark theme and fallback |
| `assets/profile-header-light.svg` | Desktop, light theme |
| `assets/profile-header-mobile.svg` | Mobile, dark theme |
| `assets/profile-header-mobile-light.svg` | Mobile, light theme |

Both README languages select the appropriate asset with `picture` and `source`.
The mobile composition is separate so the name and role remain readable. The
header is static: it is complete immediately and requires no animation support.

## Edit the content

- Update `README.md` and `README.pt-BR.md` together.
- Keep project descriptions grounded in their linked public repositories.
- Update the header copy in `scripts/render_profile_header.py`, then regenerate.
- Do not hand-edit generated SVGs: validation compares them with the generator.
- Preview at 320px and 390px, in both themes and in a desktop profile column.
- Check the GitHub-rendered README, including language links and expanded details.

`Validate profile` runs on pull requests and pushes to `main`. It checks local
references, image alternatives, self-contained SVGs and reproducible generation.
The workflow has read-only repository permissions and creates no commits.
It does not replace visual review or check the availability of external sites.

## Original artwork

The earlier portrait, neofetch card, contribution calendar, language bar and
their generators remain versioned. They are historical assets, not required by
the current README. The native GitHub contribution calendar already provides
activity context; language percentages and streaks are not measures of expertise.

The legacy workflow is now manual only. `Generate legacy profile art (manual)`
can still refresh the historical metrics using GitHub data, but the profile no
longer produces daily metric commits.

To regenerate the original portrait from a new photo, use a separate local
environment and the existing optional dependencies:

```sh
python -m venv .venv
# Activate the environment for your shell, then:
pip install -r scripts/requirements-local.txt
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/render_profile_header.py
python scripts/validate_profile.py
```

The original animation generators retain a visible static base state if an SVG
client ignores animation. They are not used for the new header.

## References

- [GitHub profile README documentation](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Theme-aware images on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- [Native expandable sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- Original terminal-art inspiration: [Avi Vashishta](https://www.avivashishta.com/blog/build-animated-github-profile-readme.html).
