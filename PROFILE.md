# How this profile is built

The README uses native GitHub Markdown and a self-contained SVG terminal. The
terminal renders the chrome portrait as a grid of ASCII characters. Project
descriptions, technology choices and contact links remain native text.

The visual and editorial contract lives in [DESIGN.md](./DESIGN.md).

## Generate and validate

Python 3.11 or newer is enough for the current header. No packages, credentials,
external fonts, image services or network access are needed.

```sh
python scripts/render_profile_header.py
python scripts/validate_profile.py
```

The generator creates four assets from the versioned `assets/chrome-portrait.txt` grid:

| Asset | Use |
| :--- | :--- |
| `assets/profile-header-silver-loop.svg` | Desktop, dark theme and fallback |
| `assets/profile-header-silver-loop-light.svg` | Desktop, light theme |
| `assets/profile-header-silver-loop-mobile.svg` | Mobile, dark theme |
| `assets/profile-header-silver-loop-mobile-light.svg` | Mobile, light theme |

Both README languages select the appropriate asset with `picture` and `source`.
Mobile stacks the portrait and name for a wider portrait at narrow viewports.
When motion is enabled, the glyph rows assemble from the crown to the shoulders.
An angled reflection then makes a continuous 5.4-second pass across the assembled
portrait. Both READMEs embed the responsive image directly in the header. Viewers
who prefer reduced motion get the complete still frame.

A new visual edition gets new filenames in both READMEs. The GitHub profile
can serve stale SVG bytes when only a query parameter changes.

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

## Replace the chrome portrait

`assets/chrome-portrait.png` is the 500 × 500 upload for the GitHub avatar and the
input to the ASCII conversion. The glyphs follow the highlights of the image,
while the black background maps to spaces. The PNG is not loaded by the README.

After updating that image, use the existing local art dependencies to regenerate
the grid and all four headers:

```sh
python -m pip install -r scripts/requirements-local.txt
python scripts/make_ascii_svg.py --chrome assets/chrome-portrait.png assets/chrome-portrait.txt
python scripts/render_profile_header.py
python scripts/validate_profile.py
```

The legacy portrait, neofetch card, calendar and language bar remain archived in
the repository. The manual legacy workflow refreshes only the metrics.

## References

- [GitHub profile README documentation](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [Theme-aware images on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- [Native expandable sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- Original terminal-art inspiration: [Avi Vashishta](https://www.avivashishta.com/blog/build-animated-github-profile-readme.html).
