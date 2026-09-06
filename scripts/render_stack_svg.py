"""Desenha a barra de linguagens (assets/language-bar.svg).

Le a lista publica de repositorios (uma unica chamada, sem token) e monta uma
barra empilhada com a linguagem principal de cada repo. As fatias crescem da
esquerda para a direita e congelam.

Isso substitui a parede de badges: badges dizem o que voce ja tocou uma vez,
essa barra mostra onde o codigo realmente esta.

Uso:
    python scripts/render_stack_svg.py [usuario]
"""

from __future__ import annotations

import collections
import json
import os
import sys
import urllib.request
from pathlib import Path

USER = sys.argv[1] if len(sys.argv) > 1 else "Marcus-Boni"
API = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"
OUT = Path("assets/language-bar.svg")
TOP_N = 7

W, H = 840, 132
PAD = 22
BAR_Y, BAR_H = 62, 20

BG = "#0d1117"
BORDER = "#30363d"
DIM = "#8b949e"
BRIGHT = "#e6edf3"
OTHER = "#6e7681"

# Cores oficiais do linguist, para o grafico bater com o que o GitHub mostra.
COLORS = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5",
    "HTML": "#e34c26", "CSS": "#663399", "Java": "#b07219", "C#": "#178600",
    "C++": "#f34b7d", "C": "#555555", "Rust": "#dea584", "Go": "#00ADD8",
    "Dart": "#00B4AB", "Shell": "#89e051", "Ruby": "#701516", "PHP": "#4F5D95",
    "Jupyter Notebook": "#DA5B0B", "Vue": "#41b883", "Svelte": "#ff3e00",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "SCSS": "#c6538c",
}

TOTAL_DUR = 1.6


def fetch_repos() -> list[dict]:
    req = urllib.request.Request(API, headers={"User-Agent": f"profile-art/1.0 ({USER})"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def build_svg(counts: list[tuple[str, int]], total: int, repos: int) -> str:
    mono = ("font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"
            "'DejaVu Sans Mono',monospace")

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Distribuicao de linguagens em {repos} repositorios publicos">',
        "<style>",
        f"  text{{{mono};font-size:11px;fill:{DIM}}}",
        f"  .h{{font-size:12px;fill:{BRIGHT}}}",
        "</style>",
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="{PAD}" y="{PAD + 12}" class="h">language distribution</text>',
        f'<text x="{W - PAD}" y="{PAD + 12}" text-anchor="end">'
        f"{repos} public repos - by primary language</text>",
    ]

    # Barra empilhada. Cada fatia cresce no seu trecho da linha do tempo, entao
    # a barra parece se preencher da esquerda para a direita.
    x = PAD
    usable = W - PAD * 2
    acc = 0.0
    for name, count in counts:
        frac = count / total
        w = usable * frac
        k1, k2 = acc, min(acc + frac, 1.0)
        out.append(
            f'<rect x="{x:.1f}" y="{BAR_Y}" width="{w:.1f}" height="{BAR_H}" '
            f'fill="{COLORS.get(name, OTHER)}">'
            f'<animate attributeName="width" values="0;0;{w:.1f};{w:.1f}" '
            f'keyTimes="0;{k1:.4f};{k2:.4f};1" dur="{TOTAL_DUR}s" begin="0s" fill="freeze"/>'
            f"</rect>"
        )
        x += w
        acc += frac

    # Legenda: bolinha + nome + percentual.
    lx, ly = PAD, BAR_Y + BAR_H + 26
    for name, count in counts:
        pct = 100 * count / total
        out.append(f'<circle cx="{lx + 4:.0f}" cy="{ly - 4:.0f}" r="4.5" '
                   f'fill="{COLORS.get(name, OTHER)}"/>')
        label = f"{name} {pct:.1f}%"
        out.append(f'<text x="{lx + 14:.0f}" y="{ly:.0f}">{label}</text>')
        lx += 14 + len(label) * 6.6 + 16

    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    print(f"-> GET {API}")
    repos = [r for r in fetch_repos() if not r.get("fork")]

    counts = collections.Counter(r["language"] for r in repos if r.get("language"))
    top = counts.most_common(TOP_N)
    rest = sum(counts.values()) - sum(c for _, c in top)
    if rest:
        top.append(("Other", rest))

    total = sum(c for _, c in top)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_svg(top, total, len(repos)), encoding="utf-8")

    print("-> " + ", ".join(f"{n} {100 * c / total:.1f}%" for n, c in top))
    print(f"-> gravado {OUT}")


if __name__ == "__main__":
    main()
