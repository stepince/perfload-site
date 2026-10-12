"""YouTube video intro screen (1920x1080). Run from this folder: python3 intro.py
-> ../../assets/branding/perfload-intro-1920x1080.png"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '../../assets/branding/perfload-intro-1920x1080.png'
W, H, S = 1920, 1080, 2
NAVY = (7, 11, 26); PANEL = (14, 21, 44); LINE = (38, 52, 92)
BLUE = (59, 130, 246); CYAN = (34, 211, 238); TEAL = (45, 212, 191); IND = (79, 70, 229)
WHITE = (255, 255, 255); MUT = (150, 163, 190); GREEN = (52, 211, 153)
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
def F(sz, bold=True): return ImageFont.truetype(HN, round(sz * S), index=1 if bold else 0)
def MONO(sz): return ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', round(sz * S))
s = lambda v: round(v * S)

img = Image.new('RGB', (W * S, H * S), NAVY)
glow = Image.new('RGB', img.size, NAVY); g = ImageDraw.Draw(glow)
g.ellipse((s(1000), s(150), s(2200), s(1250)), fill=(26, 58, 160))
g.ellipse((s(-350), s(-250), s(900), s(650)), fill=(60, 50, 190))
g.ellipse((s(500), s(250), s(1400), s(650)), fill=(25, 45, 120))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(s(260))), 0.6)
d = ImageDraw.Draw(img, 'RGBA')
for x in range(0, W, 120): d.line((s(x), 0, s(x), s(H)), fill=(255, 255, 255, 7), width=1)
for y in range(0, H, 120): d.line((0, s(y), s(W), s(y)), fill=(255, 255, 255, 7), width=1)

# --- background: network graph, endpoint chips, terminal text (all kept dim) ---
random.seed(11)
nodes = [(random.uniform(0, W), random.uniform(0, H)) for _ in range(46)]
for i, a in enumerate(nodes):
    for b in nodes[i + 1:]:
        if math.dist(a, b) < 250:
            d.line((s(a[0]), s(a[1]), s(b[0]), s(b[1])), fill=(90, 120, 210, 34), width=s(1.5))
for x, y in nodes:
    d.ellipse((s(x - 4), s(y - 4), s(x + 4), s(y + 4)), fill=(110, 150, 240, 70))
term = ['$ curl -X POST https://api.example.com/orders', '  -H "Authorization: Bearer $TOKEN"', '$ docker run -p 3000:3000 perfload', '$ k6 run --vus 50 --duration 60s', '  ✓ status is 200', '  http_req_duration p(95)=182ms', '  checks.........: 100.00%']
for i, ln in enumerate(term):
    d.text((s(40), s(36 + i * 34)), ln, font=MONO(18), fill=(30, 44, 88))
for (x, y, t, c) in [(1450, 64, 'GET  /users  200', GREEN), (1620, 118, 'POST /orders  201', GREEN), (1380, 168, 'GET  /health  200', GREEN), (60, 640, 'PUT  /cart  200', GREEN)]:
    tw = d.textlength(t, font=MONO(17)) / S
    d.rounded_rectangle((s(x), s(y), s(x + tw + 28), s(y + 36)), radius=s(10), fill=(20, 30, 62, 200), outline=(50, 70, 130, 255), width=s(1.5))
    d.ellipse((s(x + 11), s(y + 14), s(x + 19), s(y + 22)), fill=c)
    d.text((s(x + 24), s(y + 18)), t, font=MONO(17), fill=(110, 130, 180), anchor='lm')

def rrect(box, r, fill=None, outline=None, w=1):
    d.rounded_rectangle([s(v) for v in box], radius=s(r), fill=fill, outline=outline, width=s(w))
def text(xy, t, font, fill, anchor='la'): d.text((s(xy[0]), s(xy[1])), t, font=font, fill=fill, anchor=anchor)
def mark(x, y, size, color=WHITE):
    k = size / 32
    for pts in ([(9.3, 9.3), (15.7, 16), (9.3, 22.7)], [(17.6, 22.0), (24.6, 22.0)]):
        P = [(s(x + a * k), s(y + b * k)) for a, b in pts]
        d.line(P, fill=color, width=round(2.3 * k * S), joint='curve')
        r = 1.15 * k * S
        for px, py in P: d.ellipse((px - r, py - r, px + r, py + r), fill=color)
def tracked(cx, y, t, font, fill, spacing):
    ws = [d.textlength(c, font=font) / S for c in t]; tot = sum(ws) + spacing * (len(t) - 1); x = cx - tot / 2
    for c, w in zip(t, ws): text((x, y), c, font, fill); x += w + spacing

# --- centre: logo tile, title, tagline, secondary ---
rrect((960 - 55, 120, 960 + 55, 230), 26, fill=IND + (255,)); mark(960 - 55, 120, 110)
text((960, 262), 'PERFLOAD', F(190), WHITE, 'ma')
text((960, 505), 'From cURL to Load Test.', F(50, False), (225, 232, 245), 'ma')
text((960, 568), 'Simple. Fast. Powerful.', F(50), CYAN, 'ma')
tracked(960, 650, 'API LOAD TESTING MADE SIMPLE', F(26), MUT, 5)

# --- flow: request -> engine -> metrics (bottom-left/centre) ---
FY, FH = 760, 190
def node(x, w, title, col):
    rrect((x, FY, x + w, FY + FH), 20, fill=PANEL + (255,), outline=col + (255,), w=3)
    text((x + 22, FY + 26), title, F(20), col)
def arrow(x0, x1, y):
    d.line((s(x0), s(y), s(x1 - 6), s(y)), fill=CYAN + (255,), width=s(5))
    d.polygon([(s(x1 - 22), s(y - 13)), (s(x1), s(y)), (s(x1 - 22), s(y + 13))], fill=CYAN + (255,))
    for k in range(1, 3): d.ellipse((s(x0 + k * (x1 - x0) / 3 - 5), s(y - 5), s(x0 + k * (x1 - x0) / 3 + 5), s(y + 5)), fill=WHITE + (255,))
n1, n2, n3, nw, ng = 90, 90 + 320 + 90, 90 + 2 * (320 + 90), 320, 90
node(n1, nw, 'API REQUEST', BLUE)
for i, ln in enumerate(['curl -X POST', "  api.example.com/orders", "  -d '{\"qty\": 1}'"]):
    text((n1 + 22, FY + 70 + i * 32), ln, MONO(19), (170, 195, 255))
node(n2, nw, 'PERFLOAD ENGINE', (125, 100, 255))
rrect((n2 + 22, FY + 66, n2 + 98, FY + 142), 18, fill=(125, 100, 255, 255)); text((n2 + 60, FY + 105), 'k6', F(44), WHITE, 'mm')
text((n2 + 116, FY + 84), '50 VUs', F(30), WHITE); text((n2 + 116, FY + 124), '60 seconds', F(22, False), MUT)
node(n3, nw, 'PERFORMANCE METRICS', GREEN)
for i, (k, v, c) in enumerate([('p95', '182 ms', CYAN), ('RPS', '1,240', WHITE), ('errors', '0.0%', GREEN)]):
    text((n3 + 22, FY + 66 + i * 38), k, F(20, False), MUT); text((n3 + 298, FY + 66 + i * 38), v, F(26), c, 'ra')
arrow(n1 + nw + 6, n2 - 8, FY + FH / 2); arrow(n2 + nw + 6, n3 - 8, FY + FH / 2)

# --- dashboard (right) ---
DX, DY, DW, DH = 1340, 470, 520, 540
sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((s(DX), s(DY + 16), s(DX + DW), s(DY + DH + 16)), radius=s(22), fill=(0, 0, 0, 170))
img = Image.alpha_composite(img.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(s(26)))).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
rrect((DX, DY, DX + DW, DY + DH), 22, fill=PANEL + (255,), outline=(70, 90, 150, 255), w=2)
for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
    d.ellipse((s(DX + 22 + i * 24), s(DY + 20), s(DX + 36 + i * 24), s(DY + 34)), fill=c)
text((DX + 112, DY + 27), 'perfload · live run', MONO(16), MUT, 'lm')
rrect((DX + DW - 126, DY + 14, DX + DW - 20, DY + 42), 14, fill=(16, 185, 129, 50), outline=(16, 185, 129, 255), w=1.5)
text((DX + DW - 73, DY + 28), '● RUNNING', F(13), GREEN, 'mm')
for i, (lab, val, col) in enumerate([('p95 LATENCY', '182 ms', CYAN), ('THROUGHPUT', '1,240/s', WHITE), ('VIRTUAL USERS', '50', TEAL)]):
    x = DX + 22 + i * 160
    rrect((x, DY + 62, x + 148, DY + 148), 12, fill=(24, 34, 68, 255), outline=LINE + (255,), w=1)
    text((x + 12, DY + 78), lab, F(11), MUT); text((x + 12, DY + 100), val, F(28), col)
def chart(y0, y1, color, seed, label, base, amp, slope):
    cx0, cx1 = DX + 24, DX + DW - 24
    text((cx0, y0 - 10), label, F(13), MUT)
    for i in range(3):
        y = y0 + 10 + i * (y1 - y0 - 10) / 2; d.line((s(cx0), s(y), s(cx1), s(y)), fill=(255, 255, 255, 16), width=1)
    random.seed(seed); pts = []
    for i in range(61):
        t = i / 60
        v = base + slope * (1 - math.exp(-4 * t)) + amp * math.sin(t * 22 + seed) + random.uniform(-amp, amp) * 0.6
        pts.append((cx0 + t * (cx1 - cx0), y0 + 10 + v * (y1 - y0 - 10)))
    return pts, color, y1
curves = [chart(DY + 190, DY + 330, CYAN, 7, 'Response time', 0.55, 0.04, -0.2), chart(DY + 380, DY + 515, TEAL, 3, 'Requests / sec', 0.85, 0.03, -0.45)]
lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
for pts, col, y1 in curves:
    P = [(s(x), s(y)) for x, y in pts]
    ld.polygon(P + [(s(pts[-1][0]), s(y1)), (s(pts[0][0]), s(y1))], fill=col + (36,))
    ld.line(P, fill=col + (255,), width=s(4), joint='curve')
img = Image.alpha_composite(img.convert('RGBA'), lay.filter(ImageFilter.GaussianBlur(s(7)))); img = Image.alpha_composite(img, lay).convert('RGB'); d = ImageDraw.Draw(img, 'RGBA')
for pts, col, _ in curves:
    ex, ey = pts[-1]; d.ellipse((s(ex - 7), s(ey - 7), s(ex + 7), s(ey + 7)), fill=WHITE + (255,), outline=col + (255,), width=s(3))

# --- url ---
text((90, 1010), 'perfload.io', F(34), WHITE, 'lm')
d.rounded_rectangle((s(90), s(1032), s(90 + 70), s(1036)), radius=s(2), fill=CYAN + (255,))
img.convert('RGB').resize((W, H), Image.LANCZOS).save(OUT, optimize=True)
