"""Gera o cartao de informacoes estilo `neofetch` (assets/info-card.svg).

Cada linha entra com fade, escalonada de cima para baixo, logo depois que o
retrato termina de imprimir. Roda uma vez e congela.

Para atualizar o conteudo edite HOST e ROWS abaixo e rode de novo. Esse cartao
e proposital e deliberadamente estatico: sao fatos sobre voce, nao metricas.

Uso:
    python scripts/make_info_card.py [saida.svg]
    STATIC=1 python scripts/make_info_card.py    # quadro congelado p/ preview
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape

# ------------------------------------------------------------------- conteudo

HOST = "marcus@github"

# (rotulo, valor, cor-do-valor). None insere uma linha em branco.
ROWS: list[tuple[str, str, str] | None] = [
    ("Role", "Web Developer, full-stack leaning", "#e6edf3"),
    ("Company", "Optsolv", "#e6edf3"),
    ("Location", "Espirito Santo, Brazil (UTC-3)", "#e6edf3"),
    ("Uptime", "since Oct 2022 - building in public", "#e6edf3"),
    None,
    ("Frontend", "React . Next.js . TypeScript . Tailwind", "#7ee787"),
    ("Backend", "Node . Java/Spring . .NET . Python", "#7ee787"),
    ("Data", "PostgreSQL . SQL Server . Supabase . Drizzle", "#7ee787"),
    ("Cloud", "Azure . Docker . GitHub Actions", "#7ee787"),
    ("Mobile", "React Native . Flutter", "#7ee787"),
    None,
    ("Focus", "multi-tenant SaaS architecture", "#79c0ff"),
    ("Learning", "Rust . MCP & AI agents", "#79c0ff"),
    ("Repos", "70 public . 3 yrs shipping", "#79c0ff"),
    None,
    ("Web", "marcusboni.com.br", "#d2a8ff"),
]

# ----------------------------------------------------------------- aparencia

W = 660  # a altura e calculada a partir do conteudo, no fim do build
PAD = 26
BAR_H = 34  # altura da barra de titulo do "terminal"
FONT = 13.0
LINE_H = 19.0
LABEL_W = 96  # coluna dos rotulos

BG = "#0d1117"
BAR = "#161b22"
BORDER = "#30363d"
LABEL = "#8b949e"
DOTS = ("#ff5f56", "#ffbd2e", "#27c93f")
PALETTE = ["#39d353", "#7ee787", "#79c0ff", "#d2a8ff", "#ffa657", "#ff7b72", "#8b949e"]

ROW_DELAY = 0.055
ROW_DUR = 0.42
START = 0.45  # espera o retrato ganhar corpo antes de comecar


def build_svg(static: bool) -> str:
    mono = ("font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"
            "'DejaVu Sans Mono',monospace")

    # Quantas linhas animadas existem, para fechar a janela de tempo comum.
    steps = 2 + sum(1 for r in ROWS if r) + len(PALETTE) + 1
    total = START + steps * ROW_DELAY + ROW_DUR

    def anim(delay: float) -> str:
        """Fade escalonado, sempre comecando em 0s.

        O atraso vai no keyTimes em vez do `begin` para que o estado base do
        elemento possa ser o visivel: se o cliente ignorar SMIL, o cartao
        aparece completo e parado, nunca vazio.
        """
        if static:
            return ""
        d = START + delay
        return (
            f'<animate attributeName="opacity" values="0;0;1;1" '
            f'keyTimes="0;{d / total:.4f};{(d + ROW_DUR) / total:.4f};1" '
            f'dur="{total:.2f}s" begin="0s" fill="freeze"/>'
        )

    body: list[str] = []
    y = BAR_H + PAD + 14
    step = 0

    # Cabecalho: host + regua, como o neofetch de verdade.
    body.append(f'<g><text x="{PAD}" y="{y}" fill="#39d353" font-weight="bold">'
                f"{escape(HOST)}</text>{anim(0)}</g>")
    y += 15
    body.append(f'<g><text x="{PAD}" y="{y}" class="label">'
                f'{"-" * 34}</text>{anim(ROW_DELAY)}</g>')
    y += LINE_H + 5
    step = 2

    for row in ROWS:
        if row is None:
            y += LINE_H * 0.45
            continue
        label, value, color = row
        dots = "." * max(1, 10 - len(label))
        body.append(
            f"<g>"
            f'<text x="{PAD}" y="{y:.1f}" class="label">{escape(label)}{dots}:</text>'
            f'<text x="{PAD + LABEL_W}" y="{y:.1f}" fill="{color}">{escape(value)}</text>'
            f"{anim(step * ROW_DELAY)}</g>"
        )
        y += LINE_H
        step += 1

    # Faixa de cores do neofetch, logo abaixo do conteudo.
    y += 10
    for i, color in enumerate(PALETTE):
        body.append(
            f'<rect x="{PAD + i * 22}" y="{y - 11:.1f}" width="16" height="14" rx="3" '
            f'fill="{color}">{anim(step * ROW_DELAY + i * 0.03)}</rect>'
        )
    body.append(
        f'<g><text x="{W - PAD}" y="{y:.1f}" class="dim" text-anchor="end">'
        f"open to collaboration</text>{anim(step * ROW_DELAY + 0.2)}</g>"
    )

    height = round(y + PAD)

    head: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img" '
        f'aria-label="Cartao de perfil de Marcus Boni no estilo neofetch">',
        "<style>",
        f"  text{{{mono};font-size:{FONT}px}}",
        f"  .label{{fill:{LABEL}}}",
        f"  .dim{{fill:{LABEL};font-size:{FONT - 1}px}}",
        "</style>",
        # Moldura do terminal.
        f'<rect width="{W}" height="{height}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M0 10a10 10 0 0 1 10-10h{W - 20}a10 10 0 0 1 10 10v{BAR_H - 10}H0z" fill="{BAR}"/>',
        f'<line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{BORDER}"/>',
    ]
    for i, color in enumerate(DOTS):
        head.append(f'<circle cx="{20 + i * 18}" cy="{BAR_H / 2}" r="5.5" fill="{color}"/>')
    head.append(
        f'<text x="{W / 2}" y="{BAR_H / 2 + 4.5}" class="dim" text-anchor="middle">'
        f"{escape(HOST)} - neofetch</text>"
    )

    return "\n".join(head + body + ["</svg>"])


def main() -> None:
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/info-card.svg")
    static = os.environ.get("STATIC") == "1"
    dst.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg(static)
    dst.write_text(svg, encoding="utf-8")

    height = svg.split('height="', 1)[1].split('"', 1)[0]
    print(f"-> {dst}  {W}x{height}, {dst.stat().st_size // 1024} KB"
          f"{'  (estatico)' if static else ''}")


if __name__ == "__main__":
    main()
