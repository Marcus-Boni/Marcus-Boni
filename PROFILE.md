# Como este perfil é montado

Todo o visual do README é SVG gerado neste repositório. Nenhum serviço de
terceiros, nenhum token, nenhum JavaScript.

## Por que SVG próprio

O GitHub remove `<script>` e quase todo CSS inline do README, mas **renderiza
SVG carregado via `<img>` e executa as animações SMIL/CSS de dentro dele**. Essa
é a única brecha de movimento disponível — e ela é suficiente.

A alternativa comum são serviços hospedados de estatística. Eles trazem limite
de requisições, dependem do uptime de outra pessoa e, quando caem, o seu perfil
fica com imagem quebrada. Gerando o SVG aqui, a arte fica versionada no repo,
carrega instantâneo e o único ponto móvel é uma página pública do próprio GitHub.

## Os quatro painéis

| Arquivo | Gerado por | Atualiza |
| :--- | :--- | :--- |
| `assets/ascii-portrait.svg` | `make_ascii_svg.py` | manual, ao trocar a foto |
| `assets/info-card.svg` | `make_info_card.py` | manual, ao mudar os dados |
| `assets/contrib-heatmap.svg` | `render_heatmap_svg.py` | diário, via Actions |
| `assets/language-bar.svg` | `render_stack_svg.py` | diário, via Actions |

## Regenerar o retrato

Só é necessário quando você troca a foto.

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r scripts/requirements-local.txt

python scripts/prep_photo.py source-photo.jpg   # recorta o fundo e ajusta contraste
python scripts/make_ascii_svg.py                # gera o SVG animado
```

O `prep_photo.py` remove o fundo com `rembg`, aplica CLAHE (contraste local, para
o rosto não achatar), normaliza e **compõe sobre branco puro**. Isso não é
estético: na rampa de densidade o branco vira espaço, então o fundo simplesmente
desaparece do ASCII.

Funciona melhor com foto frontal, bem iluminada e com o rosto ocupando boa parte
do quadro. Retrato de perfil ou contraluz vira borrão.

## Atualizar o cartão neofetch

Edite `HOST` e `ROWS` no topo de `scripts/make_info_card.py` e rode:

```bash
python scripts/make_info_card.py
```

O cartão é estático de propósito: ali são fatos sobre você, não métricas. O que
é métrica está nos outros dois painéis, e esses se atualizam sozinhos.

## Prévia local

```bash
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
python scripts/render_stack_svg.py
```

Para congelar as animações e conferir o quadro final:

```bash
STATIC=1 python scripts/make_ascii_svg.py
STATIC=1 python scripts/make_info_card.py
```

## Uma decisão que vale explicar

As animações **não usam `begin` atrasado**. O atraso de cada linha vive dentro do
`keyTimes`, e toda animação começa em `0s`, com o estado base do elemento sendo o
**visível**.

O motivo é o modo de falhar. Com `opacity="0"` e um `begin` atrasado, qualquer
cliente que ignore SMIL — proxy de imagem, leitor RSS, impressão, aba em segundo
plano — mostra um retângulo vazio. Do jeito atual, esse mesmo cliente mostra o
painel completo e parado. Um README que às vezes aparece em branco é pior do que
um README sem animação.

## Automação

`.github/workflows/update-profile-art.yml` roda todo dia às 06:17 UTC, refaz os
dois painéis dinâmicos e só commita se o conteúdo mudou. Dá para disparar na
mão pela aba **Actions** → *Update profile art* → *Run workflow*.

O `[skip ci]` na mensagem de commit impede que o commit do bot dispare o próprio
workflow de novo.

---

Ideia original do [Avi Vashishta](https://www.avivashishta.com/blog/build-animated-github-profile-readme.html);
implementação e scripts refeitos aqui.
