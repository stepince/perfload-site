"""YouTube thumbnail 2 (1280x720): "Compare load tests!" - TEST A vs TEST B.
Run from this folder: python3 thumbnail_compare.py -> ../../assets/branding/perfload-thumbnail-compare-1280x720.png"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '../../assets/branding/perfload-thumbnail-compare-1280x720.png'
W, H, S = 1280, 720, 2
NAVY = (8, 12, 28); PANEL = (15, 22, 46); LINE = (38, 52, 92)
CYAN = (34, 211, 238); TEAL = (45, 212, 191); IND = (79, 70, 229); BLUE = (59, 130, 246)
WHITE = (255, 255, 255); MUT = (150, 163, 190); GREEN = (52, 211, 153); ORANGE = (251, 146, 60)
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
def F(sz, bold=True): return ImageFont.truetype(HN, round(sz * S), index=1 if bold else 0)
def MONO(sz): return ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', round(sz * S))
s = lambda v: round(v * S)

img = Image.new('RGB', (W * S, H * S), NAVY)
glow = Image.new('RGB', img.size, NAVY); g = ImageDraw.Draw(glow)
g.ellipse((s(680), s(-200), s(1500), s(520)), fill=(30, 64, 175)); g.ellipse((s(-250), s(300), s(560), s(900)), fill=(67, 56, 202))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(s(170))), 0.6)
d = ImageDraw.Draw(img, 'RGBA')
for x in range(0, W, 80): d.line((s(x), 0, s(x), s(H)), fill=(255, 255, 255, 7), width=1)
for y in range(0, H, 80): d.line((0, s(y), s(W), s(y)), fill=(255, 255, 255, 7), width=1)
for i, ln in enumerate(['$ perfload run --vus 100 --duration 60s', '  BASE_URL=https://api.example.com', '$ perfload compare run-A run-B', '  p95  910ms -> 340ms', '  errors  2.4% -> 0.1%'] * 5):
    d.text((s(18), s(8 + i * 27)), ln, font=MONO(15), fill=(24, 36, 74))

def rrect(box, r, fill=None, outline=None, w=1): d.rounded_rectangle([s(v) for v in box], radius=s(r), fill=fill, outline=outline, width=s(w))
def text(xy, t, font, fill, anchor='la'): d.text((s(xy[0]), s(xy[1])), t, font=font, fill=fill, anchor=anchor)
def fit(t, target, bold=True):
    sz = 40
    while d.textlength(t, font=F(sz, bold)) / S < target: sz += 1
    return sz
def mark(x, y, size, color=WHITE):
    k = size / 32
    for pts in ([(9.3, 9.3), (15.7, 16), (9.3, 22.7)], [(17.6, 22.0), (24.6, 22.0)]):
        P = [(s(x + a * k), s(y + b * k)) for a, b in pts]
        d.line(P, fill=color, width=round(2.3 * k * S), joint='curve')
        r = 1.15 * k * S
        for px, py in P: d.ellipse((px - r, py - r, px + r, py + r), fill=color)

# ---- left: brand, headline, secondary, variables panel, url ----
rrect((60, 46, 118, 104), 14, fill=IND); mark(60, 46, 58)
text((134, 76), 'PERFLOAD', F(40), WHITE, 'lm')
c1 = fit('COMPARE', 520); text((58, 140), 'COMPARE', F(c1), WHITE)
c2 = fit('LOAD TESTS!', 520); text((62, 140 + c1 * 1.02), 'LOAD TESTS!', F(c2), CYAN)
ys = 140 + c1 * 1.02 + c2 * 1.1
text((62, ys), 'Variables + Performance Analysis', F(27), (210, 220, 240))
PX, PY, PW, PH = 60, ys + 52, 500, 128
rrect((PX, PY, PX + PW, PY + PH), 14, fill=(11, 17, 38, 255), outline=LINE + (255,), w=2)
for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((s(PX + 16 + i * 18), s(PY + 14), s(PX + 26 + i * 18), s(PY + 24)), fill=c)
text((PX + 90, PY + 19), 'variables.env', MONO(14), MUT, 'lm')
for i, (k, v, vc) in enumerate([('BASE_URL', '=https://api.example.com', (170, 195, 255)), ('VUS', '=100', CYAN), ('DURATION', '=60s', CYAN)]):
    text((PX + 20, PY + 40 + i * 28), k, MONO(19), (125, 211, 252)); text((PX + 20 + d.textlength(k, font=MONO(19)) / S, PY + 40 + i * 28), v, MONO(19), vc)
text((62, 660), 'perfload.io', F(36), WHITE, 'lm'); d.rounded_rectangle((s(62), s(684), s(132), s(688)), radius=s(2), fill=CYAN + (255,))

# ---- right: TEST A / TEST B ----
CW, CH, CY0 = 280, 540, 85
def sparkline(cx0, cy0, cx1, cy1, seed, level, amp, col):
    random.seed(seed); pts = []
    for i in range(41):
        t = i / 40; v = level + amp * math.sin(t * 17 + seed) + random.uniform(-amp, amp) * 0.9
        pts.append((cx0 + t * (cx1 - cx0), cy0 + v * (cy1 - cy0)))
    return pts, col
def card(x, label, acc, big, bigcol, rows, spark, winner):
    global img, d
    if winner:
        gl = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((s(x), s(CY0), s(x + CW), s(CY0 + CH)), radius=s(20), outline=CYAN + (255,), width=s(8))
        img = Image.alpha_composite(img.convert('RGBA'), gl.filter(ImageFilter.GaussianBlur(s(14)))).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
    else:
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((s(x), s(CY0 + 12), s(x + CW), s(CY0 + CH + 12)), radius=s(20), fill=(0, 0, 0, 160))
        img = Image.alpha_composite(img.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(s(20)))).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
    rrect((x, CY0, x + CW, CY0 + CH), 20, fill=PANEL + (255,), outline=(CYAN if winner else (70, 90, 150)) + (255,), w=3 if winner else 2)
    rrect((x + 20, CY0 + 20, x + 20 + 108, CY0 + 54), 17, fill=acc + (255,))
    text((x + 20 + 54, CY0 + 37), label, F(20), WHITE, 'mm')
    text((x + 20, CY0 + 82), 'AVG RESPONSE TIME', F(13), MUT)
    text((x + 20, CY0 + 100), big, F(84), bigcol)
    bw = d.textlength(big, font=F(84)) / S; text((x + 28 + bw, CY0 + 160), 'ms', F(28), MUT, 'la')
    pts, col = spark
    P = [(s(a), s(b)) for a, b in pts]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.polygon(P + [(P[-1][0], s(CY0 + 300)), (P[0][0], s(CY0 + 300))], fill=col + (40,)); ld.line(P, fill=col + (255,), width=s(3), joint='curve')
    img = Image.alpha_composite(img.convert('RGBA'), lay.filter(ImageFilter.GaussianBlur(s(5)))); img = Image.alpha_composite(img, lay).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
    for i, (lab, val, vc) in enumerate(rows):
        yy = CY0 + 328 + i * 68
        d.line((s(x + 20), s(yy - 2), s(x + CW - 20), s(yy - 2)), fill=LINE + (255,), width=s(1.5))
        text((x + 20, yy + 6), lab, F(13), MUT); text((x + 20, yy + 24), val, F(30), vc)
XA, XB = 620, 950
card(XA, 'TEST A', (71, 85, 120), '450', ORANGE, [('THROUGHPUT', '820 req/s', WHITE), ('ERROR RATE', '2.4%', ORANGE), ('P95 LATENCY', '910 ms', WHITE)],
     sparkline(XA + 24, CY0 + 215, XA + CW - 24, CY0 + 295, 4, 0.30, 0.20, ORANGE), False)
card(XB, 'TEST B', (13, 148, 136), '180', GREEN, [('THROUGHPUT', '1,950 req/s', WHITE), ('ERROR RATE', '0.1%', GREEN), ('P95 LATENCY', '340 ms', WHITE)],
     sparkline(XB + 24, CY0 + 215, XB + CW - 24, CY0 + 295, 9, 0.78, 0.06, CYAN), True)
# arrow badge between the two results
bx, by = 925, 205
d.ellipse((s(bx - 46), s(by - 46), s(bx + 46), s(by + 46)), fill=NAVY + (255,))
d.ellipse((s(bx - 40), s(by - 40), s(bx + 40), s(by + 40)), fill=CYAN + (255,))
d.polygon([(s(bx - 12), s(by - 24)), (s(bx + 12), s(by - 24)), (s(bx + 12), s(by + 2)), (s(bx + 26), s(by + 2)), (s(bx), s(by + 30)), (s(bx - 26), s(by + 2)), (s(bx - 12), s(by + 2))], fill=NAVY + (255,))
rrect((bx - 46, by + 56, bx + 46, by + 94), 19, fill=NAVY + (255,), outline=GREEN + (255,), w=2.5)
text((bx, by + 75), '-60%', F(26), GREEN, 'mm')
img.convert('RGB').resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
