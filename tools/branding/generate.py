"""Regenerates the PerfLoad branding images in assets/branding/ from the favicon's
terminal-prompt mark (white ">_" on indigo). Run from this folder: python3 generate.py"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = '../../assets/branding/'
ACC = (79, 70, 229); LIGHT = (129, 140, 248); TXT = (232, 234, 240); MUT = (154, 160, 174); BG = (11, 13, 20)
# Prompt geometry on the favicon's 32x32 grid.
CHEV = [(9.3, 9.3), (15.7, 16), (9.3, 22.7)]
UNDER = [(17.6, 22.0), (24.6, 22.0)]
SW = 2.3

def mark(d, ox, oy, size, color=(255, 255, 255, 255)):
    k = size / 32.0
    def seg(pts):
        P = [(ox + x * k, oy + y * k) for x, y in pts]
        d.line(P, fill=color, width=round(SW * k), joint='curve')
        r = SW * k / 2
        for x, y in P: d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    seg(CHEV); seg(UNDER)

def svg_mark(ox, oy, size):
    k = size / 32.0
    f = lambda pts: ' '.join(f'{ox + x * k:.1f},{oy + y * k:.1f}' for x, y in pts)
    return (f'<g fill="none" stroke="#fff" stroke-width="{SW * k:.1f}" stroke-linecap="round" stroke-linejoin="round">'
            f'<polyline points="{f(CHEV)}"/><polyline points="{f(UNDER)}"/></g>')

FONT = '/System/Library/Fonts/HelveticaNeue.ttc'

# ---------- profile (800x800, full-bleed so YouTube's circle crop stays clean) ----------
S = 4; N = 800 * S
im = Image.new('RGB', (N, N), ACC); d = ImageDraw.Draw(im, 'RGBA')
mark(d, N * 0.5 - N * 0.5, N * 0.5 - N * 0.5, N)   # favicon grid maps 1:1 onto the canvas
im.resize((800, 800), Image.LANCZOS).save(OUT + 'perfload-profile-800.png', optimize=True)
open(OUT + 'perfload-profile.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" role="img" aria-label="PerfLoad">'
    f'<rect width="800" height="800" fill="#4f46e5"/>{svg_mark(0, 0, 800)}</svg>\n')

# ---------- banner (2560x1440) ----------
W, H = 2560, 1440
def series(base, amp, seed, ramp):
    random.seed(seed); pts = []
    for i in range(0, W + 1, 16):
        t = i / W
        y = base - ramp * (1 - math.exp(-3 * t)) + amp * math.sin(t * 38 + seed) * (0.4 + t) + random.uniform(-amp, amp) * 0.4
        pts.append((i, round(y, 1)))
    return pts
A = series(H * 0.90, 26, 1, H * 0.12); B = series(H * 0.96, 22, 5, H * 0.08)
MS = 190                      # mark size
TITLE = 210
gap = 48
f1 = ImageFont.truetype(FONT, TITLE, index=1)
tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('PerfLoad', font=f1)
row_w = MS + gap + tw; rx0 = (W - row_w) / 2; ry = 545

SS = 2
big = Image.new('RGB', (W * SS, H * SS), BG)
glow = Image.new('RGB', big.size, BG); ImageDraw.Draw(glow).ellipse((W * SS * .5 - 1500 * SS, H * SS * .5 - 700 * SS, W * SS * .5 + 1500 * SS, H * SS * .5 + 700 * SS), fill=(40, 36, 120))
big = Image.blend(big, glow.filter(ImageFilter.GaussianBlur(500 * SS)), 0.55)
d = ImageDraw.Draw(big, 'RGBA')
for x in range(0, W, 160): d.line((x * SS, 0, x * SS, H * SS), fill=(255, 255, 255, 10), width=2)
for y in range(0, H, 160): d.line((0, y * SS, W * SS, y * SS), fill=(255, 255, 255, 10), width=2)
layer = Image.new('RGBA', big.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
for pts, col, wd in [(A, LIGHT + (150,), 7), (B, ACC + (170,), 6)]:
    P = [(x * SS, y * SS) for x, y in pts]
    ld.polygon(P + [(W * SS, H * SS), (0, H * SS)], fill=col[:3] + (22,))
    ld.line(P, fill=col, width=wd * SS, joint='curve')
big = Image.alpha_composite(big.convert('RGBA'), layer.filter(ImageFilter.GaussianBlur(14 * SS)))
big = Image.alpha_composite(big, layer)
d = ImageDraw.Draw(big, 'RGBA')
# favicon tile + wordmark
d.rounded_rectangle((rx0 * SS, ry * SS, (rx0 + MS) * SS, (ry + MS) * SS), radius=MS * 0.22 * SS, fill=ACC + (255,))
mark(d, rx0 * SS, ry * SS, MS * SS)
d.text(((rx0 + MS + gap) * SS, (ry + MS / 2) * SS), 'PerfLoad', font=ImageFont.truetype(FONT, TITLE * SS, index=1), fill=TXT, anchor='lm')
# tagline with slashed "script"
f2 = ImageFont.truetype(FONT, 78 * SS, index=0)
parts = ['No ', 'script', ' HTTP load testing']
ws = [d.textlength(p, font=f2) / SS for p in parts]; x = (W - sum(ws)) / 2; ty = 790
for p, w in zip(parts, ws):
    d.text((x * SS, ty * SS), p, font=f2, fill=MUT)
    if p == 'script':
        cx, cy, rx, ry2 = x + w / 2, ty + 52, w / 2 + 14, 62
        d.ellipse(((cx - rx) * SS, (cy - ry2) * SS, (cx + rx) * SS, (cy + ry2) * SS), outline=ACC, width=8 * SS)
        d.line(((cx - rx * .75) * SS, (cy + ry2 * .8) * SS, (cx + rx * .75) * SS, (cy - ry2 * .8) * SS), fill=ACC, width=8 * SS)
    x += w
big.convert('RGB').resize((W, H), Image.LANCZOS).save(OUT + 'perfload-youtube-banner.png', optimize=True)

# banner SVG
path = lambda p: 'M' + ' L'.join(f'{x} {y}' for x, y in p)
grid = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 160)) + ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 160))
tcx = (W - sum(ws)) / 2   # tagline left edge
sx = tcx + ws[0] + ws[1] / 2
open(OUT + 'perfload-youtube-banner.svg', 'w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="PerfLoad: no script HTTP load testing">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="60%"><stop offset="0" stop-color="#28247a" stop-opacity="0.75"/><stop offset="1" stop-color="#0b0d14" stop-opacity="0"/></radialGradient>
    <filter id="blur" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>
  <rect width="{W}" height="{H}" fill="#0b0d14"/><rect width="{W}" height="{H}" fill="url(#glow)"/>
  <g stroke="#fff" stroke-opacity="0.04" stroke-width="2">{grid}</g>
  <g fill="none" stroke-linejoin="round" stroke-linecap="round">
    <path d="{path(A)} L{W} {H} L0 {H} Z" fill="#818cf8" fill-opacity="0.09" stroke="none"/>
    <path d="{path(B)} L{W} {H} L0 {H} Z" fill="#4f46e5" fill-opacity="0.09" stroke="none"/>
    <g filter="url(#blur)"><path d="{path(A)}" stroke="#818cf8" stroke-opacity="0.6" stroke-width="7"/><path d="{path(B)}" stroke="#4f46e5" stroke-opacity="0.65" stroke-width="6"/></g>
    <path d="{path(A)}" stroke="#818cf8" stroke-opacity="0.6" stroke-width="7"/><path d="{path(B)}" stroke="#4f46e5" stroke-opacity="0.7" stroke-width="6"/>
  </g>
  <rect x="{rx0:.1f}" y="{ry}" width="{MS}" height="{MS}" rx="{MS * .22:.1f}" fill="#4f46e5"/>
  {svg_mark(rx0, ry, MS)}
  <g font-family="'Helvetica Neue', Helvetica, Arial, sans-serif">
    <text x="{rx0 + MS + gap:.1f}" y="{ry + MS / 2 + 72:.1f}" font-size="{TITLE}" font-weight="700" fill="#e8eaf0">PerfLoad</text>
    <text x="{W / 2}" y="{ty + 72}" text-anchor="middle" font-size="78" fill="#9aa0ae" xml:space="preserve">No script HTTP load testing</text>
  </g>
  <g fill="none" stroke="#4f46e5" stroke-width="8" stroke-linecap="round">
    <ellipse cx="{sx:.1f}" cy="{ty + 52}" rx="{ws[1] / 2 + 14:.1f}" ry="62"/>
    <line x1="{sx - (ws[1] / 2 + 14) * .75:.1f}" y1="{ty + 52 + 50}" x2="{sx + (ws[1] / 2 + 14) * .75:.1f}" y2="{ty + 52 - 50}"/>
  </g>
</svg>
''')

# ---------- YouTube video watermark (150x150, transparent corners) ----------
WS = 8; WN = 150 * WS
wm = Image.new('RGBA', (WN, WN), (0, 0, 0, 0)); d = ImageDraw.Draw(wm)
d.rounded_rectangle((0, 0, WN - 1, WN - 1), radius=WN * 0.22, fill=ACC + (255,))
mark(d, 0, 0, WN)
wm.resize((150, 150), Image.LANCZOS).save(OUT + 'perfload-video-watermark-150.png', optimize=True)
