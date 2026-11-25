"""Render the four self-contained monochrome chrome ASCII hero terminal SVGs.

Generates desktop/mobile x dark/light variants from assets/chrome-portrait.txt
using Python's standard library only. Strictly follows a silver, white, gray,
and black palette aligned with the GitHub chrome bust avatar.
"""

from __future__ import annotations

from html import escape
from math import ceil, radians, tan
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASCII_SOURCE = ROOT / "assets" / "chrome-portrait.txt"
OUTPUTS = {
    (False, False): "hero-terminal-v4.svg",
    (False, True): "hero-terminal-v4-light.svg",
    (True, False): "hero-terminal-v4-mobile.svg",
    (True, True): "hero-terminal-v4-mobile-light.svg",
}

FONT_STACK = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PALETTES = {
    False: {
        "surface": "#0e1014",
        "bar": "#14171d",
        "border": "#2d333d",
        "divider": "#232832",
        "heading_top": "#ffffff",
        "heading_bottom": "#cbd3de",
        "subheading": "#cfd6e0",
        "quiet": "#929ca9",
        "accent": "#f2f5f9",
        "dots": ("#d2d8e1", "#8b94a2", "#515966"),
        "plate_border": "#282e38",
        "plate_tick": "#47505e",
    },
    True: {
        "surface": "#f6f7f9",
        "bar": "#ebedf1",
        "border": "#c3cad4",
        "divider": "#d8dde6",
        "heading_top": "#12161c",
        "heading_bottom": "#2e3541",
        "subheading": "#2d3542",
        "quiet": "#4d5664",
        "accent": "#151921",
        "dots": ("#3f4754", "#707987", "#a1aab7"),
        "plate_border": "#2b323d",
        "plate_tick": "#4d5766",
    },
}


def tag(name: str, *, content: str | None = None, **attributes: str | int | float) -> str:
    attrs = " ".join(
        f'{key}="{escape(str(value), quote=True)}"' for key, value in attributes.items()
    )
    opening = f"<{name} {attrs}" if attrs else f"<{name}"
    return f"{opening}/>" if content is None else f"{opening}>{content}</{name}>"


def text_el(
    x: float,
    y: float,
    value: str,
    *,
    fill: str,
    size: float,
    weight: int = 400,
    **extra: str | int | float,
) -> str:
    return tag(
        "text",
        x=x,
        y=y,
        fill=fill,
        content=escape(value),
        **{"font-size": size, "font-weight": weight, **extra},
    )


def corner_ticks(x: int, y: int, width: int, height: int, stroke: str) -> str:
    """Minimal crosshair corner marks inside the ASCII sculpture plate."""
    inset = 9
    arm = 7
    x0, y0 = x + inset, y + inset
    x1, y1 = x + width - inset, y + height - inset
    d = (
        f"M{x0} {y0 + arm}V{y0}H{x0 + arm}"
        f"M{x1 - arm} {y0}H{x1}V{y0 + arm}"
        f"M{x0} {y1 - arm}V{y1}H{x0 + arm}"
        f"M{x1 - arm} {y1}H{x1}V{y1 - arm}"
    )
    return tag(
        "path",
        d=d,
        fill="none",
        stroke=stroke,
        **{"stroke-width": 1.0, "stroke-linecap": "square", "aria-hidden": "true"},
    )


def portrait(center_x: int, top: int, height: int) -> str:
    lines = ASCII_SOURCE.read_text(encoding="ascii").splitlines()
    columns = max(map(len, lines))
    line_height = height / len(lines)
    font_size = line_height * 0.94
    width = columns * font_size * 0.60
    x = round(center_x - width / 2, 2)
    group = ['<g id="portrait" fill="url(#silver)"><g id="portrait-glyphs">']
    for index, line in enumerate(lines):
        group.append(
            tag(
                "text",
                x=x,
                y=round(top + (index + 0.85) * line_height, 2),
                textLength=round(width, 2),
                lengthAdjust="spacingAndGlyphs",
                content=escape(line.ljust(columns)),
                style=f"--row-delay:{0.08 + index * 0.036:.3f}s",
                **{
                    "class": "portrait-line",
                    "font-size": round(font_size, 2),
                    "xml:space": "preserve",
                },
            )
        )
    return "\n".join([*group, "</g></g>"])


def build_svg(mobile: bool = False, light: bool = False) -> str:
    """Build one minimalist monochrome chrome profile hero SVG."""
    p = PALETTES[light]
    width, height = (480, 466) if mobile else (960, 326)
    bar_h = 38 if mobile else 40

    plate = (
        dict(x=16, y=50, width=448, height=256, rx=8)
        if mobile
        else dict(x=570, y=54, width=374, height=256, rx=8)
    )
    px, py, pw, ph = plate["x"], plate["y"], plate["width"], plate["height"]

    # Primary diagonal chrome reflection sweep
    band_h = 114
    band_angle = 8
    skew = tan(radians(band_angle))
    band_y = py - band_h - 10
    travel = ph + band_h + ceil(pw * skew) + 20

    # Secondary gentle counter-angle specular glint (cool silver-white)
    glint_h = 62
    glint_angle = -6
    glint_skew = tan(radians(abs(glint_angle)))
    glint_y = py - glint_h - 10
    glint_travel = ph + glint_h + ceil(pw * glint_skew) + 20

    # Initial horizontal silver scanline across the portrait height
    scan_top = 59 if mobile else 63
    scan_span = 236 if mobile else 236

    # Frame & title bar
    surface = tag(
        "rect",
        x=0.5,
        y=0.5,
        width=width - 1,
        height=height - 1,
        rx=12,
        fill=p["surface"],
        stroke=p["border"],
    )
    bar = tag("rect", width=width, height=bar_h, fill=p["bar"], **{"clip-path": "url(#frame)"})
    bar_rule = tag("line", x1=1, y1=bar_h, x2=width - 1, y2=bar_h, stroke=p["divider"])

    dot_x0 = 20 if mobile else 22
    dot_gap = 13 if mobile else 14
    dots = [
        tag("circle", cx=dot_x0 + i * dot_gap, cy=bar_h / 2, r=3.3, fill=fill)
        for i, fill in enumerate(p["dots"])
    ]

    if mobile:
        bar_left = text_el(64, 23.5, "marcus@github", fill=p["quiet"], size=12.5)
        bar_right_x = 460
        bar_right_text = "ES-BR · UTC-3"
        bar_dot_x = 362
    else:
        bar_left = text_el(72, 24.5, "marcus@github", fill=p["quiet"], size=13)
        bar_right_x = 938
        bar_right_text = "ES-BR · UTC-3"
        bar_dot_x = 834

    status_dot_halo = tag(
        "circle",
        cx=bar_dot_x,
        cy=bar_h / 2,
        r=5.2,
        fill=p["accent"],
        **{"class": "status-halo", "opacity": 0.2, "aria-hidden": "true"},
    )
    status_dot = tag(
        "circle",
        cx=bar_dot_x,
        cy=bar_h / 2,
        r=2.8,
        fill=p["accent"],
        **{"aria-hidden": "true"},
    )
    bar_right = text_el(
        bar_right_x,
        23.5 if mobile else 24.5,
        bar_right_text,
        fill=p["quiet"],
        size=11.5,
        **{"text-anchor": "end"},
    )

    # Obsidian sculpture plate
    plate_rect = tag("rect", fill="url(#obsidian)", stroke=p["plate_border"], **plate)
    plate_grid = tag(
        "rect",
        x=px + 1,
        y=py + 1,
        width=pw - 2,
        height=ph - 2,
        rx=7,
        fill="url(#scan-grid)",
        **{"aria-hidden": "true"},
    )
    plate_corners = corner_ticks(px, py, pw, ph, p["plate_tick"])

    if mobile:
        artwork = portrait(center_x=240, top=59, height=238)
    else:
        artwork = portrait(center_x=757, top=63, height=238)

    # Crisp monochrome silver raster scan beam
    scan_beam = "\n".join(
        [
            '<g class="scan-beam" clip-path="url(#plate-clip)" aria-hidden="true">',
            f'  <rect x="{px}" y="{scan_top - 16}" width="{pw}" height="18" fill="url(#beam-glow)"/>',
            f'  <rect x="{px}" y="{scan_top}" width="{pw}" height="1.5" fill="#ffffff" opacity="0.88"/>',
            "</g>",
        ]
    )

    # Pure minimalist identity block (no stack clutter)
    terminal_nodes: list[str] = []
    if mobile:
        tx = 26
        terminal_nodes.append(
            '<g class="cli-line" style="--cli-delay:0.04s">'
            + text_el(tx, 344, "$", fill=p["accent"], size=15.5, weight=700)
            + text_el(tx + 15, 344, "whoami", fill=p["quiet"], size=15.5, weight=600)
            + "</g>"
        )
        terminal_nodes.append(
            '<g class="cli-hero" style="--cli-delay:0.14s">'
            + text_el(tx - 2, 398, "Marcus Boni", fill="url(#heading-fill)", size=48, weight=800)
            + text_el(tx, 429, "Forward Deployed Engineer", fill=p["subheading"], size=20, weight=500)
            + "</g>"
        )
        status_str = "marcusboni.com.br/blog"
        status_w = 166
        terminal_nodes.append(
            '<g class="cli-line" style="--cli-delay:0.32s">'
            + text_el(tx, 454, "$", fill=p["accent"], size=12.5, weight=700)
            + text_el(
                tx + 14,
                454,
                status_str,
                fill=p["quiet"],
                size=12,
                textLength=status_w,
                lengthAdjust="spacingAndGlyphs",
            )
            + tag(
                "rect",
                x=tx + 14 + status_w + 5,
                y=443.5,
                width=7.5,
                height=13,
                rx=1.5,
                fill=p["accent"],
                **{"class": "cursor-block", "aria-hidden": "true"},
            )
            + "</g>"
        )
    else:
        tx = 44
        terminal_nodes.append(
            '<g class="cli-line" style="--cli-delay:0.04s">'
            + text_el(tx, 118, "$", fill=p["accent"], size=19, weight=700)
            + text_el(tx + 18, 118, "whoami", fill=p["quiet"], size=19, weight=600)
            + "</g>"
        )
        terminal_nodes.append(
            '<g class="cli-hero" style="--cli-delay:0.14s">'
            + text_el(tx - 3, 188, "Marcus Boni", fill="url(#heading-fill)", size=58, weight=800)
            + text_el(tx, 229, "Forward Deployed Engineer", fill=p["subheading"], size=22.5, weight=500)
            + "</g>"
        )
        status_str = "marcusboni.com.br/blog"
        status_w = 186
        terminal_nodes.append(
            '<g class="cli-line" style="--cli-delay:0.34s">'
            + text_el(tx, 282, "$", fill=p["accent"], size=14, weight=700)
            + text_el(
                tx + 16,
                282,
                status_str,
                fill=p["quiet"],
                size=13.5,
                textLength=status_w,
                lengthAdjust="spacingAndGlyphs",
            )
            + tag(
                "rect",
                x=tx + 16 + status_w + 6,
                y=270,
                width=8.5,
                height=14.5,
                rx=1.5,
                fill=p["accent"],
                **{"class": "cursor-block", "aria-hidden": "true"},
            )
            + "</g>"
        )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">Marcus Boni — Forward Deployed Engineer</title>',
            '<desc id="desc">Minimalist monochrome silver-and-graphite developer terminal with an animated ASCII bust portrait of Marcus Boni, Forward Deployed Engineer.</desc>',
            "<style>",
            f"  text{{font-family:{FONT_STACK}}}",
            "  .portrait-line{white-space:pre}",
            "  .portrait-reflection,.portrait-glint,.scan-beam{display:none}",
            "  @media (prefers-reduced-motion: no-preference){",
            "    .cli-line{animation:cli-in .38s cubic-bezier(.16,1,.3,1) var(--cli-delay) backwards}",
            "    .cli-hero{animation:hero-in .45s cubic-bezier(.16,1,.3,1) var(--cli-delay) backwards}",
            "    #portrait .portrait-line{animation:assemble .42s cubic-bezier(.2,.75,.25,1) var(--row-delay) backwards}",
            "    .scan-beam{display:inline;animation:raster-scan 1.55s linear .08s both}",
            "    .portrait-reflection{display:inline}",
            "    .portrait-glint{display:inline}",
            "    #reflection-band{animation:sweep 4.8s linear 1.7s infinite backwards}",
            "    #glint-band{animation:glint 7.6s linear 3.6s infinite backwards}",
            "    .cursor-block{animation:cursor-blink 1.05s steps(2,end) .8s infinite}",
            "    .status-halo{animation:led-pulse 2.8s ease-in-out infinite}",
            "    @keyframes cli-in{from{opacity:.26;transform:translateX(-5px)} to{opacity:1;transform:translateX(0)}}",
            "    @keyframes hero-in{from{opacity:.40;transform:translateY(4px)} to{opacity:1;transform:translateY(0)}}",
            "    @keyframes assemble{from{opacity:.34} to{opacity:1}}",
            f"    @keyframes raster-scan{{0%{{opacity:0;transform:translateY(0)}} 6%{{opacity:1}} 92%{{opacity:1;transform:translateY({scan_span}px)}} 100%{{opacity:0;transform:translateY({scan_span + 10}px)}}}}",
            f"    @keyframes sweep{{from{{transform:translateY(0)}} to{{transform:translateY({travel}px)}}}}",
            f"    @keyframes glint{{from{{transform:translateY(0)}} to{{transform:translateY({glint_travel}px)}}}}",
            "    @keyframes cursor-blink{0%,49%{opacity:1} 50%,100%{opacity:0}}",
            "    @keyframes led-pulse{0%,100%{opacity:.12} 50%{opacity:.42}}",
            "  }",
            "</style>",
            "<defs>",
            f'  <clipPath id="frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
            f'  <clipPath id="plate-clip"><rect x="{px + 1}" y="{py + 1}" width="{pw - 2}" height="{ph - 2}" rx="7"/></clipPath>',
            '  <linearGradient id="heading-fill" x1="0" y1="0" x2="0" y2="1">',
            f'    <stop stop-color="{p["heading_top"]}"/>',
            f'    <stop offset="1" stop-color="{p["heading_bottom"]}"/>',
            "  </linearGradient>",
            '  <linearGradient id="obsidian" x1="0" y1="0" x2="1" y2="1">',
            '    <stop stop-color="#060709"/>',
            '    <stop offset=".55" stop-color="#0f1218"/>',
            '    <stop offset="1" stop-color="#191e27"/>',
            "  </linearGradient>",
            '  <pattern id="scan-grid" width="4" height="4" patternUnits="userSpaceOnUse">',
            '    <line x1="0" y1="0" x2="4" y2="0" stroke="#ffffff" stroke-opacity="0.025" stroke-width="1"/>',
            "  </pattern>",
            '  <linearGradient id="silver" gradientUnits="userSpaceOnUse" x1="0" y1="50" x2="0" y2="310">',
            '    <stop stop-color="#b4bfd0"/>',
            '    <stop offset=".35" stop-color="#ffffff"/>',
            '    <stop offset=".68" stop-color="#dfe5ee"/>',
            '    <stop offset="1" stop-color="#aeb9c9"/>',
            "  </linearGradient>",
            '  <linearGradient id="beam-glow" x1="0" y1="0" x2="0" y2="1">',
            '    <stop stop-color="#ffffff" stop-opacity="0"/>',
            '    <stop offset="1" stop-color="#ffffff" stop-opacity=".22"/>',
            "  </linearGradient>",
            '  <linearGradient id="reflection-falloff" x2="0" y2="1">',
            '    <stop stop-color="#fff" stop-opacity="0"/>',
            '    <stop offset=".28" stop-color="#fff" stop-opacity=".38"/>',
            '    <stop offset=".50" stop-color="#fff" stop-opacity=".98"/>',
            '    <stop offset=".72" stop-color="#fff" stop-opacity=".32"/>',
            '    <stop offset="1" stop-color="#fff" stop-opacity="0"/>',
            "  </linearGradient>",
            '  <linearGradient id="glint-falloff" x2="0" y2="1">',
            '    <stop stop-color="#fff" stop-opacity="0"/>',
            '    <stop offset=".50" stop-color="#e4ebf5" stop-opacity=".42"/>',
            '    <stop offset="1" stop-color="#fff" stop-opacity="0"/>',
            "  </linearGradient>",
            f'  <mask id="reflection-mask" maskUnits="userSpaceOnUse" x="{px}" y="{py}" width="{pw}" height="{ph}">',
            f'    <g transform="skewY(-{band_angle}) translate(0 {round(px * skew)})">',
            f'      <rect id="reflection-band" x="{px}" y="{band_y}" width="{pw}" height="{band_h}" fill="url(#reflection-falloff)"/>',
            "    </g>",
            "  </mask>",
            f'  <mask id="glint-mask" maskUnits="userSpaceOnUse" x="{px}" y="{py}" width="{pw}" height="{ph}">',
            f'    <g transform="skewY({abs(glint_angle)}) translate(0 -{round(px * glint_skew)})">',
            f'      <rect id="glint-band" x="{px}" y="{glint_y}" width="{pw}" height="{glint_h}" fill="url(#glint-falloff)"/>',
            "    </g>",
            "  </mask>",
            "</defs>",
            surface,
            bar,
            bar_rule,
            *dots,
            bar_left,
            status_dot_halo,
            status_dot,
            bar_right,
            plate_rect,
            plate_grid,
            plate_corners,
            artwork,
            '<use class="portrait-reflection" href="#portrait-glyphs" fill="#ffffff" mask="url(#reflection-mask)" aria-hidden="true"/>',
            '<use class="portrait-glint" href="#portrait-glyphs" fill="#e8eef7" mask="url(#glint-mask)" aria-hidden="true"/>',
            scan_beam,
            *terminal_nodes,
            "</svg>",
            "",
        ]
    )


def main() -> None:
    for (mobile, light), filename in OUTPUTS.items():
        (ROOT / "assets" / filename).write_text(
            build_svg(mobile=mobile, light=light), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
