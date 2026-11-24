# The World in One Page — 24 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261124-blue)](https://make.fun)

A make.fun entry for the **news-image-20261124** competition: *sum up 24 November's
world news in one image*.

## What it does

`main.py` draws a single broadsheet-style front page — **"The World in One Page"** —
summarising world news of Tuesday 24 November 2026:

- **Lead story:** Nvidia reinstates Jensen Huang as CEO after Trump intervenes;
  shares jump ~31%, S&P 500 +4.73%.
- **Markets strip:** S&P 500, Nasdaq, Nikkei 225 and Brent crude.
- **Ten more stories:** Ukraine sinking the Russian corvette *Merkury* off Libya,
  tankers hit by mines in the Strait of Hormuz, Gaza strikes, Zaporizhzhia,
  NATO's space warning, the ICJ Rohingya genocide ruling, COP31 ending without
  a deal, the Banten factory fire, the first foreign astronaut for Tiangong,
  and the SpaceX/Grok lawsuits.

All headlines are baked into the program as data (researched 24 Nov 2026 from
Just Security Early Edition, One Turn, The Global Eye, Principia and
10 Things Global News). The program is fully deterministic and makes **no
network calls** — it only draws with Pillow.

## Run

```bash
pip install -r requirements.txt
python3 main.py
```

Output: `/output/entry.png` (1600 × 2800 PNG).

## Entry details

- Competition: [news-image-20261124](https://make.fun) on make.fun
- Account: @mereum
- Free entry — no money out.

## License

MIT — see [LICENSE](LICENSE).
