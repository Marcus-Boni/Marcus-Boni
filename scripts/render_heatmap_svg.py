"""Desenha o mapa de contribuicoes animado (assets/contrib-heatmap.svg).

Le data/contributions.json e monta o calendario de 53 semanas x 7 dias. Os
quadrados aparecem em onda diagonal, do canto superior esquerdo para o
inferior direito, e congelam. Roda uma vez.

Uso:
    python scripts/render_heatmap_svg.py [saida.svg]
    STATIC=1 python scripts/render_heatmap_svg.py   # quadro congelado
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

SRC = Path("data/contributions.json")

# ----------------------------------------------------------------- aparencia

CELL = 11.0
GAP = 3.0
PITCH = CELL + GAP
PAD = 22.0
LEFT = 30.0  # coluna dos rotulos de dia da semana
TOP = 40.0  # faixa dos rotulos de mes
FOOTER = 54.0

BG = "#0d1117"
BORDER = "#30363d"
DIM = "#8b949e"
BRIGHT = "#e6edf3"

# nenhuma -> mais intensa. O nivel 5 e um verde neon acima da escala do GitHub,
# reservado para os dias realmente fora da curva.
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

WAVE = 0.012  # atraso por passo diagonal (s)
CELL_DUR = 0.34
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load() -> dict:
    if not SRC.exists():
        raise SystemExit(f"! {SRC} nao existe - rode scripts/fetch_contributions.py antes")
    return json.loads(SRC.read_text(encoding="utf-8"))


def grid(days: list[dict]) -> tuple[list[list[dict | None]], list[tuple[int, int]]]:
    """Distribui os dias em colunas de semana. Devolve a grade e os rotulos de mes.

    A coluna 0 e a semana do dia mais antigo; a linha e o dia da semana
    (0 = domingo), igual ao calendario do GitHub.
    """
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # weekday(): 0=segunda -> queremos 0=domingo

    weeks: list[list[dict | None]] = [[None] * 7]
    row = offset
    for day in days:
        if row > 6:
            weeks.append([None] * 7)
            row = 0
        weeks[-1][row] = day
        row += 1

    # Um rotulo por mes, na primeira semana em que ele aparece.
    labels: list[tuple[int, int]] = []
    seen: set[str] = set()
    for w, week in enumerate(weeks):
        for day in week:
            if not day:
                continue
            key = day["date"][:7]
            if key not in seen:
                seen.add(key)
                labels.append((w, int(day["date"][5:7])))
            break
    return weeks, labels


def build_svg(data: dict, static: bool) -> str:
    days = data["raw_days"]
    weeks, month_labels = grid(days)

    width = LEFT + len(weeks) * PITCH + PAD * 2
    height = TOP + 7 * PITCH + FOOTER + PAD

    mono = ("font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"
            "'DejaVu Sans Mono',monospace")

    out: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
        f'aria-label="{data["total"]} contribuicoes de {data["user"]} nos ultimos 12 meses">',
        "<style>",
        f"  text{{{mono};font-size:10px;fill:{DIM}}}",
        f"  .h{{font-size:12px;fill:{BRIGHT}}}",
        f"  .n{{font-size:13px;fill:{BRIGHT};font-weight:bold}}",
        "</style>",
        f'<rect width="{width:.0f}" height="{height:.0f}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
    ]

    # Cabecalho.
    total = f"{data['total']:,}".replace(",", ".")
    out.append(f'<text x="{PAD}" y="{PAD + 4}" class="h">{total} contributions '
               f"in the last year</text>")
    out.append(f'<text x="{width - PAD:.0f}" y="{PAD + 4}" text-anchor="end">'
               f'updated {data["generated_at"]}</text>')

    x0 = PAD + LEFT
    y0 = TOP

    for w, month in month_labels:
        out.append(f'<text x="{x0 + w * PITCH:.1f}" y="{y0 - 6:.0f}">{MONTHS[month - 1]}</text>')

    for i, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="{PAD}" y="{y0 + i * PITCH + CELL - 2:.1f}">{label}</text>')

    # Grade. A onda diagonal faz o calendario "abrir" em vez de piscar inteiro.
    # O atraso vive no keyTimes, nunca no `begin`: assim o estado base de cada
    # quadrado e o visivel, e um cliente sem SMIL mostra o calendario completo
    # e parado em vez de um retangulo vazio.
    total = (len(weeks) + 7) * WAVE + CELL_DUR
    for w, week in enumerate(weeks):
        for d, day in enumerate(week):
            if day is None:
                continue
            level = day["level"]
            if level >= 4 and day["count"] >= 15:
                level = 5  # destaca os dias excepcionais
            x = x0 + w * PITCH
            y = y0 + d * PITCH
            rect = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" '
                    f'fill="{LEVELS[level]}"')
            if static:
                out.append(rect + "/>")
            else:
                begin = (w + d) * WAVE
                out.append(
                    rect + ">"
                    f'<animate attributeName="opacity" values="0;0;1;1" '
                    f'keyTimes="0;{begin / total:.4f};{(begin + CELL_DUR) / total:.4f};1" '
                    f'dur="{total:.2f}s" begin="0s" fill="freeze"/></rect>'
                )

    # Legenda Less -> More.
    ly = y0 + 7 * PITCH + 20
    lx = width - PAD - len(LEVELS) * (CELL + 3) - 62
    out.append(f'<text x="{lx:.1f}" y="{ly + CELL - 2:.1f}">Less</text>')
    for i, color in enumerate(LEVELS):
        out.append(f'<rect x="{lx + 28 + i * (CELL + 3):.1f}" y="{ly:.1f}" '
                   f'width="{CELL}" height="{CELL}" rx="2.5" fill="{color}"/>')
    out.append(f'<text x="{lx + 34 + len(LEVELS) * (CELL + 3):.1f}" y="{ly + CELL - 2:.1f}">More</text>')

    # Rodape com os numeros que valem a pena contar.
    stats = [
        (f"{data['current_streak']}d", "current streak"),
        (f"{data['longest_streak']}d", "longest streak"),
        (str(data["active_days"]), "active days"),
        (str(data["best_day"]["count"]), "best day"),
    ]
    sx = PAD
    for value, label in stats:
        out.append(f'<text x="{sx:.0f}" y="{ly + CELL - 2:.1f}" class="n">{value}</text>')
        out.append(f'<text x="{sx + len(value) * 8 + 6:.0f}" y="{ly + CELL - 2:.1f}">{label}</text>')
        sx += len(value) * 8 + len(label) * 6 + 26

    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    dst = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/contrib-heatmap.svg")
    static = os.environ.get("STATIC") == "1"
    data = load()
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(build_svg(data, static), encoding="utf-8")
    print(f"-> {dst}  {data['total']} contribuicoes, {dst.stat().st_size // 1024} KB"
          f"{'  (estatico)' if static else ''}")


if __name__ == "__main__":
    main()
