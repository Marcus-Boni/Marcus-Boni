"""Render the profile hero header SVG assets.

The generator is intentionally dependency-free and deterministic. It reuses the
ASCII portrait glyphs from assets/ascii-portrait.svg while leaving that source
asset untouched.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASCII_SOURCE = ROOT / "assets" / "ascii-portrait.svg"
OUTPUTS = {
    (False, False): ROOT / "assets" / "profile-header.svg",
    (False, True): ROOT / "assets" / "profile-header-light.svg",
    (True, False): ROOT / "assets" / "profile-header-mobile.svg",
    (True, True): ROOT / "assets" / "profile-header-mobile-light.svg",
}

FONT_STACK = (
    "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
)


def _palette(light: bool) -> dict[str, str]:
    if light:
        return {
            "bg": "#f6f8fa",
            "panel": "#ffffff",
            "panel_2": "#f1f4f8",
            "stroke": "#d0d7de",
            "soft": "#8c959f",
            "text": "#24292f",
            "muted": "#57606a",
            "bone": "#24292f",
            "accent": "#a65a35",
            "green": "#1a7f37",
            "shadow": "#afb8c133",
            "portrait": "#57606a",
            "portrait_hi": "#a65a35",
        }
    return {
        "bg": "#0d1117",
        "panel": "#111820",
        "panel_2": "#161b22",
        "stroke": "#30363d",
        "soft": "#6e7681",
        "text": "#f0f6fc",
        "muted": "#c9d1d9",
        "bone": "#f7efe7",
        "accent": "#efaa82",
        "green": "#39d353",
        "shadow": "#01040966",
        "portrait": "#c9d1d9",
        "portrait_hi": "#efaa82",
    }


def _read_portrait_lines() -> list[str]:
    tree = ET.parse(ASCII_SOURCE)
    root = tree.getroot()
    namespace = ""
    if root.tag.startswith("{"):
        namespace = root.tag.split("}", 1)[0] + "}"

    lines = [
        node.text
        for node in root.iter(f"{namespace}text")
        if node.text and node.text.strip()
    ]
    if not lines:
        raise RuntimeError(f"No ASCII portrait text found in {ASCII_SOURCE}")

    common_indent = min(len(line) - len(line.lstrip(" ")) for line in lines)
    trimmed = [line[common_indent:].rstrip() for line in lines]
    max_cols = max(len(line) for line in trimmed)
    return [line.ljust(max_cols) for line in trimmed]


def _tag(
    name: str,
    attrs: dict[str, str | int | float] | None = None,
    content: str | None = None,
) -> str:
    rendered_attrs = ""
    if attrs:
        rendered_attrs = " " + " ".join(
            f'{key}="{escape(str(value), quote=True)}"' for key, value in attrs.items()
        )
    if content is None:
        return f"<{name}{rendered_attrs}/>"
    return f"<{name}{rendered_attrs}>{content}</{name}>"


def _text(
    x: float,
    y: float,
    value: str,
    *,
    fill: str,
    size: float,
    weight: int | None = None,
    opacity: float | None = None,
    anchor: str | None = None,
) -> str:
    attrs: dict[str, str | int | float] = {
        "x": x,
        "y": y,
        "fill": fill,
        "font-size": size,
    }
    if weight is not None:
        attrs["font-weight"] = weight
    if opacity is not None:
        attrs["opacity"] = opacity
    if anchor is not None:
        attrs["text-anchor"] = anchor
    return _tag("text", attrs, escape(value))


def _portrait(
    *,
    x: float,
    y: float,
    height: float,
    palette: dict[str, str],
    opacity: float = 0.72,
) -> str:
    lines = _read_portrait_lines()
    line_height = height / len(lines)
    font_size = line_height * 10 / 11
    rendered: list[str] = []
    for index, line in enumerate(lines):
        fill = palette["portrait_hi"] if index % 9 in (3, 4) else palette["portrait"]
        y_pos = round(y + index * line_height, 2)
        rendered.append(
            _tag(
                "text",
                {
                    "x": x,
                    "y": y_pos,
                    "fill": fill,
                    "font-size": round(font_size, 2),
                    "opacity": opacity,
                    "xml:space": "preserve",
                },
                escape(line),
            )
        )
    return "\n".join(rendered)


def _desktop(palette: dict[str, str]) -> str:
    w, h = 960, 310
    parts: list[str] = [
        _tag("rect", {"width": w, "height": h, "rx": 16, "fill": palette["bg"]}),
        _tag(
            "path",
            {
                "d": "M42 86 H316 M658 84 H884 M672 252 H904",
                "fill": "none",
                "stroke": palette["soft"],
                "stroke-width": 1,
                "opacity": 0.26,
            },
        ),
        _tag(
            "rect",
            {
                "x": 28,
                "y": 24,
                "width": 904,
                "height": 262,
                "rx": 12,
                "fill": palette["panel"],
                "stroke": palette["stroke"],
            },
        ),
        _tag(
            "rect",
            {
                "x": 28,
                "y": 24,
                "width": 904,
                "height": 38,
                "rx": 12,
                "fill": palette["panel_2"],
                "stroke": palette["stroke"],
            },
        ),
    ]

    for idx, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        parts.append(_tag("circle", {"cx": 50 + idx * 18, "cy": 43, "r": 5, "fill": color}))
    parts.extend(
        [
            _text(480, 47, "marcus@github:~", fill=palette["muted"], size=12, anchor="middle"),
            _text(58, 96, "marcus@github:~", fill=palette["green"], size=16, weight=700),
            _text(204, 96, "$ whoami", fill=palette["bone"], size=16, weight=700),
            _text(58, 154, "Marcus Boni", fill=palette["bone"], size=51, weight=800),
            _text(62, 193, "Software developer", fill=palette["accent"], size=23, weight=700),
            _text(
                62,
                227,
                "Web apps. Integrations. Developer tools.",
                fill=palette["muted"],
                size=19,
            ),
            _tag(
                "rect",
                {
                    "x": 62,
                    "y": 252,
                    "width": 430,
                    "height": 1,
                    "fill": palette["stroke"],
                },
            ),
            _text(62, 273, "Espírito Santo, Brazil", fill=palette["muted"], size=14),
            _text(260, 273, "marcusboni.com.br", fill=palette["accent"], size=14, weight=700),
            _portrait(
                x=704,
                y=86,
                height=196,
                palette=palette,
                opacity=0.66,
            ),
        ]
    )
    return "\n".join(parts)


def _mobile(palette: dict[str, str]) -> str:
    w, h = 480, 340
    parts: list[str] = [
        _tag("rect", {"width": w, "height": h, "rx": 18, "fill": palette["bg"]}),
        _tag(
            "rect",
            {
                "x": 22,
                "y": 20,
                "width": 436,
                "height": 298,
                "rx": 13,
                "fill": palette["panel"],
                "stroke": palette["stroke"],
            },
        ),
        _tag(
            "rect",
            {
                "x": 22,
                "y": 20,
                "width": 436,
                "height": 38,
                "rx": 13,
                "fill": palette["panel_2"],
                "stroke": palette["stroke"],
            },
        ),
    ]
    for idx, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        parts.append(_tag("circle", {"cx": 42 + idx * 17, "cy": 38, "r": 5, "fill": color}))

    parts.extend(
        [
            _text(244, 44, "marcus@github:~", fill=palette["muted"], size=16, anchor="middle"),
            _text(42, 88, "$ whoami", fill=palette["green"], size=16, weight=700),
            _text(42, 143, "Marcus", fill=palette["bone"], size=50, weight=800),
            _text(42, 196, "Boni", fill=palette["bone"], size=50, weight=800),
            _text(44, 236, "Software developer", fill=palette["accent"], size=25, weight=700),
            _text(44, 275, "Web apps. Integrations.", fill=palette["muted"], size=22),
            _text(44, 304, "Developer tools.", fill=palette["muted"], size=22),
            _portrait(
                x=324,
                y=86,
                height=156,
                palette=palette,
                opacity=0.48,
            ),
        ]
    )
    return "\n".join(parts)


def build_svg(mobile: bool = False, light: bool = False) -> str:
    """Build one profile header SVG as a deterministic string."""
    palette = _palette(light)
    width, height = (480, 340) if mobile else (960, 310)
    title = "Marcus Boni profile header"
    desc = (
        "Mobile terminal-style profile header for Marcus Boni, software developer."
        if mobile
        else (
            "Terminal-style profile header for Marcus Boni, software developer in "
            "Espírito Santo, Brazil."
        )
    )
    body = _mobile(palette) if mobile else _desktop(palette)

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f"<title id=\"title\">{escape(title)}</title>",
            f"<desc id=\"desc\">{escape(desc)}</desc>",
            "<style>",
            f"  text{{font-family:{FONT_STACK};dominant-baseline:alphabetic}}",
            "  svg{shape-rendering:geometricPrecision;text-rendering:optimizeLegibility}",
            "</style>",
            body,
            "</svg>",
            "",
        ]
    )


def main() -> None:
    first_pass: dict[tuple[bool, bool], str] = {}
    second_pass: dict[tuple[bool, bool], str] = {}
    for key in OUTPUTS:
        first_pass[key] = build_svg(mobile=key[0], light=key[1])
        second_pass[key] = build_svg(mobile=key[0], light=key[1])
    if first_pass != second_pass:
        raise RuntimeError("Non-deterministic SVG output")

    for key, path in OUTPUTS.items():
        path.write_text(first_pass[key], encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
