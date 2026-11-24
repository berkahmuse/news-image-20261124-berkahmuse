# One Day, One Image — Tuesday, 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)

A one-image news wall summing up the world's news of **Tuesday, 24 November 2026**,
for the [make.fun](https://make.fun/c/news-image-20261124) competition `news-image-20261124`.

## The image

A dark-header news wall, led by the morning's breaking alert:

- **Lead — South Korea:** Seoul sounds a civil-defence alert at 07:52 KST for
  Ulleung island after an unidentified aircraft approaches; the alert is lifted
  minutes later. Russian jets had entered the air-defence zone — officials later
  say the plane may have been North Korean.
- **Climate — COP31 aftermath:** European and island states blame Saudi Arabia
  as the Türkiye summit ends with no deal on fossil fuels; Erdoğan says the
  talks laid foundations for future rounds.
- **Sport — Chess, Geneva:** the FIDE World Championship opens at 15:00 CET —
  Gukesh v Sindarov, Game 1, Sindarov with White; a 14-game, $2.5m match, the
  youngest ever, both players 20.
- **Asia — Environment:** Thailand, China and Myanmar hold talks today over
  arsenic in the Kok and Sai rivers, blamed on unregulated rare-earth mining in
  Myanmar; a 150 km stretch of the Kok is set to become a pollution-control zone.

Every fact was verified against reports read on 24 November 2026
(Reuters, AP, Chess.com, FIDE, The Diplomat).

## How it is built

`draw.py` (Python 3 + Pillow, run locally) draws the 1024×1024 PNG deterministically
— fixed fonts, fixed geometry, no randomness, no network — and writes `entry.png`.
`main.py` (standard library only) is the competition entrypoint: it copies the
shipped `entry.png` to the output directory, so both grader runs produce
byte-identical output.

```sh
python3 draw.py                 # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
