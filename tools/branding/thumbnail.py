"""YouTube thumbnail (1280x720): "PerfLoad - Your first load test!".
Run from this folder: python3 thumbnail.py  ->  ../../assets/branding/perfload-thumbnail-1280x720.png
Docker / Chrome / k6 marks are simplified drawings, not the official logos."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '../../assets/branding/perfload-thumbnail-1280x720.png'
W, H, S = 1280, 720, 2
NAVY = (8, 12, 28); PANEL = (15, 22, 46); LINE = (38, 52, 92)
BLUE = (59, 130, 246); CYAN = (34, 211, 238); TEAL = (45, 212, 191); IND = (79, 70, 229)
WHITE = (255, 255, 255); MUT = (150, 163, 190)
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
def F(sz, bold=True): return ImageFont.truetype(HN, int(sz * S), index=1 if bold else 0)
MONO = lambda sz: ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', int(sz * S))
s = lambda v: round(v * S)

img = Image.new('RGB', (W * S, H * S), NAVY)
# background glows
glow = Image.new('RGB', img.size, NAVY); g = ImageDraw.Draw(glow)
g.ellipse((s(700), s(-150), s(1500), s(500)), fill=(30, 64, 175))
g.ellipse((s(-250), s(300), s(550), s(900)), fill=(67, 56, 202))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(s(170))), 0.6)
d = ImageDraw.Draw(img, 'RGBA')
# faint terminal text
random.seed(3)
code = ['$ curl -X POST https://api.example.com/orders', '  -H "Authorization: Bearer $TOKEN"', '$ docker run -p 3000:3000 perfload', 'k6 run --vus 50 --duration 60s', '  ✓ status is 200', '  http_req_duration p(95)=182ms', '  checks.........: 100.00%', '$ _']
for i, ln in enumerate(code * 3):
    d.text((s(18), s(8 + i * 27)), ln, font=MONO(15), fill=(30, 44, 88))
# subtle grid
for x in range(0, W, 80): d.line((s(x), 0, s(x), s(H)), fill=(255, 255, 255, 7), width=1)
for y in range(0, H, 80): d.line((0, s(y), s(W), s(y)), fill=(255, 255, 255, 7), width=1)

def rrect(box, r, fill=None, outline=None, w=1):
    d.rounded_rectangle([s(v) for v in box], radius=s(r), fill=fill, outline=outline, width=w * S)
def text(xy, t, font, fill, anchor='la'): d.text((s(xy[0]), s(xy[1])), t, font=font, fill=fill, anchor=anchor)

# prompt mark (same geometry as the favicon)
def mark(x, y, size, color=WHITE):
    k = size / 32
    for pts in ([(9.3, 9.3), (15.7, 16), (9.3, 22.7)], [(17.6, 22.0), (24.6, 22.0)]):
        P = [(s(x + a * k), s(y + b * k)) for a, b in pts]
        d.line(P, fill=color, width=round(2.3 * k * S), joint='curve')
        for px, py in P: d.ellipse((px - 1.15 * k * S, py - 1.15 * k * S, px + 1.15 * k * S, py + 1.15 * k * S), fill=color)

# ---- brand row + headline (left) ----
rrect((60, 52, 112, 104), 12, fill=IND); mark(60, 52, 52)
text((128, 78), 'PerfLoad.io', F(34), WHITE, 'lm')
text((58, 142), 'PERFLOAD', F(112), WHITE)
text((62, 285), 'YOUR FIRST', F(80), WHITE)
text((62, 372), 'LOAD TEST!', F(80), CYAN)

# ---- dashboard (right) ----
DX, DY, DW, DH = 700, 62, 530, 402
sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((s(DX), s(DY + 14), s(DX + DW), s(DY + DH + 14)), radius=s(18), fill=(0, 0, 0, 170))
img = Image.alpha_composite(img.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(s(22)))).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
rrect((DX, DY, DX + DW, DY + DH), 18, fill=PANEL + (255,), outline=(70, 90, 150, 255), w=2)
for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
    d.ellipse((s(DX + 20 + i * 22), s(DY + 18), s(DX + 32 + i * 22), s(DY + 30)), fill=c)
text((DX + 100, DY + 24), 'load test results', MONO(14), MUT, 'lm')
rrect((DX + DW - 130, DY + 12, DX + DW - 18, DY + 38), 13, fill=(16, 185, 129, 50), outline=(16, 185, 129, 255), w=1)
text((DX + DW - 62, DY + 25), 'PASSED', F(14), (52, 211, 153), 'mm')
d.line([(s(DX + DW - 112), s(DY + 25)), (s(DX + DW - 108), s(DY + 29)), (s(DX + DW - 100), s(DY + 20))], fill=(52, 211, 153, 255), width=s(2.5), joint='curve')
# KPIs
kp = [('p95 LATENCY', '182 ms', CYAN), ('REQUESTS / SEC', '1,240', WHITE), ('ERROR RATE', '0.0%', (52, 211, 153))]
for i, (lab, val, col) in enumerate(kp):
    x = DX + 20 + i * 165
    rrect((x, DY + 58, x + 155, DY + 142), 12, fill=(24, 34, 68, 255), outline=LINE + (255,), w=1)
    text((x + 12, DY + 76), lab, F(11), MUT)
    text((x + 12, DY + 98), val, F(30), col)
# chart
cx0, cy0, cx1, cy1 = DX + 24, DY + 168, DX + DW - 24, DY + DH - 28
for i in range(4):
    y = cy0 + i * (cy1 - cy0) / 3; d.line((s(cx0), s(y), s(cx1), s(y)), fill=(255, 255, 255, 16), width=1)
text((cx0, cy0 - 14), 'Response time', F(13), MUT)
random.seed(7); pts = []
n = 60
for i in range(n + 1):
    t = i / n
    v = 0.62 - 0.25 * (1 - math.exp(-4 * t)) + 0.05 * math.sin(t * 24) + random.uniform(-0.035, 0.035)
    pts.append((cx0 + t * (cx1 - cx0), cy0 + 10 + v * (cy1 - cy0 - 10)))
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
P = [(s(x), s(y)) for x, y in pts]
ld.polygon(P + [(s(cx1), s(cy1)), (s(cx0), s(cy1))], fill=CYAN + (38,))
ld.line(P, fill=CYAN + (255,), width=s(3.5), joint='curve')
img = Image.alpha_composite(img.convert('RGBA'), lay.filter(ImageFilter.GaussianBlur(s(6)))); img = Image.alpha_composite(img, lay).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
ex, ey = pts[-1]; d.ellipse((s(ex - 7), s(ey - 7), s(ex + 7), s(ey + 7)), fill=WHITE, outline=CYAN + (255,), width=s(3))

# ---- workflow steps (bottom) ----
def docker(cx, cy, r):
    b = r * 0.32; x0 = cx - 1.5 * b; y0 = cy - 0.1 * r
    for row, cnt in ((0, 3), (-1, 2)):
        for j in range(cnt):
            xx = x0 + j * (b + 2) + (0 if row == 0 else b * 0.5); yy = y0 + row * (b + 2)
            d.rectangle((s(xx), s(yy), s(xx + b), s(yy + b)), fill=(255, 255, 255, 255))
    d.polygon([(s(cx - r * 0.95), s(cy + r * 0.05)), (s(cx + r * 0.9), s(cy + r * 0.05)), (s(cx + r * 0.6), s(cy + r * 0.62)), (s(cx - r * 0.55), s(cy + r * 0.62))], fill=(255, 255, 255, 255))
def chrome(cx, cy, r):
    box = (s(cx - r), s(cy - r), s(cx + r), s(cy + r))
    d.pieslice(box, 210, 330, fill=(234, 67, 53)); d.pieslice(box, 330, 450, fill=(251, 188, 5)); d.pieslice(box, 90, 210, fill=(52, 168, 83))
    d.ellipse((s(cx - r * .55), s(cy - r * .55), s(cx + r * .55), s(cy + r * .55)), fill=WHITE)
    d.ellipse((s(cx - r * .42), s(cy - r * .42), s(cx + r * .42), s(cy + r * .42)), fill=(66, 133, 244))
def k6(cx, cy, r):
    rrect((cx - r, cy - r, cx + r, cy + r), r * 0.28, fill=(125, 100, 255, 255)); text((cx, cy + 1), 'k6', F(r * 1.15), WHITE, 'mm')
steps = [('1', 'INSTALL', 'Docker', docker, (36, 150, 237)), ('2', 'CAPTURE', 'Chrome', chrome, (251, 188, 5)), ('3', 'LOAD TEST', 'k6', k6, (125, 100, 255))]
SY, SH, SWD, GAP = 520, 150, 350, 55
total = 3 * SWD + 2 * GAP; sx0 = (W - total) / 2 + 0
for i, (num, act, tool, icon, col) in enumerate(steps):
    x = 60 + i * (SWD + GAP)
    rrect((x, SY, x + SWD, SY + SH), 20, fill=PANEL + (255,), outline=col + (255,), w=3)
    d.ellipse((s(x + 20), s(SY + 24), s(x + 112), s(SY + 116)), fill=(255, 255, 255, 14), outline=LINE + (255,), width=s(2))
    icon(x + 66, SY + 70, 36)
    text((x + 128, SY + 52), f'{num}  {act}', F(28), WHITE, 'lm')
    text((x + 128, SY + 92), tool, F(26, False), col if tool != 'Chrome' else (253, 224, 71), 'lm')
    if i < 2:
        ax = x + SWD + 6; ay = SY + SH / 2
        d.line((s(ax - 6), s(ay), s(ax + 14), s(ay)), fill=CYAN + (255,), width=s(5))
        d.polygon([(s(ax + 10), s(ay - 13)), (s(ax + 32), s(ay)), (s(ax + 10), s(ay + 13))], fill=CYAN + (255,))

img.convert('RGB').resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
