"""Vector versions of the YouTube thumbnail (1280x720) and the 150x150 video watermark.
Run from this folder: python3 thumbnail_svg.py  (same layout/numbers as thumbnail.py)"""
import math, random
OUT = '../../assets/branding/'
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"; MONO = "Menlo, 'SF Mono', Consolas, monospace"
def mark(x, y, size):
    k = size / 32; f = lambda pts: ' '.join(f'{x + p * k:.1f},{y + q * k:.1f}' for p, q in pts)
    return (f'<g fill="none" stroke="#fff" stroke-width="{2.3 * k:.1f}" stroke-linecap="round" stroke-linejoin="round">'
            f'<polyline points="{f([(9.3, 9.3), (15.7, 16), (9.3, 22.7)])}"/><polyline points="{f([(17.6, 22.0), (24.6, 22.0)])}"/></g>')

# ---- watermark ----
open(OUT + 'perfload-video-watermark-150.svg', 'w').write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150" role="img" aria-label="PerfLoad"><rect width="150" height="150" rx="33" fill="#4f46e5"/>{mark(0, 0, 150)}</svg>\n')

# ---- thumbnail ----
o = []; a = o.append
def T(x, y, t, size, fill, family=SANS, weight=400, anchor='start', extra=''):
    t = t.replace('&', '&amp;').replace('<', '&lt;')
    a(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>')
CYAN, GREEN, MUT, PANEL, LINE = '#22d3ee', '#34d399', '#96a3be', '#0f162e', '#26345c'
a('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" role="img" aria-label="PerfLoad: your first load test. Install with Docker, capture with Chrome, load test with k6.">')
a('<defs><filter id="b170" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="170"/></filter><filter id="b6" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b22" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter></defs>')
a('<rect width="1280" height="720" fill="#080c1c"/>')
a('<g filter="url(#b170)" opacity="0.6"><ellipse cx="1100" cy="175" rx="400" ry="325" fill="#1e40af"/><ellipse cx="150" cy="600" rx="400" ry="300" fill="#4338ca"/></g>')
a('<g stroke="#fff" stroke-opacity="0.03">' + ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="720"/>' for x in range(0, 1280, 80)) + ''.join(f'<line x1="0" y1="{y}" x2="1280" y2="{y}"/>' for y in range(0, 720, 80)) + '</g>')
code = ['$ curl -X POST https://api.example.com/orders', '  -H "Authorization: Bearer $TOKEN"', '$ docker run -p 3000:3000 perfload', 'k6 run --vus 50 --duration 60s', '  ✓ status is 200', '  http_req_duration p(95)=182ms', '  checks.........: 100.00%', '$ _']
for i, ln in enumerate(code * 3): T(18, 8 + i * 27 + 12, ln, 15, '#1e2c58', MONO, extra='xml:space="preserve"')
a('<rect x="60" y="52" width="52" height="52" rx="12" fill="#4f46e5"/>' + mark(60, 52, 52))
T(128, 90, 'PerfLoad.io', 34, '#fff', weight=700)
T(58, 235, 'PERFLOAD', 112, '#fff', weight=700); T(62, 351, 'YOUR FIRST', 80, '#fff', weight=700); T(62, 438, 'LOAD TEST!', 80, CYAN, weight=700)
# dashboard
DX, DY, DW, DH = 700, 62, 530, 402
a(f'<rect x="{DX}" y="{DY + 14}" width="{DW}" height="{DH}" rx="18" fill="#000" fill-opacity="0.67" filter="url(#b22)"/><rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="18" fill="{PANEL}" stroke="#465a96" stroke-width="2"/>')
for i, c in enumerate(['#ff5f56', '#ffbd2e', '#27c93f']): a(f'<circle cx="{DX + 26 + i * 22}" cy="{DY + 24}" r="6" fill="{c}"/>')
T(DX + 100, DY + 29, 'load test results', 14, MUT, MONO)
a(f'<rect x="{DX + DW - 130}" y="{DY + 12}" width="112" height="26" rx="13" fill="#10b981" fill-opacity="0.2" stroke="#10b981"/><polyline points="{DX + DW - 112},{DY + 25} {DX + DW - 108},{DY + 29} {DX + DW - 100},{DY + 20}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
T(DX + DW - 62, DY + 30, 'PASSED', 14, GREEN, weight=700, anchor='middle')
for i, (lab, val, col) in enumerate([('p95 LATENCY', '182 ms', CYAN), ('REQUESTS / SEC', '1,240', '#fff'), ('ERROR RATE', '0.0%', GREEN)]):
    x = DX + 20 + i * 165
    a(f'<rect x="{x}" y="{DY + 58}" width="155" height="84" rx="12" fill="#182244" stroke="{LINE}"/>'); T(x + 12, DY + 85, lab, 11, MUT, weight=700); T(x + 12, DY + 123, val, 30, col, weight=700)
cx0, cy0, cx1, cy1 = DX + 24, DY + 168, DX + DW - 24, DY + DH - 28
for i in range(4): y = cy0 + i * (cy1 - cy0) / 3; a(f'<line x1="{cx0}" y1="{y:.0f}" x2="{cx1}" y2="{y:.0f}" stroke="#fff" stroke-opacity="0.06"/>')
T(cx0, cy0 - 3, 'Response time', 13, MUT, weight=700)
random.seed(7); pts = []
for i in range(61):
    t = i / 60; v = 0.62 - 0.25 * (1 - math.exp(-4 * t)) + 0.05 * math.sin(t * 24) + random.uniform(-0.035, 0.035)
    pts.append((round(cx0 + t * (cx1 - cx0), 1), round(cy0 + 10 + v * (cy1 - cy0 - 10), 1)))
dpath = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
a(f'<path d="{dpath} L{pts[-1][0]} {cy1} L{pts[0][0]} {cy1} Z" fill="{CYAN}" fill-opacity="0.15"/><path d="{dpath}" fill="none" stroke="{CYAN}" stroke-width="3.5" stroke-linejoin="round" filter="url(#b6)" opacity="0.8"/><path d="{dpath}" fill="none" stroke="{CYAN}" stroke-width="3.5" stroke-linejoin="round"/>')
a(f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="7" fill="#fff" stroke="{CYAN}" stroke-width="3"/>')
# steps
def docker(cx, cy, r):
    b = r * 0.32; x0 = cx - 1.5 * b; y0 = cy - 0.1 * r; out = []
    for row, cnt in ((0, 3), (-1, 2)):
        for j in range(cnt): out.append(f'<rect x="{x0 + j * (b + 2) + (0 if row == 0 else b * .5):.1f}" y="{y0 + row * (b + 2):.1f}" width="{b:.1f}" height="{b:.1f}" fill="#fff"/>')
    out.append(f'<polygon points="{cx - r * .95:.1f},{cy + r * .05:.1f} {cx + r * .9:.1f},{cy + r * .05:.1f} {cx + r * .6:.1f},{cy + r * .62:.1f} {cx - r * .55:.1f},{cy + r * .62:.1f}" fill="#fff"/>')
    return ''.join(out)
def pie(cx, cy, r, a0, a1, fill):
    p = lambda t: (cx + r * math.cos(math.radians(t)), cy + r * math.sin(math.radians(t)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    return f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{fill}"/>'
def chrome(cx, cy, r):
    return (pie(cx, cy, r, 210, 330, '#ea4335') + pie(cx, cy, r, 330, 450, '#fbbc05') + pie(cx, cy, r, 90, 210, '#34a853')
            + f'<circle cx="{cx}" cy="{cy}" r="{r * .55:.1f}" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r * .42:.1f}" fill="#4285f4"/>')
def k6(cx, cy, r):
    return f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" rx="{r * .28:.1f}" fill="#7d64ff"/><text x="{cx}" y="{cy + r * .4:.1f}" font-family="{SANS}" font-size="{r * 1.15:.1f}" font-weight="700" fill="#fff" text-anchor="middle">k6</text>'
SY, SH, SWD = 520, 150, 350
for i, (num, act, tool, icon, col, tcol) in enumerate([('1', 'INSTALL', 'Docker', docker, '#2496ed', '#2496ed'), ('2', 'CAPTURE', 'Chrome', chrome, '#fbbc05', '#fde047'), ('3', 'LOAD TEST', 'k6', k6, '#7d64ff', '#7d64ff')]):
    x = 60 + i * 405
    a(f'<rect x="{x}" y="{SY}" width="{SWD}" height="{SH}" rx="20" fill="{PANEL}" stroke="{col}" stroke-width="3"/><circle cx="{x + 66}" cy="{SY + 70}" r="46" fill="#fff" fill-opacity="0.055" stroke="{LINE}" stroke-width="2"/>')
    a(icon(x + 66, SY + 70, 36))
    T(x + 128, SY + 62, f'{num}  {act}', 28, '#fff', weight=700, extra='xml:space="preserve"'); T(x + 128, SY + 101, tool, 26, tcol)
    if i < 2:
        ax, ay = x + SWD + 6, SY + 75
        a(f'<line x1="{ax - 6}" y1="{ay}" x2="{ax + 14}" y2="{ay}" stroke="{CYAN}" stroke-width="5"/><polygon points="{ax + 10},{ay - 13} {ax + 32},{ay} {ax + 10},{ay + 13}" fill="{CYAN}"/>')
a('</svg>')
open(OUT + 'perfload-thumbnail-1280x720.svg', 'w').write('\n'.join(o) + '\n')
