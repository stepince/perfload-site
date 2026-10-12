"""YouTube thumbnail 3 (1280x720): "AI runs my load tests!" - Claude in Chrome -> AI Skills + REST API -> PerfLoad.
Run from this folder: python3 thumbnail_ai.py -> ../../assets/branding/perfload-thumbnail-ai-1280x720.png
The Claude and Chrome marks are simplified drawings, not the official logos."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '../../assets/branding/perfload-thumbnail-ai-1280x720.png'
W, H, S = 1280, 720, 2
NAVY = (8, 12, 28); PANEL = (15, 22, 46); LINE = (38, 52, 92)
CYAN = (34, 211, 238); TEAL = (45, 212, 191); IND = (79, 70, 229)
WHITE = (255, 255, 255); MUT = (150, 163, 190); GREEN = (52, 211, 153); CLAUDE = (217, 119, 87)
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
def F(sz, bold=True): return ImageFont.truetype(HN, round(sz * S), index=1 if bold else 0)
def MONO(sz): return ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', round(sz * S))
s = lambda v: round(v * S)

img = Image.new('RGB', (W * S, H * S), NAVY)
glow = Image.new('RGB', img.size, NAVY); g = ImageDraw.Draw(glow)
g.ellipse((s(500), s(250), s(1500), s(900)), fill=(30, 64, 175)); g.ellipse((s(-250), s(-200), s(650), s(450)), fill=(67, 56, 202)); g.ellipse((s(350), s(380), s(800), s(700)), fill=(14, 100, 130))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(s(170))), 0.6)
d = ImageDraw.Draw(img, 'RGBA')
for x in range(0, W, 80): d.line((s(x), 0, s(x), s(H)), fill=(255, 255, 255, 7), width=1)
for y in range(0, H, 80): d.line((0, s(y), s(W), s(y)), fill=(255, 255, 255, 7), width=1)
for i, ln in enumerate(['> Run a load test on /orders', '  100 users for 60 seconds', '$ curl -X POST localhost:3000/...', '  -H "Content-Type: application/json"', '  skills/workbench.md loaded', '  http_req_duration p(95)=182ms', '  checks.........: 100.00%', '  ✓ run complete'] * 4):
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
def claude(cx, cy, r):   # simplified starburst
    L = [1, .72, .95, .68, 1, .75, .92, .7, .98, .72, .9, .68]
    for i, l in enumerate(L):
        a = math.radians(i * 30 - 90); x1, y1 = cx + math.cos(a) * r * l, cy + math.sin(a) * r * l
        d.line((s(cx), s(cy), s(x1), s(y1)), fill=CLAUDE + (255,), width=s(r * 0.26))
        d.ellipse((s(x1 - r * .13), s(y1 - r * .13), s(x1 + r * .13), s(y1 + r * .13)), fill=CLAUDE + (255,))
    d.ellipse((s(cx - r * .2), s(cy - r * .2), s(cx + r * .2), s(cy + r * .2)), fill=CLAUDE + (255,))
def chrome(cx, cy, r):
    box = (s(cx - r), s(cy - r), s(cx + r), s(cy + r))
    d.pieslice(box, 210, 330, fill=(234, 67, 53)); d.pieslice(box, 330, 450, fill=(251, 188, 5)); d.pieslice(box, 90, 210, fill=(52, 168, 83))
    d.ellipse((s(cx - r * .55), s(cy - r * .55), s(cx + r * .55), s(cy + r * .55)), fill=WHITE); d.ellipse((s(cx - r * .42), s(cy - r * .42), s(cx + r * .42), s(cy + r * .42)), fill=(66, 133, 244))
def composite(layer, blur=0, passes=1):
    global img, d
    if blur: img = Image.alpha_composite(img.convert('RGBA'), layer.filter(ImageFilter.GaussianBlur(s(blur))))
    else: img = img.convert('RGBA')
    for _ in range(passes): img = Image.alpha_composite(img, layer)
    img = img.convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
def window(x0, y0, x1, y1, outline=(70, 90, 150), glow_col=None):
    global img, d
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((s(x0), s(y0 + 12), s(x1), s(y1 + 12)), radius=s(18), fill=(0, 0, 0, 170))
    composite(sh, 20, 0) if False else None
    img = Image.alpha_composite(img.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(s(20)))).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
    rrect((x0, y0, x1, y1), 18, fill=PANEL + (255,), outline=outline + (255,), w=2)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse((s(x0 + 18 + i * 20), s(y0 + 16), s(x0 + 28 + i * 20), s(y0 + 26)), fill=c)

# ---- headline (top-left) ----
sz = fit('LOAD TESTS!', 700)
text((58, 62), 'AI RUNS MY', F(sz), WHITE); text((62, 62 + sz * 1.03), 'LOAD TESTS!', F(sz), CYAN)
# ---- brand + secondary (top-right) ----
rrect((850, 58, 910, 118), 15, fill=IND); mark(850, 58, 60)
text((928, 88), 'PERFLOAD', F(42), WHITE, 'lm')
claude(868, 168, 20); text((900, 168), 'Claude + PerfLoad', F(34), CYAN, 'lm')
text((852, 214), 'perfload.io', F(26), MUT, 'lm'); d.rounded_rectangle((s(852), s(232), s(902), s(235)), radius=s(2), fill=CYAN + (255,))

# ---- 1: Claude in Chrome ----
N1 = (60, 372, 390, 650)
window(*N1); x0, y0, x1, y1 = N1
rrect((x0 + 90, y0 + 11, x1 - 50, y0 + 31), 10, fill=(24, 34, 68, 255)); text(((x0 + 90 + x1 - 50) / 2, y0 + 21), 'claude.ai', F(13, False), MUT, 'mm')
chrome(x1 - 28, y0 + 21, 11)
claude(x0 + 38, y0 + 74, 20); text((x0 + 68, y0 + 74), 'Claude', F(22), WHITE, 'lm')
rrect((x0 + 20, y0 + 112, x1 - 20, y0 + 190), 14, fill=(30, 44, 88, 255))
text((x0 + 36, y0 + 134), 'Run a load test on /orders', F(18), WHITE, 'lm'); text((x0 + 36, y0 + 164), '100 users for 60 seconds', F(18, False), (170, 195, 255), 'lm')
rrect((x0 + 20, y0 + 208, x1 - 20, y0 + 250), 21, fill=(34, 211, 238, 28), outline=CYAN + (255,), w=1.5)
for i in range(3): d.ellipse((s(x0 + 40 + i * 14), s(y0 + 226), s(x0 + 48 + i * 14), s(y0 + 234)), fill=CYAN + (255 - i * 70,))
text((x0 + 92, y0 + 229), 'Running the test…', F(17), CYAN, 'lm')

# ---- 3: PerfLoad dashboard ----
N3 = (740, 372, 1230, 650)
window(*N3, outline=(34, 211, 238)); x0, y0, x1, y1 = N3
text((x0 + 90, y0 + 21), 'perfload', MONO(14), MUT, 'lm')
rrect((x1 - 150, y0 + 8, x1 - 18, y0 + 34), 13, fill=(16, 185, 129, 50), outline=(16, 185, 129, 255), w=1)
d.line([(s(x1 - 138), s(y0 + 21)), (s(x1 - 133), s(y0 + 26)), (s(x1 - 124), s(y0 + 16))], fill=GREEN + (255,), width=s(2.5), joint='curve')
text((x1 - 70, y0 + 21), 'COMPLETED', F(13), GREEN, 'mm')
for i, (lab, val, col) in enumerate([('p95 LATENCY', '182 ms', CYAN), ('REQUESTS / SEC', '1,240', WHITE), ('ERROR RATE', '0.0%', GREEN)]):
    x = x0 + 18 + i * 153
    rrect((x, y0 + 52, x + 143, y0 + 120), 12, fill=(24, 34, 68, 255), outline=LINE + (255,), w=1)
    text((x + 12, y0 + 66), lab, F(11), MUT); text((x + 12, y0 + 84), val, F(28), col)
cx0, cx1, cy0, cy1 = x0 + 22, x1 - 22, y0 + 160, y1 - 20
for i in range(3): yy = cy0 + i * (cy1 - cy0) / 2; d.line((s(cx0), s(yy), s(cx1), s(yy)), fill=(255, 255, 255, 16), width=1)
text((cx0, cy0 - 18), 'Response time', F(13), MUT)
random.seed(7); pts = []
for i in range(61):
    t = i / 60; v = 0.62 - 0.25 * (1 - math.exp(-4 * t)) + 0.05 * math.sin(t * 24) + random.uniform(-0.035, 0.035)
    pts.append((cx0 + t * (cx1 - cx0), cy0 + 6 + v * (cy1 - cy0 - 6)))
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); P = [(s(a), s(b)) for a, b in pts]
ld.polygon(P + [(s(cx1), s(cy1)), (s(cx0), s(cy1))], fill=CYAN + (38,)); ld.line(P, fill=CYAN + (255,), width=s(3.5), joint='curve')
composite(lay, 6, 1)
ex, ey = pts[-1]; d.ellipse((s(ex - 7), s(ey - 7), s(ex + 7), s(ey + 7)), fill=WHITE + (255,), outline=CYAN + (255,), width=s(3))

# ---- 2: AI Skills + REST API (glowing link) ----
C = (440, 440, 690, 582)
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
for xa, xb in [(392, 432), (690, 734)]:
    ld.line((s(xa), s(511), s(xb), s(511)), fill=CYAN + (255,), width=s(6))
    ld.polygon([(s(xb - 4), s(511 - 14)), (s(xb + 14), s(511)), (s(xb - 4), s(511 + 14))], fill=CYAN + (255,))
ld.rounded_rectangle([s(v) for v in C], radius=s(20), outline=CYAN + (255,), width=s(5))
composite(lay, 12, 1)
rrect(C, 20, fill=PANEL + (255,), outline=CYAN + (255,), w=3)
text((565, C[1] + 30), 'AI SKILLS', F(24), WHITE, 'mm'); text((565, C[1] + 54), 'workbench.md', MONO(14), MUT, 'mm')
d.line((s(C[0] + 24), s(C[1] + 72), s(C[2] - 24), s(C[1] + 72)), fill=LINE + (255,), width=s(1.5))
text((565, C[1] + 98), 'REST API', F(24), CYAN, 'mm'); text((565, C[1] + 122), 'run · results', MONO(14), MUT, 'mm')
for xa, xb in [(392, 440), (690, 738)]: d.ellipse((s((xa + xb) / 2 - 5), s(506), s((xa + xb) / 2 + 5), s(516)), fill=WHITE + (255,))

# ---- captions ----
for xc, t in [(225, 'CLAUDE IN CHROME'), (565, 'AI SKILLS + REST API'), (985, 'PERFLOAD')]: text((xc, 678), t, F(17), MUT, 'mm')
img.convert('RGB').resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
