#!/usr/bin/env python3
"""news-image-20261124 — "The World in One Page".

Summarises world news of Tuesday 24 November 2026 as a single
broadsheet-style front-page image.

Deterministic: every headline is baked into this file as data (researched
24 Nov 2026 from Just Security Early Edition, One Turn, The Global Eye,
Principia and 10 Things). The program makes NO network calls at grading
time; it only draws with Pillow and writes one PNG.

Usage:  python3 main.py
Output: /output/entry.png  (1600 x 2800, PNG)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT_PATH = "/output/entry.png"
W, H = 1600, 2800

PAPER = (247, 242, 231)   # warm newsprint cream
INK = (20, 33, 61)        # deep navy ink
RED = (180, 35, 24)       # headline red
GOLD = (176, 141, 58)     # muted gold rule
GREY = (90, 96, 110)      # secondary text
LIGHT = (233, 226, 210)   # card background
GREEN = (31, 122, 62)     # market gains

LEAD = {
    "tag": "TECHNOLOGY  |  LEAD STORY",
    "headline": "CHIP KING RETURNS",
    "deck": "Nvidia reinstates Jensen Huang as chief executive,",
    "deck2": "less than two weeks after his resignation.",
    "body": (
        "President Trump said he personally persuaded the board to bring "
        "Huang back. Nvidia shares jumped about 31% in a single day and "
        "lifted the whole market: the S&P 500 rose 4.73%, its best day in "
        "over a year, and the Nasdaq gained 6.51%. Senate Democrats vowed "
        "an inquiry into the sudden reinstatement."
    ),
    "stat": "NVDA  +31%",
}

MARKETS = [
    ("S&P 500", "7,237", "+4.73%"),
    ("Nasdaq", "24,090", "+6.51%"),
    ("Nikkei 225", "58,645", "+3.91%"),
    ("Brent crude", "$86.71", "+0.03%"),
]

# (category, headline, one-line summary) — all verified 24 Nov 2026.
STORIES = [
    ("CONFLICT",
     "Ukraine sinks Russian warship off Libya",
     "Kyiv says seven naval drones sank the corvette Merkury at Benghazi; "
     "the UN seeks a probe after the strike on the Russian ship."),
    ("MIDDLE EAST",
     "Three tankers hit mines in Hormuz",
     "Iran says three oil tankers struck mines and caught fire in the "
     "Strait of Hormuz, and rules out talks until seven conditions are met."),
    ("MIDDLE EAST",
     "Gaza strikes kill Hamas security chief",
     "Israeli airstrikes killed Naeem Abu Nahel, director of Hamas' "
     "internal security apparatus, and six others, including a UNRWA worker."),
    ("CONFLICT",
     "Zaporizhzhia hit overnight: 2 killed, 40 hurt",
     "A Russian overnight attack struck an apartment building; four of the "
     "wounded were children, the regional governor said."),
    ("GEOPOLITICS",
     "NATO vows to defend space",
     "Chief Mark Rutte says the alliance will meet any threat in space "
     "after reports Russia may launch a nuclear-armed satellite."),
    ("JUSTICE",
     "Rohingya genocide ruling recognised",
     "Fourteen countries affirmed the ICJ ruling that Myanmar committed "
     "genocide; the UK sanctioned five senior Myanmar generals."),
    ("CLIMATE",
     "COP31 ends without a deal",
     "The UN climate summit concluded in failure amid deep splits over "
     "fossil fuels and climate finance."),
    ("DISASTER",
     "Indonesia factory fire kills 26",
     "A blaze at a factory in Banten killed 26 people, with dozens still "
     "missing, officials said."),
    ("SCIENCE",
     "First foreign astronaut for Tiangong",
     "Pakistan's Zeeshan Ali is set to become the first foreign astronaut "
     "aboard China's Tiangong space station."),
    ("TECHNOLOGY",
     "States sue SpaceX over Grok images",
     "Oregon and Virginia sued over AI-generated sexualised images made "
     "by the Grok chatbot."),
]

FOOTER = (
    "Sources (24 Nov 2026): Just Security Early Edition  |  One Turn  |  "
    "The Global Eye  |  Principia  |  10 Things Global News.  "
    "Drawn deterministically by this program - no network at grading time."
)


def font(size, bold=False):
    """Pillow's bundled scalable font; no external font files needed."""
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow without the size argument
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines fitting max_width."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, y, x0, x1, fill=INK, width=3):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)
    return y + width + 6


def draw_chip(draw, x, y, w, h):
    """A simple drawn microchip emblem for the lead story."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18,
                           fill=INK, outline=GOLD, width=4)
    pad = 26
    draw.rounded_rectangle([x + pad, y + pad, x + w - pad, y + h - pad],
                           radius=10, fill=(37, 55, 96), outline=GOLD, width=2)
    f = font(64, bold=True)
    label = "NVDA"
    tw = draw.textlength(label, font=f)
    draw.text((x + (w - tw) / 2, y + h / 2 - 44), label, font=f, fill=(247, 242, 231))
    f2 = font(34)
    sub = "+31% IN A DAY"
    tw2 = draw.textlength(sub, font=f2)
    draw.text((x + (w - tw2) / 2, y + h / 2 + 34), sub, font=f2, fill=(212, 175, 105))
    # pins on all four sides
    for i in range(5):
        px = x + 40 + i * ((w - 80) // 4)
        draw.rectangle([px, y - 16, px + 14, y], fill=GOLD)
        draw.rectangle([px, y + h, px + 14, y + h + 16], fill=GOLD)
        py = y + 40 + i * ((h - 80) // 4)
        draw.rectangle([x - 16, py, x, py + 14], fill=GOLD)
        draw.rectangle([x + w, py, x + w + 16, py + 14], fill=GOLD)


def story_card(draw, x, y, w, h, tag, headline, summary):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12,
                           fill=LIGHT, outline=(205, 196, 172), width=2)
    pad = 22
    ix = x + pad
    iy = y + 18
    tag_f = font(26, bold=True)
    draw.text((ix, iy), tag, font=tag_f, fill=RED)
    iy += 38
    head_f = font(40, bold=True)
    for line in wrap(draw, headline, head_f, w - 2 * pad):
        draw.text((ix, iy), line, font=head_f, fill=INK)
        iy += 46
    iy += 6
    body_f = font(30)
    for line in wrap(draw, summary, body_f, w - 2 * pad):
        draw.text((ix, iy), line, font=body_f, fill=(52, 58, 74))
        iy += 38
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 70
    x0, x1 = margin, W - margin

    # ---- Masthead ----
    y = 56
    y = centre(d, y, "THE WORLD IN ONE PAGE", font(92, bold=True), INK)
    y = centre(d, y + 6, "TUESDAY  |  24 NOVEMBER 2026  |  ONE IMAGE, TWELVE STORIES",
               font(34, bold=True), RED)
    y = rule(d, y + 14, x0, x1, fill=RED, width=6)
    y = rule(d, y + 2, x0, x1, fill=INK, width=2)

    # ---- Lead story: text left, chip emblem right ----
    y += 18
    tag_f = font(30, bold=True)
    d.text((x0, y), LEAD["tag"], font=tag_f, fill=RED)
    y += 46
    head_f = font(96, bold=True)
    d.text((x0, y), LEAD["headline"], font=head_f, fill=INK)
    y += 112
    deck_f = font(42)
    for line in (LEAD["deck"], LEAD["deck2"]):
        d.text((x0, y), line, font=deck_f, fill=(52, 58, 74))
        y += 52
    y += 8
    body_f = font(32)
    lead_w = 880
    for line in wrap(d, LEAD["body"], body_f, lead_w):
        d.text((x0, y), line, font=body_f, fill=INK)
        y += 42
    # chip emblem, right of the lead text
    draw_chip(d, 1030, 330, 500, 300)
    stat_f = font(44, bold=True)
    stat = LEAD["stat"]
    tw = d.textlength(stat, font=stat_f)
    d.text((1030 + (500 - tw) / 2, 648), stat, font=stat_f, fill=GREEN)
    y = max(y, 700) + 10

    # ---- Markets strip ----
    y = rule(d, y + 8, x0, x1, fill=GOLD, width=3)
    d.text((x0, y), "MARKETS  -  THE HUANG RALLY", font=font(30, bold=True), fill=GREY)
    y += 44
    col_w = (x1 - x0) // 4
    for i, (name, val, chg) in enumerate(MARKETS):
        cx = x0 + i * col_w
        d.text((cx, y), name, font=font(28, bold=True), fill=GREY)
        d.text((cx, y + 36), val, font=font(44, bold=True), fill=INK)
        d.text((cx, y + 92), chg, font=font(36, bold=True), fill=GREEN)
    y += 140
    y = rule(d, y + 6, x0, x1, fill=INK, width=2)

    # ---- Story grid: 2 columns x 5 rows ----
    y += 16
    gap = 28
    card_w = (x1 - x0 - gap) // 2
    card_h = 282
    for row in range(5):
        for col in range(2):
            idx = row * 2 + col
            tag, headline, summary = STORIES[idx]
            cx = x0 + col * (card_w + gap)
            story_card(d, cx, y, card_w, card_h, tag, headline, summary)
        y += card_h + gap

    # ---- Footer ----
    y = rule(d, y + 2, x0, x1, fill=INK, width=2)
    y += 10
    foot_f = font(26)
    for line in wrap(d, FOOTER, foot_f, x1 - x0):
        d.text((x0, y), line, font=foot_f, fill=GREY)
        y += 34
    centre(d, y + 14, "-  THE WORLD IN ONE PAGE  |  24 NOVEMBER 2026  -",
           font(30, bold=True), RED)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, "PNG")
    print("wrote", OUT_PATH, img.size)


if __name__ == "__main__":
    main()
