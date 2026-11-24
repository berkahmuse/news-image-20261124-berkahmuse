#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news image (1024x1024 PNG).

Deterministic: fixed fonts, fixed geometry, no randomness, no network.
Run:  python3 draw.py            -> writes entry.png next to this file.

Stories verified against reports read on Tuesday 24 November 2026:
- Ulleung island alert, South Korea (Reuters/AP, 07:52 KST)
- Singapore Q3 GDP +6.1%, 2026 forecast raised to ~6% (Reuters, 24 Nov)
- FIDE World Championship Game 1, Geneva (Chess.com/FIDE)
- Thailand-China-Myanmar talks on toxic rivers, 24 Nov (The Diplomat/Reuters)
  (150 km Kok pollution-control zone verified: Bloomberg/BusinessMirror, 22 Nov)

"""
import hashlib
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

PAPER = (247, 243, 233)
INK = (24, 24, 24)
NAVY = (16, 42, 67)
TEAL = (13, 92, 92)
RED = (178, 34, 34)
AMBER = (198, 140, 40)
CARD = (255, 253, 248)
BORDER = (210, 202, 182)
MUTED = (96, 90, 80)
SKY = (214, 230, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box):
    draw.rounded_rectangle(box, radius=12, fill=CARD, outline=BORDER, width=2)


def icon_radar(draw, cx, cy, r=105):
    # dark radar screen
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 32, 48))
    for rr in (78, 52, 26):
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(46, 120, 110), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(46, 120, 110), width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=(46, 120, 110), width=2)
    # sweep wedge
    wedge = [(cx, cy)]
    for a in range(-45, -4, 5):
        wedge.append((cx + int(r * 0.96 * math.cos(math.radians(a))),
                      cy + int(r * 0.96 * math.sin(math.radians(a)))))
    draw.polygon(wedge, fill=(28, 90, 84))
    # blip: unidentified aircraft
    bx, by = cx + 58, cy - 42
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED)
    draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 200))
    # small jet silhouette
    jx, jy = cx - 62, cy + 48
    draw.polygon([(jx - 34, jy + 6), (jx + 6, jy - 6), (jx + 34, jy + 2),
                  (jx + 6, jy + 8)], fill=(235, 238, 240))
    draw.polygon([(jx - 6, jy - 16), (jx + 4, jy - 2), (jx - 12, jy + 2)],
                 fill=(235, 238, 240))
    # island below the scope
    draw.ellipse([cx - 70, cy + r - 6, cx + 70, cy + r + 16], fill=TEAL)


def icon_bars(draw, x, y, s=96):
    # ascending bar chart: Singapore GDP growth, with a trend arrow
    base = y + s - 8
    heights = (34, 52, 68, 88)
    for i, h in enumerate(heights):
        bx = x + 6 + i * 24
        draw.rectangle([bx, base - h, bx + 16, base],
                       fill=TEAL if i < 3 else NAVY)
    draw.line([(x + 4, base - 28), (x + 44, base - 60), (x + 88, base - 84)],
              fill=RED, width=5, joint="curve")
    draw.polygon([(x + 88, base - 84), (x + 72, base - 86), (x + 86, base - 70)],
                 fill=RED)


def icon_chess(draw, x, y, s=96):
    cell = s // 4
    for r in range(4):
        for c in range(4):
            fill = NAVY if (r + c) % 2 == 0 else (240, 236, 224)
            draw.rectangle([x + c * cell, y + r * cell,
                            x + (c + 1) * cell, y + (r + 1) * cell], fill=fill)
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3)
    # white pawn on light square, black pawn on dark square
    draw.ellipse([x + 2 * cell + 5, y + 1 * cell + 4, x + 3 * cell - 5,
                  y + 2 * cell - 4], fill=(255, 255, 255), outline=INK, width=2)
    draw.ellipse([x + 1 * cell + 5, y + 2 * cell + 4, x + 2 * cell - 5,
                  y + 3 * cell - 4], fill=INK)


def icon_river(draw, x, y, w=96):
    # three flowing waves
    for i, yy in enumerate((y + 14, y + 42, y + 70)):
        pts = []
        for px in range(x, x + w + 1, 8):
            pts.append((px, yy + int(7 * math.sin((px - x) / 18.0 + i * 1.4))))
        draw.line(pts, fill=TEAL, width=7, joint="curve")
    # droplet of arsenic warning
    draw.ellipse([x + w - 18, y - 2, x + w + 2, y + 18], fill=RED)


def story_half(draw, box, kicker, kcolor, headline, summary, icon_fn):
    x0, y0, x1, y1 = box
    card(draw, box)
    icon_fn(draw, x0 + 18, y0 + 16)
    tx = x0 + 132
    tw = x1 - tx - 16
    draw.text((tx, y0 + 14), kicker, font=SANS_B(16), fill=kcolor)
    lines = wrap(draw, headline, SANS_B(26), tw)
    y = block(draw, tx, y0 + 40, lines[:2], SANS_B(26), INK, 31)
    slines = wrap(draw, summary, SANS(17), tw)
    block(draw, tx, y + 6, slines[:4], SANS(17), MUTED, 22)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((28, 18), "TUESDAY  •  THE WORLD IN ONE DAY", font=SANS_B(19),
           fill=AMBER)
    d.text((28, 46), "24 NOVEMBER 2026", font=SERIF_B(64),
           fill=(255, 255, 255))
    d.text((W - 28, 52), "ONE DAY\nONE IMAGE", font=SANS_B(20),
           fill=(200, 215, 225), anchor="ra", align="right")
    d.line([28, 132, W - 28, 132], fill=AMBER, width=3)

    # ---- breaking strip ----
    d.rectangle([0, 148, W, 192], fill=RED)
    d.text((28, 158), "●  BREAKING 07:52 KST — ULLEUNG ISLAND, SOUTH KOREA",
           font=SANS_B(24), fill=(255, 255, 255))

    # ---- lead story: Ulleung alert ----
    card(d, [28, 206, 996, 470])
    icon_radar(d, 150, 338)
    d.text((292, 224), "SOUTH KOREA  •  EAST SEA", font=SANS_B(18), fill=RED)
    lead = wrap(d, "ISLANDERS TOLD TO SHELTER AS MYSTERY JET NEARS",
                SANS_B(38), 996 - 292 - 20)
    y = block(d, 292, 250, lead, SANS_B(38), INK, 44)
    body = wrap(d, "Seoul sounded a civil-defence alert at 07:52 for "
                "Ulleung island after an unidentified aircraft approached; "
                "the alert was lifted minutes later. Russian jets had "
                "entered the air-defence zone — officials later said the "
                "plane may have been North Korean.", SANS(21),
                996 - 292 - 20)
    block(d, 292, y + 10, body, SANS(21), MUTED, 27)

    # ---- two half cards ----
    story_half(d, [28, 484, 500, 700], "ECONOMY  •  SINGAPORE", NAVY,
               "SINGAPORE GDP JUMPS 6.1%",
               "Q3 GDP beat forecasts at 6.1% on AI-driven exports; "
               "the government raised its 2026 growth forecast to "
               "about 6%.",
               icon_bars)
    story_half(d, [524, 484, 996, 700], "SPORT  •  CHESS, GENEVA", TEAL,
               "GUKESH v SINDAROV: GAME 1 TODAY",
               "The title match opens at 15:00 CET in Geneva. "
               "Sindarov has White in Game 1 of 14; the $2.5m match is "
               "the youngest ever — both are 20.",
               icon_chess)

    # ---- bottom wide panel: toxic rivers ----
    card(d, [28, 714, 996, 884])
    icon_river(d, 48, 762)
    d.text((172, 730), "ASIA  •  ENVIRONMENT", font=SANS_B(17), fill=TEAL)
    d.text((172, 754), "TALKS TODAY ON TOXIC RIVERS", font=SANS_B(28), fill=INK)
    river = wrap(d, "Thailand, China and Myanmar meet over arsenic in the "
                 "Kok and Sai rivers, blamed on unregulated rare-earth "
                 "mining in Myanmar. A 150 km stretch of the Kok is set to "
                 "become a pollution-control zone.", SANS(20),
                 996 - 172 - 20)
    block(d, 172, 792, river, SANS(20), MUTED, 26)

    # ---- footer ----
    d.line([28, 912, 996, 912], fill=BORDER, width=2)
    d.text((W // 2, 926), "Sources: Reuters, AP, Chess.com, FIDE, The Diplomat, MTI",
           font=SANS(16), fill=MUTED, anchor="ma")
    d.text((W // 2, 950), "From reports of Tuesday 24 November 2026  •  make.fun news-image-20261124",
           font=SANS(16), fill=MUTED, anchor="ma")
    d.text((W // 2, 978), "ONE DAY'S NEWS, ONE IMAGE", font=SANS_B(15),
           fill=NAVY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    data = OUT.read_bytes()
    print(f"wrote {OUT} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
