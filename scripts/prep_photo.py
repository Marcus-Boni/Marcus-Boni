"""Prepara uma foto para virar retrato ASCII.

Pipeline: recorte de fundo (rembg) -> composicao sobre branco -> escala de
cinza -> CLAHE (contraste local) -> normalizacao.

O fundo vira branco puro de proposito: na rampa de densidade usada pelo
make_ascii_svg.py o branco mapeia para espaco, entao o fundo simplesmente
desaparece e sobra so o sujeito.

Uso:
    python scripts/prep_photo.py                     # usa o avatar do GitHub
    python scripts/prep_photo.py foto.jpg [saida.png]

So precisa rodar de novo quando voce trocar a foto.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

# ---------------------------------------------------------------- parametros

USER = "Marcus-Boni"  # de quem baixar o avatar quando nenhuma foto e passada

CLAHE_TILES = 8  # grade de 8x8 blocos para equalizacao local
CLAHE_CLIP = 3.0  # limite de contraste (evita estourar ruido)
GAMMA = 1.05  # >1 escurece levemente os meios-tons

# A roupa escura vira um bloco solido de caracteres densos que rouba a atencao
# do rosto. Cortar o terco inferior do busto resolve.
KEEP_HEIGHT = 0.80  # fracao da altura do sujeito preservada, de cima p/ baixo
MARGIN = 0.04  # respiro ao redor do recorte, em fracao da largura


def remove_background(img: Image.Image) -> Image.Image:
    """Recorta o sujeito e compoe sobre branco. Sem rembg, devolve a original."""
    try:
        from rembg import remove
    except ImportError:
        print("  ! rembg indisponivel - seguindo sem recorte de fundo")
        return img.convert("RGB")

    cut = remove(img)  # RGBA com alpha do sujeito
    white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    return Image.alpha_composite(white, cut).convert("RGB")


def clahe(gray: np.ndarray, tiles: int = CLAHE_TILES, clip: float = CLAHE_CLIP) -> np.ndarray:
    """CLAHE em numpy puro: equaliza por bloco e interpola bilinearmente.

    Equalizar a imagem inteira de uma vez achata o rosto; por bloco recupera
    detalhe local (olhos, boca, mecha de cabelo) sem clarear o fundo.
    """
    h, w = gray.shape
    ty, tx = h / tiles, w / tiles

    # Uma LUT de 256 entradas por bloco.
    luts = np.empty((tiles, tiles, 256), dtype=np.float64)
    for by in range(tiles):
        for bx in range(tiles):
            block = gray[
                int(by * ty) : int((by + 1) * ty),
                int(bx * tx) : int((bx + 1) * tx),
            ]
            hist = np.bincount(block.ravel(), minlength=256).astype(np.float64)

            # Clipping: corta picos e redistribui a massa uniformemente.
            limit = max(1.0, clip * block.size / 256.0)
            excess = np.maximum(hist - limit, 0).sum()
            hist = np.minimum(hist, limit) + excess / 256.0

            cdf = np.cumsum(hist)
            luts[by, bx] = 255.0 * (cdf - cdf[0]) / max(cdf[-1] - cdf[0], 1e-6)

    # Coordenada de cada pixel no espaco de centros de bloco.
    fy = np.clip(np.arange(h) / ty - 0.5, 0, tiles - 1)
    fx = np.clip(np.arange(w) / tx - 0.5, 0, tiles - 1)
    y0, x0 = np.floor(fy).astype(int), np.floor(fx).astype(int)
    y1 = np.minimum(y0 + 1, tiles - 1)
    x1 = np.minimum(x0 + 1, tiles - 1)
    wy = (fy - y0)[:, None]
    wx = (fx - x0)[None, :]

    def apply(by_idx, bx_idx):
        return luts[by_idx[:, None], bx_idx[None, :], gray]

    out = (
        apply(y0, x0) * (1 - wy) * (1 - wx)
        + apply(y0, x1) * (1 - wy) * wx
        + apply(y1, x0) * wy * (1 - wx)
        + apply(y1, x1) * wy * wx
    )
    return np.clip(out, 0, 255).astype(np.uint8)


def crop_to_subject(gray: np.ndarray) -> np.ndarray:
    """Enquadra o sujeito e corta o busto, deixando o rosto dominar."""
    ink = gray < 245  # tudo que nao e fundo branco
    if not ink.any():
        return gray

    rows = np.flatnonzero(ink.any(axis=1))
    cols = np.flatnonzero(ink.any(axis=0))
    top, bottom = rows[0], rows[-1]
    left, right = cols[0], cols[-1]

    bottom = top + int((bottom - top) * KEEP_HEIGHT)
    pad = int((right - left) * MARGIN)

    h, w = gray.shape
    out = gray[
        max(top - pad, 0) : min(bottom + pad, h),
        max(left - pad, 0) : min(right + pad, w),
    ]
    print(f"-> enquadrado para {out.shape[1]}x{out.shape[0]} px")
    return out


def resolve_source(argv: list[str]) -> Path:
    """Caminho da foto. Sem argumento e sem arquivo local, baixa o avatar.

    Assim o repo nao precisa versionar binario nenhum: a foto de origem e
    sempre recuperavel a partir do proprio GitHub.
    """
    if len(argv) > 1:
        return Path(argv[1])

    local = Path("source-photo.jpg")
    if local.exists():
        return local

    url = f"https://github.com/{USER}.png?size=800"
    print(f"-> baixando avatar de {url}")
    req = urllib.request.Request(url, headers={"User-Agent": f"profile-art/1.0 ({USER})"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        local.write_bytes(resp.read())
    return local


def main() -> None:
    src = resolve_source(sys.argv)
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png")

    print(f"-> lendo {src}")
    img = Image.open(src).convert("RGBA")

    print("-> removendo fundo")
    img = remove_background(img)

    print("-> escala de cinza + CLAHE")
    gray = np.asarray(ImageOps.grayscale(img), dtype=np.uint8)
    gray = clahe(gray)

    # Normaliza a faixa util e aplica gama.
    lo, hi = np.percentile(gray, [1, 99])
    norm = np.clip((gray.astype(np.float64) - lo) / max(hi - lo, 1e-6), 0, 1)
    gray = (np.power(norm, GAMMA) * 255).astype(np.uint8)

    # O recorte deixa o fundo branco; garante que ele volte a ser branco puro
    # depois da normalizacao, senao vira ruido de pontinhos no ASCII.
    gray[gray > 244] = 255

    gray = crop_to_subject(gray)

    Image.fromarray(gray).save(dst)
    print(f"-> gravado {dst} ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
