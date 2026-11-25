"""Render the four self-contained monochrome ASCII architecture blueprint SVGs.

Strictly follows the silver, white, gray, and black palette of the profile hero,
showing four minimalist engineering layers linked by an animated silver signal bus.
"""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    (False, False): "systems-blueprint-v2.svg",
    (False, True): "systems-blueprint-v2-light.svg",
    (True, False): "systems-blueprint-v2-mobile.svg",
    (True, True): "systems-blueprint-v2-mobile-light.svg",
}

FONT_STACK = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PALETTES = {
    False: {
        "surface": "#0e1014",
        "bar": "#14171d",
        "card": "#11141a",
        "card_header": "#171b22",
        "border": "#2d333d",
        "card_border": "#282e38",
        "divider": "#222730",
        "wire": "#3e4654",
        "heading": "#f4f6f9",
        "copy": "#bcc4d0",
        "quiet": "#929ca9",
        "accent": "#f1f4f8",
        "accent_soft": "#aeb7c4",
        "pulse": "#ffffff",
        "pill_bg": "#141820",
    },
    True: {
        "surface": "#f6f7f9",
        "bar": "#ebedf1",
        "card": "#ffffff",
        "card_header": "#f0f2f6",
        "border": "#c3cad4",
        "card_border": "#cfd6df",
        "divider": "#d9dee6",
        "wire": "#a5afbd",
        "heading": "#13171e",
        "copy": "#37404d",
        "quiet": "#4f5866",
        "accent": "#161a22",
        "accent_soft": "#555f6e",
        "pulse": "#161a22",
        "pill_bg": "#ffffff",
    },
}

MODULES: list[dict[str, object]] = [
    {
        "id": "01",
        "title": "INTERFACES",
        "items": [
            "React · Next.js 16",
            "TypeScript · Tailwind",
            "WebGL · Flutter",
        ],
    },
    {
        "id": "02",
        "title": "APPLIED AI",
        "items": [
            "MCP Servers (16 tools)",
            "pgvector · Grounded RAG",
            "whisper.cpp · Evals",
        ],
    },
    {
        "id": "03",
        "title": "SYSTEMS & DATA",
        "items": [
            "Rust · Tauri 2 · UniFFI",
            "Node · C# · Python",
            "PostgreSQL · Drizzle",
        ],
    },
    {
        "id": "04",
        "title": "CLOUD & SHIP",
        "items": [
            "Azure · Entra ID",
            "Azure DevOps · Docker",
            "CPU/CUDA · CI Releases",
        ],
    },
]


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


def module_corners(x: int, y: int, w: int, h: int, stroke: str) -> str:
    arm = 5
    d = (
        f"M{x} {y + arm}V{y}H{x + arm}"
        f"M{x + w - arm} {y}H{x + w}V{y + arm}"
        f"M{x} {y + h - arm}V{y + h}H{x + arm}"
        f"M{x + w - arm} {y + h}H{x + w}V{y + h - arm}"
    )
    return tag(
        "path",
        d=d,
        fill="none",
        stroke=stroke,
        **{"stroke-width": 1.15, "stroke-linecap": "square", "aria-hidden": "true"},
    )


def io_meter(x: int, y: int, fill: str, cls_prefix: str) -> list[str]:
    opacities = (0.9, 0.55, 0.25)
    return [
        tag(
            "rect",
            x=x + idx * 6,
            y=y,
            width=3.5,
            height=9,
            rx=1,
            fill=fill,
            opacity=op,
            **{"class": f"{cls_prefix}-{idx + 1}", "aria-hidden": "true"},
        )
        for idx, op in enumerate(opacities)
    ]


def build_desktop(p: dict[str, str]) -> str:
    width, height = 960, 248
    bar_h = 36
    card_w, card_h = 200, 126
    gap = 32
    x0 = 32
    card_y = 54
    bus_y = 214

    elements: list[str] = [
        tag("rect", x=0.5, y=0.5, width=width - 1, height=height - 1, rx=12, fill=p["surface"], stroke=p["border"]),
        tag("rect", width=width, height=bar_h, fill=p["bar"], **{"clip-path": "url(#bp-frame)"}),
        tag("line", x1=1, y1=bar_h, x2=width - 1, y2=bar_h, stroke=p["divider"]),
        text_el(22, 22, "SYSTEMS ARCHITECTURE", fill=p["quiet"], size=11.5, weight=600, **{"letter-spacing": "0.06em"}),
        tag("circle", cx=830, cy=18, r=2.8, fill=p["accent"], **{"class": "bus-led", "aria-hidden": "true"}),
        text_el(938, 22, "[ 4 LAYERS ]", fill=p["quiet"], size=11.5, **{"text-anchor": "end"}),
    ]

    # Lower telemetry return bus
    bus_x_start = x0 + card_w // 2
    bus_x_end = x0 + 3 * (card_w + gap) + card_w // 2
    bus_len = bus_x_end - bus_x_start
    elements.append(
        tag(
            "path",
            d=f"M{bus_x_start} {card_y + card_h}V{bus_y}H{bus_x_end}V{card_y + card_h}",
            fill="none",
            stroke=p["wire"],
            **{"stroke-width": 1.15, "stroke-dasharray": "4 3", "aria-hidden": "true"},
        )
    )
    for idx in (1, 2):
        cx = x0 + idx * (card_w + gap) + card_w // 2
        elements.append(
            tag(
                "line",
                x1=cx,
                y1=card_y + card_h,
                x2=cx,
                y2=bus_y,
                stroke=p["wire"],
                **{"stroke-width": 1.15, "stroke-dasharray": "4 3", "aria-hidden": "true"},
            )
        )
        elements.append(tag("circle", cx=cx, cy=bus_y, r=2.3, fill=p["wire"], **{"aria-hidden": "true"}))

    elements.append(
        tag(
            "line",
            x1=bus_x_start,
            y1=bus_y,
            x2=bus_x_end,
            y2=bus_y,
            stroke=p["pulse"],
            **{
                "class": "bus-signal",
                "stroke-width": 2.0,
                "stroke-linecap": "round",
                "stroke-dasharray": f"54 {bus_len}",
                "aria-hidden": "true",
            },
        )
    )

    pill_w, pill_h = 376, 22
    pill_x = (width - pill_w) // 2
    pill_y = bus_y - pill_h // 2
    elements.append(
        tag("rect", x=pill_x, y=pill_y, width=pill_w, height=pill_h, rx=4, fill=p["pill_bg"], stroke=p["card_border"])
    )
    elements.append(
        text_el(
            width / 2,
            bus_y + 3.5,
            "DISCOVERY  →  ARCHITECTURE  →  EVAL  →  DEPLOY",
            fill=p["quiet"],
            size=10.2,
            weight=600,
            **{"text-anchor": "middle", "letter-spacing": "0.04em"},
        )
    )

    elements.append(text_el(32, bus_y + 3.5, "TX", fill=p["quiet"], size=10, weight=700))
    elements.extend(io_meter(50, bus_y - 4.5, p["accent"], "tx-bar"))
    elements.extend(io_meter(891, bus_y - 4.5, p["accent"], "rx-bar"))
    elements.append(
        text_el(928, bus_y + 3.5, "RX", fill=p["quiet"], size=10, weight=700, **{"text-anchor": "end"})
    )

    # Inter-module connectors
    conn_y = card_y + 68
    for idx in range(3):
        cx1 = x0 + idx * (card_w + gap) + card_w
        cx2 = cx1 + gap
        elements.append(
            tag(
                "line",
                x1=cx1 + 1,
                y1=conn_y,
                x2=cx2 - 7,
                y2=conn_y,
                stroke=p["wire"],
                **{"stroke-width": 1.3, "stroke-dasharray": "3 3", "aria-hidden": "true"},
            )
        )
        elements.append(
            tag(
                "path",
                d=f"M{cx2 - 7} {conn_y - 3.5}L{cx2 - 1} {conn_y}L{cx2 - 7} {conn_y + 3.5}Z",
                fill=p["wire"],
                **{"aria-hidden": "true"},
            )
        )
        elements.append(
            tag(
                "circle",
                cx=cx1 + 3,
                cy=conn_y,
                r=2.5,
                fill=p["pulse"],
                **{"class": f"packet packet-{idx + 1}", "aria-hidden": "true"},
            )
        )

    # Four minimalist monochrome cards
    for idx, mod in enumerate(MODULES):
        mx = x0 + idx * (card_w + gap)
        my = card_y
        n = idx + 1
        items: list[str] = mod["items"]  # type: ignore[assignment]
        elements.append(f'<g class="layer-card layer-{n}">')
        elements.append(
            tag("rect", x=mx, y=my, width=card_w, height=card_h, rx=6, fill=p["card"], stroke=p["card_border"])
        )
        elements.append(
            tag(
                "rect",
                x=mx,
                y=my,
                width=card_w,
                height=card_h,
                rx=6,
                fill="none",
                stroke=p["accent"],
                **{"class": f"layer-glow glow-{n}", "stroke-width": 1.3, "opacity": 0, "aria-hidden": "true"},
            )
        )
        elements.append(
            tag("path", d=f"M{mx + 1} {my + 6}a5 5 0 0 1 5-5h{card_w - 12}a5 5 0 0 1 5 5v24H{mx + 1}z", fill=p["card_header"])
        )
        elements.append(tag("line", x1=mx + 1, y1=my + 30, x2=mx + card_w - 1, y2=my + 30, stroke=p["divider"]))
        elements.append(module_corners(mx, my, card_w, card_h, p["wire"]))
        elements.append(text_el(mx + 12, my + 19.5, str(mod["id"]), fill=p["quiet"], size=11, weight=700))
        elements.append(text_el(mx + 34, my + 19.5, str(mod["title"]), fill=p["heading"], size=11.5, weight=700))
        elements.append(
            tag(
                "circle",
                cx=mx + card_w - 14,
                cy=my + 15.5,
                r=2.8,
                fill=p["accent"],
                **{"class": f"node-dot dot-{n}", "opacity": 0.28, "aria-hidden": "true"},
            )
        )
        for r_idx, item in enumerate(items):
            iy = my + 56 + r_idx * 24
            elements.append(text_el(mx + 13, iy, "›", fill=p["accent_soft"], size=11.5, weight=700))
            elements.append(text_el(mx + 25, iy, item, fill=p["copy"], size=11.2))
        elements.append("</g>")

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="bp-title bp-desc">',
            '<title id="bp-title">Marcus Boni — Systems Architecture</title>',
            '<desc id="bp-desc">Minimalist monochrome ASCII architecture schematic showing four connected engineering layers: Interfaces, Applied AI, Systems and Data, and Cloud and Ship.</desc>',
            "<style>",
            f"  text{{font-family:{FONT_STACK}}}",
            "  .packet,.bus-signal{display:none}",
            "  @media (prefers-reduced-motion: no-preference){",
            "    .packet,.bus-signal{display:inline}",
            "    .bus-signal{animation:bus-flow 6.4s linear infinite}",
            "    .packet-1{animation:hop-1 6.4s linear infinite}",
            "    .packet-2{animation:hop-2 6.4s linear infinite}",
            "    .packet-3{animation:hop-3 6.4s linear infinite}",
            "    .glow-1{animation:card-lit-1 6.4s ease-in-out infinite}",
            "    .glow-2{animation:card-lit-2 6.4s ease-in-out infinite}",
            "    .glow-3{animation:card-lit-3 6.4s ease-in-out infinite}",
            "    .glow-4{animation:card-lit-4 6.4s ease-in-out infinite}",
            "    .dot-1{animation:dot-lit-1 6.4s ease-in-out infinite}",
            "    .dot-2{animation:dot-lit-2 6.4s ease-in-out infinite}",
            "    .dot-3{animation:dot-lit-3 6.4s ease-in-out infinite}",
            "    .dot-4{animation:dot-lit-4 6.4s ease-in-out infinite}",
            "    .tx-bar-1{animation:io-pulse 1.6s ease-in-out 0s infinite}",
            "    .tx-bar-2{animation:io-pulse 1.6s ease-in-out .22s infinite}",
            "    .tx-bar-3{animation:io-pulse 1.6s ease-in-out .44s infinite}",
            "    .rx-bar-1{animation:io-pulse 1.6s ease-in-out .84s infinite}",
            "    .rx-bar-2{animation:io-pulse 1.6s ease-in-out .62s infinite}",
            "    .rx-bar-3{animation:io-pulse 1.6s ease-in-out .40s infinite}",
            "    .bus-led{animation:io-pulse 2.4s ease-in-out infinite}",
            f"    @keyframes bus-flow{{0%{{stroke-dashoffset:{bus_len + 54}}} 100%{{stroke-dashoffset:-54}}}}",
            "    @keyframes hop-1{0%,16%{opacity:0;transform:translateX(0)} 18%{opacity:1;transform:translateX(0)} 27%{opacity:1;transform:translateX(24px)} 29%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes hop-2{0%,40%{opacity:0;transform:translateX(0)} 42%{opacity:1;transform:translateX(0)} 51%{opacity:1;transform:translateX(24px)} 53%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes hop-3{0%,64%{opacity:0;transform:translateX(0)} 66%{opacity:1;transform:translateX(0)} 75%{opacity:1;transform:translateX(24px)} 77%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes card-lit-1{0%,100%{opacity:0} 4%,18%{opacity:.78} 26%{opacity:0}}",
            "    @keyframes card-lit-2{0%,22%{opacity:0} 28%,42%{opacity:.78} 50%,100%{opacity:0}}",
            "    @keyframes card-lit-3{0%,46%{opacity:0} 52%,66%{opacity:.78} 74%,100%{opacity:0}}",
            "    @keyframes card-lit-4{0%,70%{opacity:0} 76%,90%{opacity:.78} 98%,100%{opacity:0}}",
            "    @keyframes dot-lit-1{0%,100%{opacity:.28} 4%,18%{opacity:1} 26%{opacity:.28}}",
            "    @keyframes dot-lit-2{0%,22%{opacity:.28} 28%,42%{opacity:1} 50%,100%{opacity:.28}}",
            "    @keyframes dot-lit-3{0%,46%{opacity:.28} 52%,66%{opacity:1} 74%,100%{opacity:.28}}",
            "    @keyframes dot-lit-4{0%,70%{opacity:.28} 76%,90%{opacity:1} 98%,100%{opacity:.28}}",
            "    @keyframes io-pulse{0%,100%{opacity:.2} 50%{opacity:.95}}",
            "  }",
            "</style>",
            "<defs>",
            f'  <clipPath id="bp-frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
            "</defs>",
            *elements,
            "</svg>",
            "",
        ]
    )


def build_mobile(p: dict[str, str]) -> str:
    width, height = 480, 488
    bar_h = 36
    card_x, card_w, card_h = 20, 440, 86
    gap = 18
    y0 = 52

    elements: list[str] = [
        tag("rect", x=0.5, y=0.5, width=width - 1, height=height - 1, rx=12, fill=p["surface"], stroke=p["border"]),
        tag("rect", width=width, height=bar_h, fill=p["bar"], **{"clip-path": "url(#bp-frame)"}),
        tag("line", x1=1, y1=bar_h, x2=width - 1, y2=bar_h, stroke=p["divider"]),
        text_el(18, 22, "SYSTEMS ARCHITECTURE", fill=p["quiet"], size=11.5, weight=600, **{"letter-spacing": "0.05em"}),
        tag("circle", cx=360, cy=18, r=2.8, fill=p["accent"], **{"class": "bus-led", "aria-hidden": "true"}),
        text_el(462, 22, "[ 4 LAYERS ]", fill=p["quiet"], size=11.5, **{"text-anchor": "end"}),
    ]

    for idx, mod in enumerate(MODULES):
        my = y0 + idx * (card_h + gap)
        n = idx + 1
        items: list[str] = mod["items"]  # type: ignore[assignment]

        elements.append(f'<g class="layer-card layer-{n}">')
        elements.append(
            tag("rect", x=card_x, y=my, width=card_w, height=card_h, rx=6, fill=p["card"], stroke=p["card_border"])
        )
        elements.append(
            tag(
                "rect",
                x=card_x,
                y=my,
                width=card_w,
                height=card_h,
                rx=6,
                fill="none",
                stroke=p["accent"],
                **{"class": f"layer-glow glow-{n}", "stroke-width": 1.3, "opacity": 0, "aria-hidden": "true"},
            )
        )
        elements.append(
            tag("path", d=f"M{card_x + 1} {my + 6}a5 5 0 0 1 5-5h{card_w - 12}a5 5 0 0 1 5 5v23H{card_x + 1}z", fill=p["card_header"])
        )
        elements.append(tag("line", x1=card_x + 1, y1=my + 29, x2=card_x + card_w - 1, y2=my + 29, stroke=p["divider"]))
        elements.append(module_corners(card_x, my, card_w, card_h, p["wire"]))

        elements.append(text_el(card_x + 14, my + 19, str(mod["id"]), fill=p["quiet"], size=11.5, weight=700))
        elements.append(text_el(card_x + 38, my + 19, str(mod["title"]), fill=p["heading"], size=12, weight=700))
        elements.append(
            tag("circle", cx=card_x + card_w - 14, cy=my + 15, r=2.8, fill=p["accent"], **{"class": f"node-dot dot-{n}", "opacity": 0.28, "aria-hidden": "true"})
        )

        # Clean compact layout: row 1 has items 0 & 1, row 2 has item 2
        elements.append(text_el(card_x + 14, my + 52, "›", fill=p["accent_soft"], size=11.5, weight=700))
        elements.append(text_el(card_x + 26, my + 52, items[0], fill=p["copy"], size=11.5))
        elements.append(text_el(card_x + 232, my + 52, "›", fill=p["accent_soft"], size=11.5, weight=700))
        elements.append(text_el(card_x + 244, my + 52, items[1], fill=p["copy"], size=11.5))
        elements.append(text_el(card_x + 14, my + 74, "›", fill=p["accent_soft"], size=11.5, weight=700))
        elements.append(text_el(card_x + 26, my + 74, items[2], fill=p["copy"], size=11.5))
        elements.append("</g>")

        if idx < 3:
            cy1 = my + card_h
            cy2 = cy1 + gap
            mid_x = width // 2
            elements.append(
                tag("line", x1=mid_x, y1=cy1 + 1, x2=mid_x, y2=cy2 - 6, stroke=p["wire"], **{"stroke-width": 1.3, "stroke-dasharray": "3 2", "aria-hidden": "true"})
            )
            elements.append(
                tag("path", d=f"M{mid_x - 3.5} {cy2 - 6}L{mid_x} {cy2 - 1}L{mid_x + 3.5} {cy2 - 6}Z", fill=p["wire"], **{"aria-hidden": "true"})
            )
            elements.append(
                tag("circle", cx=mid_x, cy=cy1 + 3, r=2.4, fill=p["pulse"], **{"class": f"vpacket vpacket-{n}", "aria-hidden": "true"})
            )

    elements.append(
        text_el(
            width / 2,
            472,
            "DISCOVERY  →  ARCHITECTURE  →  EVAL  →  DEPLOY",
            fill=p["quiet"],
            size=10.2,
            weight=600,
            **{"text-anchor": "middle", "letter-spacing": "0.03em"},
        )
    )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="bp-title bp-desc">',
            '<title id="bp-title">Marcus Boni — Systems Architecture</title>',
            '<desc id="bp-desc">Minimalist vertical monochrome ASCII architecture schematic showing four connected engineering layers: Interfaces, Applied AI, Systems and Data, and Cloud and Ship.</desc>',
            "<style>",
            f"  text{{font-family:{FONT_STACK}}}",
            "  .vpacket{display:none}",
            "  @media (prefers-reduced-motion: no-preference){",
            "    .vpacket{display:inline}",
            "    .vpacket-1{animation:vhop-1 6.4s linear infinite}",
            "    .vpacket-2{animation:vhop-2 6.4s linear infinite}",
            "    .vpacket-3{animation:vhop-3 6.4s linear infinite}",
            "    .glow-1{animation:card-lit-1 6.4s ease-in-out infinite}",
            "    .glow-2{animation:card-lit-2 6.4s ease-in-out infinite}",
            "    .glow-3{animation:card-lit-3 6.4s ease-in-out infinite}",
            "    .glow-4{animation:card-lit-4 6.4s ease-in-out infinite}",
            "    .dot-1{animation:dot-lit-1 6.4s ease-in-out infinite}",
            "    .dot-2{animation:dot-lit-2 6.4s ease-in-out infinite}",
            "    .dot-3{animation:dot-lit-3 6.4s ease-in-out infinite}",
            "    .dot-4{animation:dot-lit-4 6.4s ease-in-out infinite}",
            "    .bus-led{animation:io-pulse 2.4s ease-in-out infinite}",
            "    @keyframes vhop-1{0%,16%{opacity:0;transform:translateY(0)} 18%{opacity:1;transform:translateY(0)} 27%{opacity:1;transform:translateY(11px)} 29%,100%{opacity:0;transform:translateY(11px)}}",
            "    @keyframes vhop-2{0%,40%{opacity:0;transform:translateY(0)} 42%{opacity:1;transform:translateY(0)} 51%{opacity:1;transform:translateY(11px)} 53%,100%{opacity:0;transform:translateY(11px)}}",
            "    @keyframes vhop-3{0%,64%{opacity:0;transform:translateY(0)} 66%{opacity:1;transform:translateY(0)} 75%{opacity:1;transform:translateY(11px)} 77%,100%{opacity:0;transform:translateY(11px)}}",
            "    @keyframes card-lit-1{0%,100%{opacity:0} 4%,18%{opacity:.78} 26%{opacity:0}}",
            "    @keyframes card-lit-2{0%,22%{opacity:0} 28%,42%{opacity:.78} 50%,100%{opacity:0}}",
            "    @keyframes card-lit-3{0%,46%{opacity:0} 52%,66%{opacity:.78} 74%,100%{opacity:0}}",
            "    @keyframes card-lit-4{0%,70%{opacity:0} 76%,90%{opacity:.78} 98%,100%{opacity:0}}",
            "    @keyframes dot-lit-1{0%,100%{opacity:.28} 4%,18%{opacity:1} 26%{opacity:.28}}",
            "    @keyframes dot-lit-2{0%,22%{opacity:.28} 28%,42%{opacity:1} 50%,100%{opacity:.28}}",
            "    @keyframes dot-lit-3{0%,46%{opacity:.28} 52%,66%{opacity:1} 74%,100%{opacity:.28}}",
            "    @keyframes dot-lit-4{0%,70%{opacity:.28} 76%,90%{opacity:1} 98%,100%{opacity:.28}}",
            "    @keyframes io-pulse{0%,100%{opacity:.2} 50%{opacity:.95}}",
            "  }",
            "</style>",
            "<defs>",
            f'  <clipPath id="bp-frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
            "</defs>",
            *elements,
            "</svg>",
            "",
        ]
    )


def build_svg(mobile: bool = False, light: bool = False) -> str:
    """Build one systems blueprint SVG as a deterministic string."""
    palette = PALETTES[light]
    return build_mobile(palette) if mobile else build_desktop(palette)


def main() -> None:
    for (mobile, light), filename in OUTPUTS.items():
        (ROOT / "assets" / filename).write_text(
            build_svg(mobile=mobile, light=light), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
