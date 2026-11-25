"""Render the four self-contained profile headers from the committed ASCII grid."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASCII_SOURCE = ROOT / "assets" / "chrome-portrait.txt"
OUTPUTS = {
    (False, False): "profile-header-silver.svg",
    (False, True): "profile-header-silver-light.svg",
    (True, False): "profile-header-silver-mobile.svg",
    (True, True): "profile-header-silver-mobile-light.svg",
}

FONT_STACK = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PALETTES = {
    False: {
        "surface": "#111316",
        "bar": "#181b1f",
        "border": "#3b4047",
        "heading": "#f5f6f7",
        "copy": "#c1c7cf",
        "quiet": "#a9b1bc",
        "dots": ("#e0e3e8", "#a0a8b2", "#686f79"),
    },
    True: {
        "surface": "#f5f6f8",
        "bar": "#e9ecf0",
        "border": "#b7bdc5",
        "heading": "#16191e",
        "copy": "#343b45",
        "quiet": "#4e5662",
        "dots": ("#454d58", "#687380", "#909aa6"),
    },
}


def tag(name: str, *, content: str | None = None, **attributes: str | int | float) -> str:
    attrs = " ".join(f'{key}="{escape(str(value), quote=True)}"' for key, value in attributes.items())
    opening = f"<{name} {attrs}" if attrs else f"<{name}"
    return f"{opening}/>" if content is None else f"{opening}>{content}</{name}>"


def label(x: float, y: float, value: str, *, fill: str, size: int, weight: int = 400) -> str:
    return tag("text", x=x, y=y, fill=fill, content=escape(value),
               **{"font-size": size, "font-weight": weight})


def portrait(center_x: int, top: int, height: int) -> str:
    lines = ASCII_SOURCE.read_text(encoding="ascii").splitlines()
    columns = max(map(len, lines))
    line_height = height / len(lines)
    font_size = line_height * 0.93
    width = columns * font_size * 0.60
    x = round(center_x - width / 2, 2)
    group = ['<g id="portrait" fill="url(#silver)">']
    for index, line in enumerate(lines):
        group.append(tag(
            "text",
            x=x,
            y=round(top + (index + 0.85) * line_height, 2),
            textLength=round(width, 2),
            lengthAdjust="spacingAndGlyphs",
            content=escape(line.ljust(columns)),
            **{"class": "portrait-line", "font-size": round(font_size, 2), "xml:space": "preserve"},
        ))
    return "\n".join([*group, "</g>"])


def build_svg(mobile: bool = False, light: bool = False) -> str:
    """Build one profile header SVG as a deterministic string."""
    palette = PALETTES[light]
    width, height = (480, 466) if mobile else (960, 330)
    bar_height = 48
    plate = (
        dict(x=16, y=59, width=448, height=265, rx=8)
        if mobile else dict(x=567, y=59, width=377, height=255, rx=8)
    )
    surface = tag("rect", x=0.5, y=0.5, width=width - 1, height=height - 1, rx=12,
                  fill=palette["surface"], stroke=palette["border"])
    bar = tag("rect", width=width, height=bar_height, fill=palette["bar"],
              **{"clip-path": "url(#frame)"})
    dots = [
        tag("circle", cx=25 + index * 14, cy=24, r=3.5, fill=fill)
        for index, fill in enumerate(palette["dots"])
    ]
    caption = label(82, 30, "marcus@github", fill=palette["quiet"], size=16)
    field = tag("rect", fill="url(#graphite)", **plate)
    if mobile:
        artwork = portrait(center_x=240, top=67, height=248)
        intro = [
            label(25, 357, "$ whoami", fill=palette["quiet"], size=17, weight=600),
            label(23, 409, "Marcus Boni", fill=palette["heading"], size=54, weight=800),
            label(25, 442, "Software developer", fill=palette["copy"], size=23),
        ]
    else:
        artwork = portrait(center_x=754, top=65, height=240)
        intro = [
            label(46, 127, "$ whoami", fill=palette["quiet"], size=21, weight=600),
            label(43, 201, "Marcus Boni", fill=palette["heading"], size=60, weight=800),
            label(46, 248, "Software developer", fill=palette["copy"], size=26),
        ]

    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Marcus Boni</title>',
        '<desc id="desc">Silver ASCII portrait of Marcus Boni in a terminal.</desc>',
        "<style>",
        f"  text{{font-family:{FONT_STACK}}}",
        "  .portrait-line{white-space:pre}",
        "  @media (prefers-reduced-motion: no-preference){",
        "    #portrait{animation:silver-light 2.4s ease-out both}",
        "    @keyframes silver-light{from{opacity:.83} to{opacity:1}}",
        "  }",
        "</style>",
        "<defs>",
        f'  <clipPath id="frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
        '  <linearGradient id="graphite" x2="1" y2="1">',
        '    <stop stop-color="#08090b"/>',
        '    <stop offset="1" stop-color="#1f2329"/>',
        "  </linearGradient>",
        '  <linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="330">',
        '    <stop stop-color="#8d98a5"/>',
        '    <stop offset=".42" stop-color="#f4f6f8"/>',
        '    <stop offset=".72" stop-color="#cbd2da"/>',
        '    <stop offset="1" stop-color="#8d98a5"/>',
        "  </linearGradient>",
        "</defs>",
        surface, bar, *dots, caption, field, artwork, *intro,
        "</svg>",
        "",
    ])


def main() -> None:
    for (mobile, light), filename in OUTPUTS.items():
        (ROOT / "assets" / filename).write_text(build_svg(mobile, light), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
