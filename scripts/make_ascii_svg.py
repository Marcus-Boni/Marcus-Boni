"""Gera o retrato ASCII animado (assets/ascii-portrait.svg).

Cada linha e revelada da esquerda para a direita por um clip que abre, com um
cursor de bloco correndo na borda. As linhas entram escalonadas de cima para
baixo, como texto sendo impresso num terminal. Roda uma vez e congela.

O SVG e auto-contido: sem JS, sem CSS externo, sem fonte embutida. E o unico
tipo de animacao que o GitHub deixa passar dentro de <img>.

Uso:
    python scripts/make_ascii_svg.py [entrada.png] [saida.svg]
    STATIC=1 python scripts/make_ascii_svg.py     # quadro congelado p/ preview
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

# ---------------------------------------------------------------- parametros

COLS = 100  # colunas de caracteres
CHAR_ASPECT = 0.5  # largura/altura da celula do monoespacado
CELL_W, CELL_H = 6.0, 11.0  # geometria da celula no SVG
FONT_SIZE = 10.0
PAD = 14.0

# Rampa de densidade: claro (esparso) -> escuro (denso).
# O espaco na frente faz o fundo branco sumir.
RAMP = " .`:-=+*csS#%@"

INK = "#c9d1d9"  # cinza claro, monocromatico de proposito
CURSOR = "#39d353"  # verde GitHub no cursor
BG = "#0d1117"
BORDER = "#30363d"  # mesma moldura do cartao e do heatmap

ROW_DELAY = 0.035  # atraso entre linhas (s)
ROW_DUR = 0.5  # duracao da varredura de cada linha (s)


def staggered(attr: str, hidden: str, shown: str, delay: float, dur: float, total: float) -> str:
    """Animacao escalonada que comeca sempre em 0s, com o atraso dentro do keyTimes.

    O estado base do elemento e o VISIVEL. Se o cliente nao rodar SMIL - leitor
    de RSS, proxy de imagem, print - o conteudo aparece parado em vez de sumir.
    Um `begin` atrasado com base invisivel daria a falha oposta, e um README que
    as vezes aparece vazio nao serve.
    """
    k1 = delay / total
    k2 = (delay + dur) / total
    return (
        f'<animate attributeName="{attr}" values="{hidden};{hidden};{shown};{shown}" '
        f'keyTimes="0;{k1:.4f};{k2:.4f};1" dur="{total:.2f}s" begin="0s" fill="freeze"/>'
    )


def load_grid(path: Path) -> np.ndarray:
    """Reamostra a imagem para a grade de caracteres e devolve luminancia 0..1."""
    img = Image.open(path).convert("L")
    w, h = img.size
    rows = max(1, round(COLS * (h / w) * CHAR_ASPECT))
    small = img.resize((COLS, rows), Image.Resampling.LANCZOS)
    return np.asarray(small, dtype=np.float64) / 255.0


def to_chars(grid: np.ndarray) -> list[str]:
    """Mapeia brilho para caracteres. Claro -> espaco, escuro -> denso."""
    idx = np.clip(((1.0 - grid) * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
    return ["".join(RAMP[i] for i in row) for row in idx]


def build_svg(lines: list[str], static: bool) -> str:
    rows = len(lines)
    width = COLS * CELL_W + PAD * 2
    height = rows * CELL_H + PAD * 2
    total = ROW_DELAY * rows + ROW_DUR
    text_w = COLS * CELL_W

    out: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" '
        f'aria-label="Retrato em ASCII de Marcus Boni">',
        "<style>",
        # textLength trava a largura de cada linha, entao a grade continua
        # alinhada mesmo se a fonte monoespacada do visitante for outra.
        f"  text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace;"
        f"font-size:{FONT_SIZE}px;white-space:pre}}",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1:.0f}" height="{height - 1:.0f}" '
        f'rx="10" fill="{BG}" stroke="{BORDER}"/>',
    ]

    for i, line in enumerate(lines):
        y = PAD + (i + 1) * CELL_H - 2
        begin = i * ROW_DELAY
        cid = f"c{i}"

        if static:
            out.append(
                f'<text x="{PAD}" y="{y:.1f}" fill="{INK}" textLength="{text_w:.0f}" '
                f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(line)}</text>'
            )
            continue

        # Clip que abre da esquerda para a direita revelando a linha. A largura
        # base e a total: sem SMIL a linha ja nasce inteira.
        out.append(
            f'<clipPath id="{cid}"><rect x="{PAD}" y="{y - CELL_H:.1f}" '
            f'height="{CELL_H + 4:.0f}" width="{text_w:.0f}">'
            + staggered("width", "0", f"{text_w:.0f}", begin, ROW_DUR, total)
            + "</rect></clipPath>"
        )
        out.append(
            f'<g clip-path="url(#{cid})"><text x="{PAD}" y="{y:.1f}" fill="{INK}" '
            f'textLength="{text_w:.0f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{escape(line)}</text></g>'
        )
        # Cursor cavalgando a borda da varredura. E decorativo, entao aqui a
        # base invisivel e a queda correta: sem animacao, nenhum cursor solto.
        k1, k2 = begin / total, (begin + ROW_DUR) / total
        eps = 0.0015
        out.append(
            f'<rect y="{y - CELL_H + 2:.1f}" width="{CELL_W:.0f}" height="{CELL_H - 2:.0f}" '
            f'fill="{CURSOR}" opacity="0" x="{PAD}">'
            + staggered("x", f"{PAD}", f"{PAD + text_w:.0f}", begin, ROW_DUR, total)
            + f'<animate attributeName="opacity" values="0;0;0.9;0.9;0;0" '
            f'keyTimes="0;{k1:.4f};{k1 + eps:.4f};{k2 - eps:.4f};{k2:.4f};1" '
            f'dur="{total:.2f}s" begin="0s" fill="freeze"/></rect>'
        )

    if not static:
        out.append(f"<!-- animacao completa em {total:.1f}s, depois congela -->")
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "assets/ascii-portrait.svg")
    static = os.environ.get("STATIC") == "1"

    grid = load_grid(src)
    lines = to_chars(grid)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(build_svg(lines, static), encoding="utf-8")

    print(f"-> {dst}  {COLS}x{len(lines)} chars, {dst.stat().st_size // 1024} KB"
          f"{'  (estatico)' if static else ''}")


if __name__ == "__main__":
    main()
