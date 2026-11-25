"""Render the four self-contained animated ASCII systems topology SVGs (FIG.02).

Visualizes Marcus Boni's four engineering domains as interconnected ASCII
hardware/software modules with animated pure-CSS signal packets traveling along
the forward connectors and return telemetry bus.
"""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    (False, False): "systems-blueprint-v1.svg",
    (False, True): "systems-blueprint-v1-light.svg",
    (True, False): "systems-blueprint-v1-mobile.svg",
    (True, True): "systems-blueprint-v1-mobile-light.svg",
}

FONT_STACK = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

PALETTES = {
    False: {
        "surface": "#0e1014",
        "bar": "#15181e",
        "card": "#12151b",
        "card_header": "#181c24",
        "border": "#2d333d",
        "card_border": "#2a313c",
        "divider": "#232832",
        "wire": "#394250",
        "heading": "#f2f5f9",
        "copy": "#c0c9d6",
        "quiet": "#929dab",
        "meta": "#828d9c",
        "accent": "#ff5a26",
        "accent_soft": "#ff835c",
        "pulse": "#ff6a3a",
        "pill_bg": "#151921",
    },
    True: {
        "surface": "#f6f7f9",
        "bar": "#ebedf1",
        "card": "#ffffff",
        "card_header": "#f0f2f6",
        "border": "#c3cad4",
        "card_border": "#cfd6df",
        "divider": "#d8dde6",
        "wire": "#a8b2c0",
        "heading": "#14181f",
        "copy": "#363f4c",
        "quiet": "#4f5866",
        "meta": "#5d6776",
        "accent": "#c8370b",
        "accent_soft": "#dc4d22",
        "pulse": "#d84416",
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
            "WebGL · Custom GLSL",
            "Flutter · Mobile UI",
        ],
        "ref": "Portfolio · OptTime",
    },
    {
        "id": "02",
        "title": "APPLIED AI",
        "items": [
            "MCP Servers (16 tools)",
            "pgvector · Grounded RAG",
            "Retrieval Eval Harness",
            "whisper.cpp · Ollama",
        ],
        "ref": "OptTime · chatbot",
    },
    {
        "id": "03",
        "title": "SYSTEMS & DATA",
        "items": [
            "Rust (12-crate ws)",
            "Tauri 2 · UniFFI",
            "Node · C# · Python",
            "PostgreSQL · Drizzle",
        ],
        "ref": "ISPer · OptTime",
    },
    {
        "id": "04",
        "title": "CLOUD & SHIP",
        "items": [
            "Azure · Entra ID",
            "Azure DevOps · Docker",
            "CPU / CUDA Releases",
            "OpenAPI & CI Checks",
        ],
        "ref": "ISPer v0.30 · CI",
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
    arm = 6
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
        **{"stroke-width": 1.35, "stroke-linecap": "square", "aria-hidden": "true"},
    )


def io_meter(x: int, y: int, accent: str, cls_prefix: str) -> list[str]:
    """Three crisp vector LED bars that animate identically across all OS fonts."""
    opacities = (0.95, 0.60, 0.28)
    bars = []
    for idx, op in enumerate(opacities):
        bars.append(
            tag(
                "rect",
                x=x + idx * 6,
                y=y,
                width=4,
                height=10,
                rx=1,
                fill=accent,
                opacity=op,
                **{"class": f"{cls_prefix}-{idx + 1}", "aria-hidden": "true"},
            )
        )
    return bars


def build_desktop(p: dict[str, str]) -> str:
    width, height = 960, 294
    bar_h = 38
    card_w, card_h = 200, 166
    gap = 32
    x0 = 32
    card_y = 56
    bus_y = 256

    elements: list[str] = [
        tag("rect", x=0.5, y=0.5, width=width - 1, height=height - 1, rx=12, fill=p["surface"], stroke=p["border"]),
        tag("rect", width=width, height=bar_h, fill=p["bar"], **{"clip-path": "url(#bp-frame)"}),
        tag("line", x1=1, y1=bar_h, x2=width - 1, y2=bar_h, stroke=p["divider"]),
        text_el(22, 23.5, "FIG.02 // SYSTEMS TOPOLOGY · FROM METAL TO INTERFACE", fill=p["quiet"], size=12, weight=600),
        tag("circle", cx=744, cy=19, r=3.0, fill=p["accent"], **{"class": "bus-led", "aria-hidden": "true"}),
        text_el(938, 23.5, "[ 4 LAYERS · SIGNAL ACTIVE ]", fill=p["quiet"], size=11.5, **{"text-anchor": "end"}),
        tag(
            "rect",
            x=1,
            y=bar_h + 1,
            width=width - 2,
            height=height - bar_h - 2,
            fill="url(#bp-dots)",
            **{"clip-path": "url(#bp-frame)", "aria-hidden": "true"},
        ),
    ]

    # Lower return telemetry bus connecting all four modules
    bus_x_start = x0 + card_w // 2  # 132
    bus_x_end = x0 + 3 * (card_w + gap) + card_w // 2  # 828
    bus_len = bus_x_end - bus_x_start  # 696
    elements.append(
        tag(
            "path",
            d=f"M{bus_x_start} {card_y + card_h}V{bus_y}H{bus_x_end}V{card_y + card_h}",
            fill="none",
            stroke=p["wire"],
            **{"stroke-width": 1.25, "stroke-dasharray": "4 3", "aria-hidden": "true"},
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
                **{"stroke-width": 1.25, "stroke-dasharray": "4 3", "aria-hidden": "true"},
            )
        )
        elements.append(tag("circle", cx=cx, cy=bus_y, r=2.6, fill=p["wire"], **{"aria-hidden": "true"}))

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
                "stroke-width": 2.2,
                "stroke-linecap": "round",
                "stroke-dasharray": f"56 {bus_len}",
                "aria-hidden": "true",
            },
        )
    )

    # Centered bus pipeline label pill (clean → arrows for identical OS alignment)
    pill_w, pill_h = 418, 24
    pill_x = (width - pill_w) // 2
    pill_y = bus_y - pill_h // 2
    elements.append(
        tag("rect", x=pill_x, y=pill_y, width=pill_w, height=pill_h, rx=4, fill=p["pill_bg"], stroke=p["card_border"])
    )
    elements.append(
        text_el(
            width / 2,
            bus_y + 4,
            "WORKFLOW  →  ARCHITECTURE  →  EVAL  →  PRODUCTION",
            fill=p["quiet"],
            size=10.5,
            weight=600,
            **{"text-anchor": "middle", "letter-spacing": "0.04em"},
        )
    )

    # Vector LED telemetry meters left (TX) and right (RX)
    elements.append(text_el(32, bus_y + 4, "TX", fill=p["accent"], size=10.5, weight=700))
    elements.extend(io_meter(52, bus_y - 5, p["accent"], "tx-bar"))
    elements.extend(io_meter(888, bus_y - 5, p["accent"], "rx-bar"))
    elements.append(
        text_el(928, bus_y + 4, "RX", fill=p["accent"], size=10.5, weight=700, **{"text-anchor": "end"})
    )

    # Forward inter-module connectors (01 -> 02 -> 03 -> 04)
    conn_y = card_y + 84
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
                **{"stroke-width": 1.4, "stroke-dasharray": "3 3", "aria-hidden": "true"},
            )
        )
        elements.append(
            tag(
                "path",
                d=f"M{cx2 - 7} {conn_y - 4}L{cx2 - 1} {conn_y}L{cx2 - 7} {conn_y + 4}Z",
                fill=p["wire"],
                **{"aria-hidden": "true"},
            )
        )
        elements.append(
            tag(
                "circle",
                cx=cx1 + 3,
                cy=conn_y,
                r=2.8,
                fill=p["pulse"],
                **{"class": f"packet packet-{idx + 1}", "aria-hidden": "true"},
            )
        )

    # Four ASCII engineering layer cards
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
                **{"class": f"layer-glow glow-{n}", "stroke-width": 1.35, "opacity": 0, "aria-hidden": "true"},
            )
        )
        elements.append(
            tag("path", d=f"M{mx + 1} {my + 6}a5 5 0 0 1 5-5h{card_w - 12}a5 5 0 0 1 5 5v25H{mx + 1}z", fill=p["card_header"])
        )
        elements.append(tag("line", x1=mx + 1, y1=my + 31, x2=mx + card_w - 1, y2=my + 31, stroke=p["divider"]))
        elements.append(module_corners(mx, my, card_w, card_h, p["wire"]))
        elements.append(text_el(mx + 12, my + 20, f"[{mod['id']}]", fill=p["accent"], size=11, weight=700))
        elements.append(text_el(mx + 44, my + 20, str(mod["title"]), fill=p["heading"], size=11.5, weight=700))
        elements.append(
            tag(
                "circle",
                cx=mx + card_w - 14,
                cy=my + 16,
                r=3.0,
                fill=p["accent"],
                **{"class": f"node-dot dot-{n}", "opacity": 0.35, "aria-hidden": "true"},
            )
        )
        for r_idx, item in enumerate(items):
            iy = my + 54 + r_idx * 22
            elements.append(text_el(mx + 13, iy, "›", fill=p["accent_soft"], size=11.5, weight=700))
            elements.append(text_el(mx + 25, iy, item, fill=p["copy"], size=11.2))
        elements.append(tag("line", x1=mx + 12, y1=my + 138, x2=mx + card_w - 12, y2=my + 138, stroke=p["divider"]))
        elements.append(text_el(mx + 13, my + 155, f"ref: {mod['ref']}", fill=p["meta"], size=9.8))
        elements.append("</g>")

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="bp-title bp-desc">',
            '<title id="bp-title">Marcus Boni — Systems Topology (4 Engineering Layers)</title>',
            '<desc id="bp-desc">Animated ASCII architecture schematic showing four interconnected engineering layers: Interfaces, Applied AI, Systems and Data, and Cloud and Ship.</desc>',
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
            f"    @keyframes bus-flow{{0%{{stroke-dashoffset:{bus_len + 56}}} 100%{{stroke-dashoffset:-56}}}}",
            "    @keyframes hop-1{0%,16%{opacity:0;transform:translateX(0)} 18%{opacity:1;transform:translateX(0)} 27%{opacity:1;transform:translateX(24px)} 29%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes hop-2{0%,40%{opacity:0;transform:translateX(0)} 42%{opacity:1;transform:translateX(0)} 51%{opacity:1;transform:translateX(24px)} 53%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes hop-3{0%,64%{opacity:0;transform:translateX(0)} 66%{opacity:1;transform:translateX(0)} 75%{opacity:1;transform:translateX(24px)} 77%,100%{opacity:0;transform:translateX(24px)}}",
            "    @keyframes card-lit-1{0%,100%{opacity:0} 4%,18%{opacity:.82} 26%{opacity:0}}",
            "    @keyframes card-lit-2{0%,22%{opacity:0} 28%,42%{opacity:.82} 50%,100%{opacity:0}}",
            "    @keyframes card-lit-3{0%,46%{opacity:0} 52%,66%{opacity:.82} 74%,100%{opacity:0}}",
            "    @keyframes card-lit-4{0%,70%{opacity:0} 76%,90%{opacity:.82} 98%,100%{opacity:0}}",
            "    @keyframes dot-lit-1{0%,100%{opacity:.3} 4%,18%{opacity:1} 26%{opacity:.3}}",
            "    @keyframes dot-lit-2{0%,22%{opacity:.3} 28%,42%{opacity:1} 50%,100%{opacity:.3}}",
            "    @keyframes dot-lit-3{0%,46%{opacity:.3} 52%,66%{opacity:1} 74%,100%{opacity:.3}}",
            "    @keyframes dot-lit-4{0%,70%{opacity:.3} 76%,90%{opacity:1} 98%,100%{opacity:.3}}",
            "    @keyframes io-pulse{0%,100%{opacity:.22} 50%{opacity:1}}",
            "  }",
            "</style>",
            "<defs>",
            f'  <clipPath id="bp-frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
            '  <pattern id="bp-dots" width="16" height="16" patternUnits="userSpaceOnUse">',
            f'    <circle cx="2" cy="2" r="0.8" fill="{p["wire"]}" opacity="0.24"/>',
            "  </pattern>",
            "</defs>",
            *elements,
            "</svg>",
            "",
        ]
    )


def build_mobile(p: dict[str, str]) -> str:
    width, height = 480, 548
    bar_h = 38
    card_x, card_w, card_h = 20, 440, 100
    gap = 20
    y0 = 54

    elements: list[str] = [
        tag("rect", x=0.5, y=0.5, width=width - 1, height=height - 1, rx=12, fill=p["surface"], stroke=p["border"]),
        tag("rect", width=width, height=bar_h, fill=p["bar"], **{"clip-path": "url(#bp-frame)"}),
        tag("line", x1=1, y1=bar_h, x2=width - 1, y2=bar_h, stroke=p["divider"]),
        text_el(18, 23.5, "FIG.02 // SYSTEMS TOPOLOGY", fill=p["quiet"], size=12, weight=600),
        tag("circle", cx=360, cy=19, r=3.0, fill=p["accent"], **{"class": "bus-led", "aria-hidden": "true"}),
        text_el(462, 23.5, "[ 4 LAYERS ]", fill=p["quiet"], size=11.5, **{"text-anchor": "end"}),
        tag(
            "rect",
            x=1,
            y=bar_h + 1,
            width=width - 2,
            height=height - bar_h - 2,
            fill="url(#bp-dots)",
            **{"clip-path": "url(#bp-frame)", "aria-hidden": "true"},
        ),
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
                **{"class": f"layer-glow glow-{n}", "stroke-width": 1.35, "opacity": 0, "aria-hidden": "true"},
            )
        )
        elements.append(
            tag("path", d=f"M{card_x + 1} {my + 6}a5 5 0 0 1 5-5h{card_w - 12}a5 5 0 0 1 5 5v24H{card_x + 1}z", fill=p["card_header"])
        )
        elements.append(tag("line", x1=card_x + 1, y1=my + 30, x2=card_x + card_w - 1, y2=my + 30, stroke=p["divider"]))
        elements.append(module_corners(card_x, my, card_w, card_h, p["wire"]))

        elements.append(text_el(card_x + 14, my + 19.5, f"[{mod['id']}]", fill=p["accent"], size=11.5, weight=700))
        elements.append(text_el(card_x + 48, my + 19.5, str(mod["title"]), fill=p["heading"], size=12, weight=700))
        elements.append(text_el(card_x + card_w - 28, my + 19.5, f"ref: {mod['ref']}", fill=p["meta"], size=10, **{"text-anchor": "end"}))
        elements.append(
            tag("circle", cx=card_x + card_w - 14, cy=my + 15.5, r=3.0, fill=p["accent"], **{"class": f"node-dot dot-{n}", "opacity": 0.35, "aria-hidden": "true"})
        )

        positions = [(card_x + 14, my + 55), (card_x + 230, my + 55), (card_x + 14, my + 81), (card_x + 230, my + 81)]
        for (ix, iy), item in zip(positions, items):
            elements.append(text_el(ix, iy, "›", fill=p["accent_soft"], size=11.5, weight=700))
            elements.append(text_el(ix + 12, iy, item, fill=p["copy"], size=11.5))
        elements.append("</g>")

        if idx < 3:
            cy1 = my + card_h
            cy2 = cy1 + gap
            mid_x = width // 2
            elements.append(
                tag("line", x1=mid_x, y1=cy1 + 1, x2=mid_x, y2=cy2 - 6, stroke=p["wire"], **{"stroke-width": 1.4, "stroke-dasharray": "3 2", "aria-hidden": "true"})
            )
            elements.append(
                tag("path", d=f"M{mid_x - 4} {cy2 - 6}L{mid_x} {cy2 - 1}L{mid_x + 4} {cy2 - 6}Z", fill=p["wire"], **{"aria-hidden": "true"})
            )
            elements.append(
                tag("circle", cx=mid_x, cy=cy1 + 3, r=2.6, fill=p["pulse"], **{"class": f"vpacket vpacket-{n}", "aria-hidden": "true"})
            )

    elements.append(
        text_el(
            width / 2,
            532,
            "WORKFLOW  →  ARCHITECTURE  →  EVAL  →  PRODUCTION",
            fill=p["quiet"],
            size=10.5,
            weight=600,
            **{"text-anchor": "middle", "letter-spacing": "0.03em"},
        )
    )

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="bp-title bp-desc">',
            '<title id="bp-title">Marcus Boni — Systems Topology (4 Engineering Layers)</title>',
            '<desc id="bp-desc">Animated vertical ASCII architecture schematic showing four interconnected engineering layers: Interfaces, Applied AI, Systems and Data, and Cloud and Ship.</desc>',
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
            "    @keyframes vhop-1{0%,16%{opacity:0;transform:translateY(0)} 18%{opacity:1;transform:translateY(0)} 27%{opacity:1;transform:translateY(13px)} 29%,100%{opacity:0;transform:translateY(13px)}}",
            "    @keyframes vhop-2{0%,40%{opacity:0;transform:translateY(0)} 42%{opacity:1;transform:translateY(0)} 51%{opacity:1;transform:translateY(13px)} 53%,100%{opacity:0;transform:translateY(13px)}}",
            "    @keyframes vhop-3{0%,64%{opacity:0;transform:translateY(0)} 66%{opacity:1;transform:translateY(0)} 75%{opacity:1;transform:translateY(13px)} 77%,100%{opacity:0;transform:translateY(13px)}}",
            "    @keyframes card-lit-1{0%,100%{opacity:0} 4%,18%{opacity:.82} 26%{opacity:0}}",
            "    @keyframes card-lit-2{0%,22%{opacity:0} 28%,42%{opacity:.82} 50%,100%{opacity:0}}",
            "    @keyframes card-lit-3{0%,46%{opacity:0} 52%,66%{opacity:.82} 74%,100%{opacity:0}}",
            "    @keyframes card-lit-4{0%,70%{opacity:0} 76%,90%{opacity:.82} 98%,100%{opacity:0}}",
            "    @keyframes dot-lit-1{0%,100%{opacity:.3} 4%,18%{opacity:1} 26%{opacity:.3}}",
            "    @keyframes dot-lit-2{0%,22%{opacity:.3} 28%,42%{opacity:1} 50%,100%{opacity:.3}}",
            "    @keyframes dot-lit-3{0%,46%{opacity:.3} 52%,66%{opacity:1} 74%,100%{opacity:.3}}",
            "    @keyframes dot-lit-4{0%,70%{opacity:.3} 76%,90%{opacity:1} 98%,100%{opacity:.3}}",
            "    @keyframes io-pulse{0%,100%{opacity:.22} 50%{opacity:1}}",
            "  }",
            "</style>",
            "<defs>",
            f'  <clipPath id="bp-frame"><rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="11"/></clipPath>',
            '  <pattern id="bp-dots" width="16" height="16" patternUnits="userSpaceOnUse">',
            f'    <circle cx="2" cy="2" r="0.8" fill="{p["wire"]}" opacity="0.24"/>',
            "  </pattern>",
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
