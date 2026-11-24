# TESTLOG — make.fun news-image-20261124

Entry: **"The World Today"** — newspaper front page summing up Tue 24 Nov 2026.
Bounty: $100, 50 places paid. Deadline: Thu 2026-11-26 00:00 UTC / 07:00 WIB.
Workdir: `~/workspace/makefun-news-image-20261124/`

## Leaderboard (ORDER RULE, checked 24 Nov ~09:44 WIB)

`GET https://make.fun/api/competitions/news-image-20261124/leaderboard`:
competition open, phase dev, **blind rounds, metrics_withheld: true,
entries: []** — no live top-1 visible. Built to the published
requirements and the winner-study density format (40 stories, 8 regions,
timeline strip, world map with pins, per-story sources, "left out" box),
with a layout DIFFERENT from yesterday's accepted 20261123 entry:
map + numbers box on one band, 12 pictured stories in two rows, 4x2
region grid.

## News verified (Tue 24 Nov 2026, checked ~09:50–10:00 WIB)

8 search passes (news vertical): world, US, Europe, Middle East/APAC,
Indonesia/SE Asia, Africa/LatAm, COP31/markets, sports/science/tech.
All 40 main stories are from reporting dated 24 Nov 2026; older
developments (COP31 22 Nov, Fiona 19 Nov, trilateral 20 Nov, Dyson
Award 4 Nov) are in the "Left out as older news" box with dates.

## FLUX images (NVIDIA FLUX.1-schnell, via custom.nvidia-image helper)

- First batch: 1st call failed with `RemoteDisconnected` after ~270s
  (transient). Retried the single image — saved in ~4s. Remaining 11
  generated in batches of 3–4, all ~4–15s each.
- Two generations came back pure black (1024x1024, all channels 0,
  6,428 bytes): Jakarta parliament (twice, different prompts) and
  cricket. Regenerated with new prompts; cricket fixed on 1st retry,
  Jakarta fixed on 2nd retry with a Monas-obelisk subject.
- Final: 12/12 images verified 1024x1024, non-black (max channel 142–255).

## Test 1 (first working version)

- `python3 main.py` (MAKEFUN_OUTPUT_DIR=workdir/output), run twice.
- Output: 371,788 bytes, 1024x1024 PNG.
- sha256 `959e125ccdd66ae621d00156ebe4b0b2a6b4b030e7ed4d01ebe7c096a5baaeff`
  identical on both runs — deterministic.
- Visual check: region-grid stories overflowed their blocks into the
  footer; map labels LONDON/BRUSSELS/KYIV collided; timeline 2nd lines
  clipped by the rule; "SPORT, SCIENCE & CULTURE" header collided
  with the "5 STORIES" tag.

## Revision (real edit after the test)

- Fonts: headline 11→10px, detail 10→9px; detail clamped to 1 line.
- Region renamed "SPORT, SCIENCE & CULTURE" → "SPORT & CULTURE".
- Map pins got per-label dx/dy offsets (London left, Brussels below,
  Kyiv right) so the Europe cluster no longer collides.
- Timeline geometry shifted (bottom rule 124→128, headline y 107);
  map band 132–262; pictured strip rows at 288/350; grid at y 416.
- NIGHT timeline headline shortened to "CAS rules on Senegal AFCON appeal".

## Test 2 (after revision)

- `python3 main.py`, run twice.
- Output: 344,003 bytes, 1024x1024 PNG, under the 1 MiB limit.
- sha256 `1029322aa791260616e6d0417c9dfbf7981d5ac67096b084e7d9f2c3938dd2e5`
  identical on both runs — deterministic.
- Visual check: all 40 stories fit inside their blocks, footer clean,
  map labels readable, timeline fits, pictured strip renders 12 scenes.

## Badges (verified 24 Nov, all 200 image/svg+xml)

- https://make.fun/badge/news-image-20261124.svg
- https://make.fun/badge/news-image-20261124/tulankganteng/news-image-20261124/rank.svg
- https://make.fun/badge/news-image-20261124/tulankganteng/news-image-20261124/reward.svg

## Status

Ready for the parent to push to tulankganteng/news-image-20261124 and
submit. NOT submitted, NOT pushed by this agent.
