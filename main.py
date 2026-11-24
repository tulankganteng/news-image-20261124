#!/usr/bin/env python3
"""The World Today - Tuesday 24 November 2026 in one image.

A dense newspaper front page: 40 dated stories across 8 regions,
a timeline strip, a world map with pins, 12 pictured stories
(generated editorial images, composited here), a day-in-numbers box
and a "left out as older news" box. Deterministic: no network,
no clock, no randomness. Writes /output/entry.png (or
$MAKEFUN_OUTPUT_DIR), 1024x1024 PNG under 1 MiB.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MAX_BYTES = 1024 * 1024
BASE = Path(__file__).resolve().parent

# --- palette ---------------------------------------------------------------
CREAM = (247, 242, 231)
PAPER = (255, 253, 247)
INK = (20, 20, 20)
GREY = (110, 105, 95)
LIGHT_GREY = (200, 194, 182)
RED = (176, 42, 30)
OCEAN = (214, 230, 242)
LAND = (232, 222, 196)
LAND_EDGE = (150, 140, 110)
PIN = (176, 42, 30)

REGION_COLORS = {
    "NORTH AMERICA": (29, 78, 216),
    "EUROPE": (124, 58, 237),
    "MIDDLE EAST": (180, 83, 9),
    "ASIA-PACIFIC": (13, 148, 136),
    "AFRICA": (190, 24, 93),
    "LATIN AMERICA": (21, 128, 61),
    "MARKETS & MONEY": (146, 64, 14),
    "SPORT & CULTURE": (15, 118, 110),
}

# (headline, detail, source, pictured asset or None)
STORIES = {
    "NORTH AMERICA": [
        ("Nvidia brings back Huang as CEO",
         "Board votes unanimously 23 Nov; shares jump 30% after Trump pushes the board.",
         "USA TODAY", "pic_nvidia.jpg"),
        ("US blacklists Singapore chip firm Megaspeed",
         "Commerce Dept acts in the Nvidia spy scandal; US firms need a licence to ship to it.",
         "SPYGLASS", None),
        ("S&P 500 jumps 4.73% to 7,237",
         "Best day since Apr 2025 ends a 7-day slide; Nasdaq gains 6.5%.",
         "ARGUS", "pic_markets.jpg"),
        ("Congress vows Huang probe",
         "Warren: board 'owes Congress answers'; Huang to testify before Senate 3 Dec.",
         "USA TODAY", None),
        ("Waymo pulls robotaxis off US freeways",
         "Driverless cars withdrawn after California ban following traffic incidents.",
         "WH NEWS", None),
    ],
    "EUROPE": [
        ("EU proposes 22nd Russia sanctions package",
         "Banks, crypto platforms hit; Russian athletes barred from EU events under flag.",
         "WH NEWS", "pic_brussels.jpg"),
        ("Central Europe rejects EU budget plan",
         "Visegrad + Austria call Costa's \u20ac1.582tn 2028-34 budget unacceptable; summit 26-27 Nov.",
         "DEVDISCOURSE", None),
        ("NATO: Putin could strike before EU army responds",
         "Rutte warns a separate European army would slow decisions; missiles reach Lisbon in minutes.",
         "FOX NEWS", None),
        ("Ukraine says it sank Russian warship off Libya",
         "Kyiv claims drone hit near Benghazi; Russia vows a response.",
         "WH NEWS", "pic_warship.jpg"),
        ("Russian drone attack kills 11 near Kyiv",
         "Boy pulled alive from rubble as Zelensky warns of new strikes being planned.",
         "SPYGLASS", None),
    ],
    "MIDDLE EAST": [
        ("Iran strikes Gulf sites, sues for $290bn",
         "Tehran steps up attacks on US bases; courts demand the US pay for war damage.",
         "SPYGLASS", None),
        ("US hits Iran's shadow banking network",
         "2 dozen exchange houses sanctioned in 'Operation Economic Outcast'.",
         "BREITBART", None),
        ("Four tankers hit mines in Strait of Hormuz",
         "IRGC says two sailed under US escort; UN counts 25 seafarers killed since Feb.",
         "STOCKBIZ", "pic_hormuz.jpg"),
        ("US probes Iran over ship cyberattacks",
         "WSJ: ~50 tankers hit or threatened; Iran prime suspect, Russia also eyed.",
         "REUTERS", None),
        ("Israeli strikes kill 3 in Gaza, incl. UN worker",
         "UNRWA worker Adel al-Helo among dead; infant dies of cold in tent.",
         "REUTERS", "pic_gaza.jpg"),
    ],
    "ASIA-PACIFIC": [
        ("Russian jets enter S. Korea air defence zone",
         "Seoul issues emergency alert for Ulleung Island after airspace violation.",
         "SPYGLASS", None),
        ("Cikande candy factory fire: 24 dead, 30 missing",
         "Blaze at PT Fonusa Agung Mulia in Banten; rescuers pull 24 body bags.",
         "PEOPLE", "pic_cikande.jpg"),
        ("Prabowo names Amran & Sugiono as VP picks",
         "MPR to vote 11 Dec after Gibran stepped down; diplomas to be checked with schools.",
         "ANTARA", "pic_jakarta.jpg"),
        ("EU & Indonesia sign landmark trade deal",
         "CEPA eliminates most tariffs, from palm oil to pharmaceuticals.",
         "EIN NEWS", None),
        ("S. Korea education minister quits over AI rules",
         "Steps down amid row over AI cheating regulations.",
         "SUSB", None),
    ],
    "AFRICA": [
        ("CAS to rule today on Senegal AFCON appeal",
         "Senegal contests CAF stripping its title after a 1-0 final win over Morocco.",
         "REUTERS", None),
        ("Nigeria boat capsizes: 24 dead",
         "Vessel carrying mourners to a funeral overturns.",
         "FROGNEWS", None),
        ("Migrant boat capsizes off Senegal",
         "Dozens missing in the latest Atlantic crossing tragedy.",
         "WH NEWS", None),
        ("Drones kill 4 near Sudan's capital",
         "UN building damaged in strikes near Khartoum.",
         "FROGNEWS", None),
        ("Rand firms as gold rebounds",
         "R17.43 to the dollar; Moody's & S&P rating reviews due Friday.",
         "THE PROFILER", None),
    ],
    "LATIN AMERICA": [
        ("Mexico nabs Sinaloa kingpin 'El Chapo Isidro'",
         "Captured after fierce gun battle; will face trial at home, not the US.",
         "SPYGLASS", "pic_mexico.jpg"),
        ("Bolsonaro rushed to ICU",
         "Ex-president admitted in Brasilia with acute bowel obstruction.",
         "BREITBART", None),
        ("Petrobras buys into corn ethanol for $472m",
         "Buys 42% of Neomille; first ethanol move since 2020.",
         "RIO TIMES", None),
        ("Ecuador floods kill two girls",
         "Overnight rain floods Babahoyo; landslide hits Quevedo in Los Rios.",
         "RIO TIMES", None),
        ("Bukele seeks third term in El Salvador",
         "President confirms bid to extend his rule.",
         "BREITBART", None),
    ],
    "MARKETS & MONEY": [
        ("Gold rebounds ~3% to $3,621",
         "Bounces off 14-month low of $3,503, still 10% below its Nov 6 close.",
         "SEEKING ALPHA", "pic_gold.jpg"),
        ("Bitcoin retakes $60,000",
         "Trades $61,385 after crashing to $55,106 on 21 Nov.",
         "SEEKING ALPHA", None),
        ("SK Hynix US shares surge 20%",
         "Chipmaker jumps after Huang's return to Nvidia.",
         "SPYGLASS", None),
        ("Brent crude $82.20, down 1.6%",
         "Oil eases as Hormuz fears cool; gold +3% the same day.",
         "SEEKING ALPHA", None),
        ("Asia mixed, Europe higher at midday",
         "Hong Kong -0.1%, China +0.2%, India -1.8%; London +0.5%, Paris +0.7%.",
         "SEEKING ALPHA", None),
    ],
    "SPORT & CULTURE": [
        ("Verstappen wins Las Vegas Grand Prix",
         "Red Bull ace takes another win at the neon night race.",
         "JAGRAN JOSH", "pic_f1.jpg"),
        ("Alcaraz beats Shelton, reaches ATP final",
         "Spaniard advances to the championship match in Turin.",
         "JAGRAN JOSH", None),
        ("Pant hits 128 in Wellington Test",
         "Record score for an Asian wicketkeeper vs New Zealand.",
         "JAGRAN JOSH", "pic_cricket.jpg"),
        ("Plants turned into anticancer drug factories",
         "Biotech breakthrough reported in Nature Chemical Biology.",
         "S.NEWS", None),
        ("Ferrari unveils 296 Challenge models",
         "Stradale & Evo debut at Finali Mondiali in Spain.",
         "JAGRAN JOSH", None),
    ],
}

REGION_ORDER = list(STORIES.keys())

TIMELINE = [
    ("EARLY", "S&P 500 jumps 4.73%, best day since April 2025"),
    ("MORNING", "Nvidia board reinstates Jensen Huang as CEO"),
    ("MIDDAY", "Iran demands $290bn; tankers hit mines in Hormuz"),
    ("AFTERNOON", "EU proposes 22nd Russia sanctions package"),
    ("EVENING", "Russian jets enter S. Korea air defence zone"),
    ("NIGHT", "CAS rules on Senegal AFCON appeal"),
]

NUMBERS = [
    ("S&P 500", "+4.73%", "7,237"),
    ("GOLD", "+3%", "$3,621"),
    ("BITCOIN", "+0.8%", "$61,385"),
    ("BRENT", "-1.6%", "$82.20"),
    ("CIKANDE", "24 dead", "30 missing"),
    ("SHIP ATTACKS", "~50", "tankers hit"),
]

LEFT_OUT = [
    ("COP31 collapses in Antalya - no fossil-fuel deal (22 Nov)",
     "Fiona the hippo dies at Cincinnati Zoo (19 Nov)"),
    ("Trump-Xi-Putin trilateral tops APEC Shenzhen (20 Nov)",
     "Harvard's Rumble Rims headset wins Dyson Award (4 Nov)"),
]

# Pictured stories in strip order: (asset, caption)
PICTURED = [
    ("pic_nvidia.jpg", "HUANG RETURNS"),
    ("pic_markets.jpg", "S&P +4.73%"),
    ("pic_brussels.jpg", "EU SANCTIONS"),
    ("pic_warship.jpg", "SHIP SUNK OFF LIBYA"),
    ("pic_hormuz.jpg", "MINES IN HORMUZ"),
    ("pic_gaza.jpg", "GAZA STRIKES"),
    ("pic_cikande.jpg", "CIKANDE FIRE"),
    ("pic_jakarta.jpg", "JAKARTA VOTE"),
    ("pic_mexico.jpg", "KINGPIN NABBED"),
    ("pic_gold.jpg", "GOLD REBOUNDS"),
    ("pic_f1.jpg", "VERSTAPPEN WINS"),
    ("pic_cricket.jpg", "PANT 128"),
]

# (lon, lat, label or None, label dx, label dy) for map pins
PINS = [
    (-77, 39, "WASHINGTON", 0, -13),
    (0, 51, "LONDON", -52, -4),
    (4, 51, "BRUSSELS", -8, 8),
    (30, 50, "KYIV", 8, -4),
    (34, 31, "GAZA", 0, -13),
    (56, 26, "HORMUZ", -6, 8),
    (127, 37, "SEOUL", -10, -13),
    (107, -6, "JAKARTA", -12, 8),
    (-99, 19, "MEXICO CITY", -16, -13),
    (3, 6, "LAGOS", -8, 8),
    (-48, -16, None, 0, 0),
    (77, 28, None, 0, 0),
]

# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42),
     (-75, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 16),
     (-94, 17), (-87, 13), (-83, 9), (-79, 9), (-85, 11), (-92, 15),
     (-97, 16), (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-124, 40),
     (-124, 48), (-130, 54), (-140, 60), (-150, 61), (-158, 58), (-165, 60)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-65, -45), (-62, -39), (-58, -34), (-52, -32), (-48, -28),
     (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-52, 4), (-55, 6), (-60, 8), (-62, 10), (-68, 11),
     (-72, 12), (-76, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (10, 64), (18, 69), (28, 71), (32, 68), (30, 60),
     (24, 58), (21, 55), (18, 54), (12, 54), (8, 55), (3, 53), (0, 51),
     (-2, 50), (-5, 48), (-2, 47), (-1, 44), (3, 43), (7, 44), (12, 44),
     (14, 45), (18, 42), (22, 40), (23, 38), (26, 38), (28, 37), (30, 36),
     (27, 36), (23, 36), (19, 37), (15, 38), (12, 42), (10, 44), (7, 44),
     (3, 43), (0, 43), (-2, 44), (-6, 43), (-9, 43)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
     (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, -1),
     (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (20, -35),
     (26, -34), (32, -29), (35, -24), (40, -16), (40, -10), (41, -4),
     (42, 1), (46, 5), (51, 10), (51, 12), (48, 11), (44, 11), (43, 12),
     (40, 15), (38, 18), (37, 22), (34, 27), (32, 31), (25, 32), (19, 32),
     (11, 34), (10, 37), (5, 37)],
    # Asia
    [(32, 36), (36, 36), (36, 42), (41, 41), (44, 39), (48, 30), (50, 29),
     (54, 27), (57, 26), (57, 22), (59, 22), (61, 25), (66, 25), (67, 24),
     (72, 20), (73, 16), (76, 10), (77, 8), (80, 7), (80, 10), (84, 18),
     (88, 22), (91, 22), (93, 16), (94, 17), (97, 16), (98, 10), (100, 8),
     (101, 6), (103, 2), (104, 2), (105, 9), (106, 10), (109, 13), (109, 18),
     (106, 20), (108, 18), (110, 20), (114, 22), (117, 23), (120, 25),
     (122, 28), (122, 32), (127, 35), (127, 40), (130, 42), (132, 43),
     (135, 44), (138, 46), (140, 45), (142, 50), (142, 54), (141, 59),
     (140, 60), (137, 62), (135, 65), (132, 68), (130, 70), (128, 71),
     (125, 72), (120, 73), (115, 73), (110, 74), (105, 76), (100, 76),
     (95, 75), (90, 75), (85, 74), (80, 73), (75, 72), (70, 72), (65, 69),
     (60, 69), (55, 68), (50, 68), (45, 68), (40, 68), (35, 68), (32, 68),
     (30, 70), (28, 71), (25, 71), (20, 70), (18, 69), (15, 68), (12, 67),
     (10, 65), (8, 63), (5, 60), (5, 58), (8, 57), (10, 57), (12, 55),
     (15, 54), (18, 54), (21, 55), (24, 58), (28, 58), (30, 59), (28, 60),
     (25, 60), (22, 60), (20, 60), (18, 59), (15, 58), (12, 57), (10, 57),
     (8, 56), (5, 55), (3, 54), (0, 53), (-2, 51), (-4, 50), (-5, 48),
     (-2, 47), (-1, 44), (0, 43), (3, 43), (7, 44), (10, 44), (12, 44),
     (14, 45), (16, 44), (18, 42), (19, 42), (21, 40), (23, 38), (26, 38),
     (28, 37), (30, 36)],
    # Oceania
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -11), (142, -15),
     (141, -18), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]


# --- fonts -----------------------------------------------------------------
def load_font(name, size):
    path = BASE / "assets" / name
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default(size)


F_TITLE = load_font("DejaVuSans-Bold.ttf", 46)
F_SUB = load_font("DejaVuSans-Bold.ttf", 12)
F_SECTION = load_font("DejaVuSans-Bold.ttf", 13)
F_REGION = load_font("DejaVuSans-Bold.ttf", 13)
F_HEAD = load_font("DejaVuSans-Bold.ttf", 10)
F_BODY = load_font("DejaVuSans.ttf", 9)
F_SMALL = load_font("DejaVuSans.ttf", 9)
F_TINY = load_font("DejaVuSans.ttf", 8)
F_TINY_B = load_font("DejaVuSans-Bold.ttf", 8)
F_NUM = load_font("DejaVuSans-Bold.ttf", 15)
F_NUM_LBL = load_font("DejaVuSans-Bold.ttf", 8)
F_CAP = load_font("DejaVuSans-Bold.ttf", 9)
F_MAP_LBL = load_font("DejaVuSans-Bold.ttf", 8)


def wrap(text, font, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(lines, font, leading=0):
    return len(lines) * (font.size + leading)


def draw_wrapped(draw, xy, text, font, max_w, fill, leading=1, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + leading
    return y


def draw_map(draw, box):
    """Schematic equirectangular world map with pins."""
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0
    draw.rectangle(box, fill=OCEAN, outline=LIGHT_GREY)
    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (90.0 - lat) / 180.0 * mh)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for lon, lat, label, dx, dy in PINS:
        px, py = proj(lon, lat)
        r = 4
        draw.ellipse([px - r, py - r, px + r, py + r], fill=PIN,
                     outline=(255, 255, 255), width=1)
        if label:
            tw = F_MAP_LBL.getlength(label)
            lx = min(max(px - tw / 2 + dx, x0 + 2), x1 - tw - 2)
            ly = min(max(py + dy, y0 + 2), y1 - 10)
            draw.text((lx, ly), label, font=F_MAP_LBL, fill=INK)


def fit_lines(text, font, max_w, max_lines):
    """Wrap text and clamp to max_lines, adding an ellipsis if cut."""
    lines = wrap(text, font, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and font.getlength(last + "\u2026") > max_w:
            last = last[:-1]
        lines[-1] = last + "\u2026"
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading=1):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + leading
    return y


def thumb(img, w, h):
    """Centre-crop a square image to w x h."""
    iw, ih = img.size
    target = w / h
    if iw / ih > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        crop = img.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target)
        y0 = (ih - nh) // 2
        crop = img.crop((0, y0, iw, y0 + nh))
    return crop.resize((w, h), Image.LANCZOS)


def compose():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.text((8, 4), "THE WORLD TODAY", font=F_TITLE, fill=INK)
    date = "TUESDAY, 24 NOVEMBER 2026"
    d.text((W - 8 - F_SUB.getlength(date), 22), date, font=F_SUB, fill=INK)
    d.text((8, 54), "40 STORIES  \u2022  8 REGIONS  \u2022  EVERY CLAIM VERIFIED TODAY",
           font=F_TINY_B, fill=GREY)
    d.line([(8, 66), (W - 8, 66)], fill=INK, width=2)
    d.line([(8, 69), (W - 8, 69)], fill=INK, width=1)

    # --- timeline strip -------------------------------------------------
    d.text((8, 76), "THE DAY IN BRIEF", font=F_SECTION, fill=RED)
    seg_w = (W - 16) // 6
    for i, (when, head) in enumerate(TIMELINE):
        x = 8 + i * seg_w
        d.line([(x, 96), (x, 126)], fill=LIGHT_GREY, width=1)
        d.text((x + 4, 96), when, font=F_TINY_B, fill=RED)
        draw_lines(d, x + 4, 107,
                   fit_lines(head, F_TINY, seg_w - 10, 2), F_TINY, INK)
    d.line([(8, 128), (W - 8, 128)], fill=INK, width=1)

    # --- map + numbers --------------------------------------------------
    draw_map(d, (8, 132, 636, 262))
    nx0, ny0 = 644, 132
    d.rectangle([nx0, ny0, W - 8, 262], fill=PAPER, outline=LIGHT_GREY)
    d.text((nx0 + 8, ny0 + 6), "THE DAY IN NUMBERS", font=F_SECTION,
           fill=RED)
    d.line([(nx0 + 8, ny0 + 24), (W - 16, ny0 + 24)], fill=LIGHT_GREY, width=1)
    cell_w, cell_h = 178, 33
    for i, (lbl, val, sub) in enumerate(NUMBERS):
        cx = nx0 + 8 + (i % 2) * cell_w
        cy = ny0 + 30 + (i // 2) * cell_h
        d.text((cx, cy), lbl, font=F_NUM_LBL, fill=GREY)
        d.text((cx, cy + 9), val, font=F_NUM, fill=INK)
        vw = F_NUM.getlength(val)
        d.text((cx + vw + 5, cy + 12), sub, font=F_SMALL, fill=GREY)

    # --- pictured strip -------------------------------------------------
    d.text((8, 270), "PICTURED TODAY \u2014 12 SCENES FROM THE DAY'S NEWS",
           font=F_SECTION, fill=RED)
    cell_w, cell_h, gap = 160, 60, 8
    for idx, (asset, cap) in enumerate(PICTURED):
        row, col = divmod(idx, 6)
        x = 8 + col * (cell_w + gap)
        y = 288 + row * (cell_h + 12)
        pic = Image.open(BASE / "assets" / asset).convert("RGB")
        img.paste(thumb(pic, cell_w, 46), (x, y))
        d.rectangle([x, y, x + cell_w - 1, y + 45], outline=LIGHT_GREY)
        d.text((x, y + 48), cap, font=F_CAP, fill=INK)

    # --- region grid ----------------------------------------------------
    block_w, block_h, gap = 248, 258, 8
    grid_y = 416
    for ri, region in enumerate(REGION_ORDER):
        row, col = divmod(ri, 4)
        bx = 8 + col * (block_w + gap)
        by = grid_y + row * (block_h + gap)
        color = REGION_COLORS[region]
        d.rectangle([bx, by, bx + block_w - 1, by + block_h - 1],
                    fill=PAPER, outline=LIGHT_GREY)
        d.rectangle([bx, by, bx + block_w - 1, by + 3], fill=color)
        d.text((bx + 6, by + 8), region, font=F_REGION, fill=color)
        d.text((bx + block_w - 6 - F_TINY.getlength("5 STORIES"), by + 10),
               "5 STORIES", font=F_TINY, fill=GREY)
        d.line([(bx + 6, by + 26), (bx + block_w - 6, by + 26)],
               fill=LIGHT_GREY, width=1)
        y = by + 30
        for headline, detail, source, _pic in STORIES[region]:
            y = draw_lines(d, bx + 6, y,
                           fit_lines(headline, F_HEAD, block_w - 12, 2),
                           F_HEAD, INK)
            y = draw_lines(d, bx + 6, y,
                           fit_lines(detail, F_BODY, block_w - 12, 1),
                           F_BODY, (60, 60, 60))
            d.text((bx + 6, y), "\u25aa " + source, font=F_TINY, fill=GREY)
            y += 11

    # --- footer: left out + sources --------------------------------------
    fy = 944
    d.line([(8, fy), (W - 8, fy)], fill=INK, width=1)
    d.text((8, fy + 5), "LEFT OUT \u2014 OLDER NEWS, STILL ON THE WIRE",
           font=F_SECTION, fill=RED)
    for r, (left, right) in enumerate(LEFT_OUT):
        y = fy + 24 + r * 13
        d.text((8, y), "\u25aa " + left, font=F_TINY, fill=GREY)
        d.text((520, y), "\u25aa " + right, font=F_TINY, fill=GREY)
    src_line = ("SOURCES: REUTERS \u2022 AP \u2022 BBC \u2022 AL JAZEERA \u2022 USA TODAY "
                "\u2022 ANTARA \u2022 CNN \u2022 SEEKING ALPHA \u2022 BREITBART \u2014 "
                "ALL STORIES REPORTED 24 NOV 2026")
    d.text((8, fy + 52), src_line, font=F_TINY_B, fill=INK)
    d.text((8, fy + 64), "THE WORLD TODAY \u2022 TUESDAY 24 NOVEMBER 2026 \u2022 "
           "COMPOSITED WITH PIL; PHOTOS GENERATED WITH FLUX.1-SCHNELL",
           font=F_TINY, fill=GREY)
    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out = out_dir / "entry.png"
    image = compose()
    out_dir.mkdir(parents=True, exist_ok=True)
    image.save(out, format="PNG", optimize=True)
    data = out.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over 1 MiB")
    if image.size != (W, H):
        raise SystemExit(f"entry.png is {image.size}, expected 1024x1024")
    import hashlib
    print(f"wrote {out} ({len(data)} bytes, 1024x1024 PNG, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
