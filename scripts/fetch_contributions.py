"""Baixa o calendario de contribuicoes e grava data/contributions.json.

Usa o endpoint HTML publico /users/<user>/contributions. Sem token, sem
GraphQL, sem servico de terceiros - o unico ponto de falha e uma pagina
publica do proprio GitHub.

Uso:
    python scripts/fetch_contributions.py [usuario]
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else "Marcus-Boni"
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path("data/contributions.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; profile-art/1.0; +https://github.com/{})".format(USER),
    "Accept": "text/html",
    "X-Requested-With": "XMLHttpRequest",
}


def parse_count(text: str) -> int:
    """'No contributions on ...' -> 0 | '12 contributions on ...' -> 12."""
    m = re.match(r"\s*(\d[\d,]*)\s+contribution", text)
    return int(m.group(1).replace(",", "")) if m else 0


def fetch_days() -> list[dict]:
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # A contagem exata mora no <tool-tip for="<id-da-celula>">, nao na celula.
    counts = {
        tip["for"]: parse_count(tip.get_text())
        for tip in soup.find_all("tool-tip")
        if tip.has_attr("for")
    }

    days: list[dict] = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        cid = cell.get("id", "")
        days.append(
            {
                "date": cell["data-date"],
                "level": int(cell.get("data-level", 0)),
                "count": counts.get(cid, 0),
            }
        )

    if not days:
        raise SystemExit("! nenhuma celula encontrada - o HTML do GitHub mudou?")

    days.sort(key=lambda d: d["date"])
    return days


def streaks(days: list[dict]) -> tuple[int, int]:
    """Sequencia atual e maior sequencia, em dias com >=1 contribuicao.

    O dia de hoje ainda pode receber commits, entao um hoje zerado nao quebra
    a sequencia atual - so o dia anterior quebra.
    """
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    today = date.today().isoformat()
    current = 0
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        elif d["date"] != today:
            break
    return current, longest


def main() -> None:
    print(f"-> GET {URL}")
    days = fetch_days()

    total = sum(d["count"] for d in days)
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"])

    monthly: dict[str, int] = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

    active = sum(1 for d in days if d["count"] > 0)

    payload = {
        "user": USER,
        "generated_at": date.today().isoformat(),
        "range": {"from": days[0]["date"], "to": days[-1]["date"]},
        "total": total,
        "active_days": active,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly_totals": monthly,
        "raw_days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1), encoding="utf-8")

    print(f"-> {len(days)} dias | {total} contribuicoes | ativo em {active}")
    print(f"-> sequencia atual {current}d, recorde {longest}d, "
          f"melhor dia {best['date']} ({best['count']})")
    print(f"-> gravado {OUT}")


if __name__ == "__main__":
    main()
