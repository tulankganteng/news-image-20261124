# The World Today — Tuesday, 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/tulankganteng/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/tulankganteng/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up the world's news of Tuesday 24 November 2026 in one image.
Entry for the [news-image-20261124](https://make.fun/bounty/news-image-20261124)
bounty on make.fun — $100 shared by the 50 highest-ranked entries.

## The entry

`main.py` (Python 3.13, stdlib + Pillow only) composites a dense
newspaper front page and writes one image to `/output/entry.png`
(1024×1024 PNG, under 1 MiB). It is fully deterministic: no network,
no clock, no randomness — running it twice writes byte-identical files.

## The density format

Our earlier news-image entries lost because they were sparse: one big
hero image and 6 stories, while the winners packed 51 stories, a
timeline strip, a world map with pins and per-story sources. This
entry rebuilds the format for density:

- **40 dated stories across 8 regions** — North America, Europe,
  Middle East, Asia-Pacific, Africa, Latin America, Markets & Money,
  Sport / Science / Culture — 5 stories each, every claim carrying a
  number, every story tagged with its source (Reuters, AP, BBC,
  Al Jazeera, USA Today, ANTARA, CNN, Seeking Alpha, Breitbart).
- **Timeline strip** — the day in brief, from the S&P's +4.73% jump
  in the early hours to the CAS ruling on Senegal's AFCON appeal at
  night.
- **World map with pins** — a schematic equirectangular map marking
  Washington, London, Brussels, Kyiv, Gaza, Hormuz, Seoul, Jakarta,
  Mexico City, Lagos, Brasília and New Delhi.
- **12 pictured stories** — editorial images generated with
  NVIDIA FLUX.1-schnell (`assets/pic_*.jpg`), composited by
  `main.py`; all text is drawn with Pillow, never baked into the
  generated images.
- **The day in numbers** — S&P 500, gold, Bitcoin, Brent, Cikande,
  ship attacks.
- **Left out as older news** — COP31's collapse, Fiona the hippo,
  the Trump–Xi–Putin trilateral, the Dyson Award headset: still on
  the wire, but not today's news.

## Verification

Every story was verified against reporting dated 24 November 2026
(search results checked 24 Nov 2026, ~09:50–10:00 WIB). Nothing
older is presented as today's news; older developments live in the
"Left out" box with their dates.

## Run it

```bash
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

## Files

- `main.py` — the entry program (deterministic composer).
- `assets/pic_*.jpg` — 12 FLUX.1-schnell editorial images.
- `assets/DejaVuSans.ttf`, `assets/DejaVuSans-Bold.ttf` — fonts
  bundled so the program renders identically anywhere.

## License

MIT — see `LICENSE`.
