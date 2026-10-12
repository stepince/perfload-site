"""Vector version of the 1920x1080 intro screen. Run from this folder: python3 intro_svg.py
-> ../../assets/branding/perfload-intro-1920x1080.svg  (same layout/numbers as intro.py)"""
import math, random
OUT = '../../assets/branding/perfload-intro-1920x1080.svg'
W, H = 1920, 1080
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"; MONO = "Menlo, 'SF Mono', Consolas, monospace"
o = []; a = o.append
def T(x, y, t, size, fill, family=SANS, weight=400, anchor='start', extra=''):
    t = t.replace('&', '&amp;').replace('<', '&lt;')
    a(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>')
def mark(x, y, size):
    k = size / 32; f = lambda pts: ' '.join(f'{x + p * k:.1f},{y + q * k:.1f}' for p, q in pts)
    return (f'<g fill="none" stroke="#fff" stroke-width="{2.3 * k:.1f}" stroke-linecap="round" stroke-linejoin="round">'
            f'<polyline points="{f([(9.3, 9.3), (15.7, 16), (9.3, 22.7)])}"/><polyline points="{f([(17.6, 22.0), (24.6, 22.0)])}"/></g>')

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="PerfLoad: From cURL to Load Test. Simple. Fast. Powerful.">')
a('''<defs>
<filter id="b130" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="130"/></filter>
<filter id="b7" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="b26" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="26"/></filter>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="#070b1a"/>')
a('<g filter="url(#b130)" opacity="0.6"><ellipse cx="1600" cy="700" rx="600" ry="550" fill="#1a3aa0"/><ellipse cx="275" cy="200" rx="625" ry="450" fill="#3c32be"/><ellipse cx="950" cy="450" rx="450" ry="200" fill="#192d78"/></g>')
a('<g stroke="#fff" stroke-opacity="0.03">' + ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 120)) + ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 120)) + '</g>')
# network
random.seed(11); nodes = [(random.uniform(0, W), random.uniform(0, H)) for _ in range(46)]
ln = []; 
for i, p in enumerate(nodes):
    for q in nodes[i + 1:]:
        if math.dist(p, q) < 250: ln.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}"/>')
a('<g stroke="#5a78d2" stroke-opacity="0.13" stroke-width="1.5">' + ''.join(ln) + '</g>')
a('<g fill="#6e96f0" fill-opacity="0.27">' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4"/>' for x, y in nodes) + '</g>')
for i, t in enumerate(['$ curl -X POST https://api.example.com/orders', '  -H "Authorization: Bearer $TOKEN"', '$ docker run -p 3000:3000 perfload', '$ k6 run --vus 50 --duration 60s', '  ✓ status is 200', '  http_req_duration p(95)=182ms', '  checks.........: 100.00%']):
    T(40, 36 + i * 34 + 14, t, 18, '#1e2c58', MONO, extra='xml:space="preserve"')
for x, y, t in [(1450, 64, 'GET  /users  200'), (1620, 118, 'POST /orders  201'), (1380, 168, 'GET  /health  200'), (60, 640, 'PUT  /cart  200')]:
    w = len(t) * 10.2 + 28
    a(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="36" rx="10" fill="#141e3e" fill-opacity="0.8" stroke="#324682" stroke-width="1.5"/><circle cx="{x + 15}" cy="{y + 18}" r="4" fill="#34d399"/>')
    T(x + 24, y + 24, t, 17, '#6e82b4', MONO, extra='xml:space="preserve"')
# centre
a(f'<rect x="905" y="120" width="110" height="110" rx="26" fill="#4f46e5"/>' + mark(905, 120, 110))
T(960, 420, 'PERFLOAD', 190, '#fff', weight=700, anchor='middle')
T(960, 560, 'From cURL to Load Test.', 50, '#e1e8f5', anchor='middle')
T(960, 622, 'Simple. Fast. Powerful.', 50, '#22d3ee', weight=700, anchor='middle')
T(970, 676, 'API LOAD TESTING MADE SIMPLE', 26, '#96a3be', weight=700, anchor='middle', extra='letter-spacing="5"')
# flow
FY, FH, nw = 760, 190, 320; n1, n2, n3 = 90, 500, 910
def node(x, title, col): a(f'<rect x="{x}" y="{FY}" width="{nw}" height="{FH}" rx="20" fill="#0e152c" stroke="{col}" stroke-width="3"/>'); T(x + 22, FY + 42, title, 20, col, weight=700)
node(n1, 'API REQUEST', '#3b82f6')
for i, t in enumerate(['curl -X POST', '  api.example.com/orders', '  -d \'{"qty": 1}\'']): T(n1 + 22, FY + 88 + i * 32, t, 19, '#aac3ff', MONO, extra='xml:space="preserve"')
node(n2, 'PERFLOAD ENGINE', '#7d64ff')
a(f'<rect x="{n2 + 22}" y="{FY + 66}" width="76" height="76" rx="18" fill="#7d64ff"/>'); T(n2 + 60, FY + 120, 'k6', 44, '#fff', weight=700, anchor='middle')
T(n2 + 116, FY + 112, '50 VUs', 30, '#fff', weight=700); T(n2 + 116, FY + 140, '60 seconds', 22, '#96a3be')
node(n3, 'PERFORMANCE METRICS', '#34d399')
for i, (k, v, c) in enumerate([('p95', '182 ms', '#22d3ee'), ('RPS', '1,240', '#fff'), ('errors', '0.0%', '#34d399')]):
    T(n3 + 22, FY + 80 + i * 38, k, 20, '#96a3be'); T(n3 + 298, FY + 82 + i * 38, v, 26, c, weight=700, anchor='end')
for x0, x1 in [(n1 + nw + 6, n2 - 8), (n2 + nw + 6, n3 - 8)]:
    y = FY + FH / 2
    a(f'<line x1="{x0}" y1="{y}" x2="{x1 - 6}" y2="{y}" stroke="#22d3ee" stroke-width="5"/><polygon points="{x1 - 22},{y - 13} {x1},{y} {x1 - 22},{y + 13}" fill="#22d3ee"/>')
    for k in (1, 2): a(f'<circle cx="{x0 + k * (x1 - x0) / 3:.0f}" cy="{y}" r="5" fill="#fff"/>')
# dashboard
DX, DY, DW, DH = 1340, 470, 520, 540
a(f'<rect x="{DX}" y="{DY + 16}" width="{DW}" height="{DH}" rx="22" fill="#000" fill-opacity="0.67" filter="url(#b26)"/>')
a(f'<rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="22" fill="#0e152c" stroke="#465a96" stroke-width="2"/>')
for i, c in enumerate(['#ff5f56', '#ffbd2e', '#27c93f']): a(f'<circle cx="{DX + 29 + i * 24}" cy="{DY + 27}" r="7" fill="{c}"/>')
T(DX + 112, DY + 32, 'perfload · live run', 16, '#96a3be', MONO)
a(f'<rect x="{DX + DW - 126}" y="{DY + 14}" width="106" height="28" rx="14" fill="#10b981" fill-opacity="0.2" stroke="#10b981" stroke-width="1.5"/>'); T(DX + DW - 73, DY + 33, '● RUNNING', 13, '#34d399', weight=700, anchor='middle')
for i, (lab, val, col) in enumerate([('p95 LATENCY', '182 ms', '#22d3ee'), ('THROUGHPUT', '1,240/s', '#fff'), ('VIRTUAL USERS', '50', '#2dd4bf')]):
    x = DX + 22 + i * 160
    a(f'<rect x="{x}" y="{DY + 62}" width="148" height="86" rx="12" fill="#182244" stroke="#26345c"/>'); T(x + 12, DY + 90, lab, 11, '#96a3be', weight=700); T(x + 12, DY + 126, val, 28, col, weight=700)
def chart(y0, y1, col, seed, label, base, amp, slope):
    cx0, cx1 = DX + 24, DX + DW - 24
    T(cx0, y0 - 2, label, 13, '#96a3be', weight=700)
    for i in range(3): a(f'<line x1="{cx0}" y1="{y0 + 10 + i * (y1 - y0 - 10) / 2:.0f}" x2="{cx1}" y2="{y0 + 10 + i * (y1 - y0 - 10) / 2:.0f}" stroke="#fff" stroke-opacity="0.06"/>')
    random.seed(seed); pts = []
    for i in range(61):
        t = i / 60; v = base + slope * (1 - math.exp(-4 * t)) + amp * math.sin(t * 22 + seed) + random.uniform(-amp, amp) * 0.6
        pts.append((round(cx0 + t * (cx1 - cx0), 1), round(y0 + 10 + v * (y1 - y0 - 10), 1)))
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    a(f'<path d="{d} L{pts[-1][0]} {y1} L{pts[0][0]} {y1} Z" fill="{col}" fill-opacity="0.14"/>')
    a(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" filter="url(#b7)" opacity="0.8"/><path d="{d}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round"/>')
    a(f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="7" fill="#fff" stroke="{col}" stroke-width="3"/>')
chart(DY + 190, DY + 330, '#22d3ee', 7, 'Response time', 0.55, 0.04, -0.2)
chart(DY + 380, DY + 515, '#2dd4bf', 3, 'Requests / sec', 0.85, 0.03, -0.45)
T(90, 1022, 'perfload.io', 34, '#fff', weight=700); a('<rect x="90" y="1032" width="70" height="4" rx="2" fill="#22d3ee"/>')
a('</svg>')
open(OUT, 'w').write('\n'.join(o) + '\n')
