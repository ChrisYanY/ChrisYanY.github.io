# Generates article covers (assets/covers/<slug>.svg) and the static homepage accent.
# Usage: python3 scripts/covers.py assets/covers /tmp/accent-static.svg
# To add a cover for a new post: write a function returning svg(...) and add (slug, fn) to the list at the bottom.
#
# Covers are loaded via <img>, so scripts don't run inside them; all motion is CSS keyframes
# embedded in each SVG. Keep it slow and quiet, and honour prefers-reduced-motion.

import math, random, sys, pathlib
OUT = pathlib.Path(sys.argv[1])
INK, MUTED, FAINT, LINE, ACC, ACC2 = "#16181b", "#5a6068", "#9aa0a6", "#d6d6d2", "#2B547E", "#7b8794"
PAPER = "#e8e8e5"
W, H = 800, 500

BASE_CSS = """
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes flow10 { to { stroke-dashoffset: -20; } }
@keyframes flow11 { to { stroke-dashoffset: -22; } }
"""

def svg(body, css=""):
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-hidden="true">'
    style = f'<style>{BASE_CSS}{css}</style>'
    base = f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
    # faint engineering grid
    grid = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{LINE}" stroke-width="1"/>' for x in range(40, W, 40))
    grid += ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{LINE}" stroke-width="1"/>' for y in range(40, H, 40))
    return head + style + base + f'<g opacity=".55">{grid}</g>' + body + '</svg>'

def diffusion():
    # a wave of denoising sweeps left to right: noise collapses onto a band, then dissolves again
    r = random.Random(7); out = []
    cols, rows = 26, 14
    for i in range(cols):
        for j in range(rows):
            gx = 70 + i*25; gy = 85 + j*25
            on = abs((j-rows/2) - 4*math.sin(i/3.2)) < 2.4
            dx, dy = r.gauss(0, 46), r.gauss(0, 46)
            cls = "on" if on else "off"
            out.append(f'<circle class="{cls}" cx="{gx}" cy="{gy}" r="{2.6 if on else 2.2}" '
                       f'style="--dx:{dx:.1f}px;--dy:{dy:.1f}px;animation-delay:{-16 + i*0.22:.2f}s"/>')
    out.append(f'<path d="M70 450 L730 450" stroke="{INK}" stroke-width="1.2"/>')
    for k, lab in enumerate(["t = T", "", "", "t = 0"]):
        x = 70 + k*220
        out.append(f'<line x1="{x}" y1="444" x2="{x}" y2="456" stroke="{INK}" stroke-width="1.2"/>')
        if lab: out.append(f'<text x="{x}" y="476" font-family="ui-monospace,Menlo,monospace" font-size="13" fill="{MUTED}" text-anchor="middle">{lab}</text>')
    css = f"""
circle.on, circle.off {{ animation: 16s ease-in-out infinite; }}
circle.on {{ fill: {ACC}; }}
circle.off {{ fill: {MUTED}; opacity: .12; }}
circle.on  {{ animation-name: dn-on; }}
circle.off {{ animation-name: dn-off; }}
@keyframes dn-on {{
  0%, 100% {{ transform: translate(var(--dx), var(--dy)); fill: {FAINT}; opacity: .4; }}
  42%, 64% {{ transform: translate(0, 0); fill: {ACC}; opacity: 1; }}
}}
@keyframes dn-off {{
  0%, 100% {{ transform: translate(var(--dx), var(--dy)); fill: {FAINT}; opacity: .4; }}
  42%, 64% {{ transform: translate(0, 0); fill: {MUTED}; opacity: .12; }}
}}
"""
    return svg(''.join(out), css)

def landscape():
    # a map of 41 papers; edges fire like activations, the hub cluster breathes
    r = random.Random(41); out = []; nodes = []
    centers = [(170,150),(380,110),(600,160),(250,330),(470,300),(660,360),(380,420)]
    sizes = [7,6,6,6,6,5,5]  # = 41 papers
    for c,(cx,cy) in enumerate(centers):
        for k in range(sizes[c]):
            a = r.random()*2*math.pi; d = 18 + r.random()*46
            nodes.append((cx+math.cos(a)*d, cy+math.sin(a)*d*0.8, c))
    edges = []
    for i,(x1,y1,c1) in enumerate(nodes):
        for j,(x2,y2,c2) in enumerate(nodes[i+1:], i+1):
            d = math.hypot(x1-x2, y1-y2)
            if (c1 == c2 and d < 60) or (c1 != c2 and d < 120 and r.random() < .18):
                edges.append((x1, y1, x2, y2, c1 == c2))
    for (x1, y1, x2, y2, same) in edges:
        base = .5 if same else .28
        out.append(f'<line class="e" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'style="--b:{base};animation-duration:{9 + r.random()*7:.1f}s;animation-delay:{-r.random()*16:.1f}s"/>')
    hub = 4
    for i,(x,y,c) in enumerate(nodes):
        col = ACC if c == hub else (ACC2 if c == 1 else INK)
        cls = ' class="hub"' if c == hub else ''
        extra = f' style="animation-delay:{-i*0.7:.1f}s"' if c == hub else ''
        out.append(f'<circle{cls} cx="{x:.1f}" cy="{y:.1f}" r="{5 if c==hub else 4}" fill="{PAPER}" stroke="{col}" stroke-width="2"{extra}/>')
    css = f"""
line.e {{ stroke: {MUTED}; stroke-width: 1; opacity: var(--b); animation: fire ease-in-out infinite; }}
@keyframes fire {{
  0%, 82%, 100% {{ opacity: var(--b); stroke: {MUTED}; stroke-width: 1; }}
  90% {{ opacity: .95; stroke: {ACC}; stroke-width: 1.6; }}
}}
circle.hub {{ transform-box: fill-box; transform-origin: center; animation: breathe 4.8s ease-in-out infinite; }}
@keyframes breathe {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.35); }} }}
"""
    return svg(''.join(out), css)

def opro():
    # an optimizer walks down the loss landscape step by step; the re-ranked list keeps reshuffling
    out = []
    cx, cy = 300, 255
    for k in range(1, 9):
        rx, ry = 34*k, 22*k
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate(-18 {cx} {cy})" fill="none" stroke="{FAINT}" stroke-width="1.1" opacity="{1-k*0.08:.2f}"/>')
    pts = [(560,430),(470,400),(430,330),(360,320),(340,280),(312,268),(303,258)]
    d = "M" + " L".join(f"{x} {y}" for x,y in pts)
    out.append(f'<path class="trail" d="{d}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-dasharray="6 5"/>')
    for i,(x,y) in enumerate(pts):
        last = i == len(pts)-1
        out.append(f'<circle cx="{x}" cy="{y}" r="{6 if last else 4.5}" fill="{ACC if last else PAPER}" stroke="{ACC}" stroke-width="2"/>')
    # the walker: hops point to point, pauses at the optimum, restarts
    n = len(pts); hop = 70 / (n - 1)
    frames = []
    for i,(x,y) in enumerate(pts):
        frames.append(f"{i*hop:.1f}% {{ transform: translate({x}px, {y}px); opacity: 1; }}")
    frames.append(f"92% {{ transform: translate({pts[-1][0]}px, {pts[-1][1]}px); opacity: 1; }}")
    frames.append(f"100% {{ transform: translate({pts[-1][0]}px, {pts[-1][1]}px); opacity: 0; }}")
    out.append(f'<circle class="walker" cx="0" cy="0" r="9" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
    # re-ranking bars
    bars = [0.92, 0.81, 0.74, 0.58, 0.47, 0.33]
    for i,b in enumerate(bars):
        y = 110 + i*34
        out.append(f'<rect class="bar" x="610" y="{y}" width="{b*140:.0f}" height="18" rx="2" fill="{ACC2 if i==0 else MUTED}" opacity="{.95 if i==0 else .45}" '
                   f'style="animation-duration:{5 + i*0.9:.1f}s;animation-delay:{-i*1.3:.1f}s"/>')
        out.append(f'<text x="598" y="{y+14}" font-family="ui-monospace,Menlo,monospace" font-size="12" fill="{MUTED}" text-anchor="end">{i+1}</text>')
    css = f"""
path.trail {{ animation: flow11 2.6s linear infinite; }}
circle.walker {{ opacity: 0; animation: walk 11s ease-in-out infinite; }}
@keyframes walk {{ {' '.join(frames)} }}
rect.bar {{ transform-box: fill-box; transform-origin: left center; animation: rerank ease-in-out infinite; }}
@keyframes rerank {{ 0%, 100% {{ transform: scaleX(1); }} 50% {{ transform: scaleX(.86); }} }}
"""
    return svg(''.join(out), css)

def towers():
    # five towers; a signal climbs each tower in turn, arcs carry it across
    out = []
    heights = [6, 8, 5, 7, 4]
    for t,h in enumerate(heights):
        x = 110 + t*130
        for k in range(h):
            y = 420 - k*38
            delay = t*2.2 + k*0.32
            out.append(f'<rect class="blk" x="{x}" y="{y}" width="80" height="28" rx="3" style="animation-delay:{delay - 12:.2f}s"/>')
            if k: out.append(f'<line x1="{x+40}" y1="{y+28}" x2="{x+40}" y2="{y+38}" stroke="{INK}" stroke-width="1.4"/>')
        top = 420 - (h-1)*38
        out.append(f'<text x="{x+40}" y="{top-14}" font-family="ui-monospace,Menlo,monospace" font-size="13" fill="{MUTED}" text-anchor="middle">0{t+1}</text>')
    for a,b in [(0,1),(1,3),(2,4)]:
        x1, x2 = 150 + a*130, 150 + b*130
        out.append(f'<path class="arc" d="M{x1} 462 Q{(x1+x2)/2} 492 {x2} 462" fill="none" stroke="{ACC2}" stroke-width="1.8" stroke-dasharray="5 5"/>')
    css = f"""
rect.blk {{ fill: {PAPER}; stroke: {INK}; stroke-width: 1.6; animation: lit 12s ease-in-out infinite; }}
@keyframes lit {{
  0%, 12%, 100% {{ fill: {PAPER}; stroke: {INK}; }}
  4% {{ fill: {ACC}; stroke: {ACC}; }}
}}
path.arc {{ animation: flow10 2.4s linear infinite; }}
"""
    return svg(''.join(out), css)

def flywheel():
    # the wheel turns: a marker orbits the loop, inspire arcs pulse back, inner ring counter-rotates
    out = []
    cx, cy, R = 400, 250, 165
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    out.append(f'<circle class="inner" cx="{cx}" cy="{cy}" r="{R-34}" fill="none" stroke="{FAINT}" stroke-width="1" stroke-dasharray="2 6"/>')
    angs = [180, 270, 0, 90]
    pts = [(cx + R*math.cos(math.radians(a)), cy + R*math.sin(math.radians(a))) for a in angs]
    for a in [225, 315, 45, 135]:
        x = cx + R*math.cos(math.radians(a)); y = cy + R*math.sin(math.radians(a))
        dx, dy = -math.sin(math.radians(a)), math.cos(math.radians(a))
        out.append(f'<path d="M{x-dx*9-dy*6:.1f} {y-dy*9+dx*6:.1f} L{x:.1f} {y:.1f} L{x-dx*9+dy*6:.1f} {y-dy*9-dx*6:.1f}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    hx, hy = pts[3]
    for (tx, ty) in [pts[0], pts[1]]:
        mx, my = (hx+tx)/2*0.55 + cx*0.45, (hy+ty)/2*0.55 + cy*0.45
        out.append(f'<path class="inspire" d="M{hx:.1f} {hy:.1f} Q{mx:.1f} {my:.1f} {tx:.1f} {ty:.1f}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-dasharray="6 5"/>')
    for i,(x,y) in enumerate(pts):
        r = 13 if i == 2 else 10
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{ACC if i==3 else PAPER}" stroke="{ACC if i==3 else INK}" stroke-width="2"/>')
    out.append(f'<g class="orbit"><circle cx="{cx}" cy="{cy - R}" r="5.5" fill="{ACC}"/></g>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{MUTED}"/>')
    css = f"""
g.orbit {{ transform-origin: {cx}px {cy}px; animation: spin 22s linear infinite; }}
circle.inner {{ transform-origin: {cx}px {cy}px; animation: spin 90s linear infinite reverse; }}
path.inspire {{ animation: flow11 2.8s linear infinite; }}
"""
    return svg("".join(out), css)

def orchestra():
    # a person (LLM) at the centre, orchestrating a ring of precise instruments (classic models):
    # signals flow out along the dashed lines, every needle settles on its own reading
    out = []; r = random.Random(11)
    cx, cy = 400, 250
    n = 6
    needles = []
    for i in range(n):
        a = math.radians(-90 + i * 360 / n)
        x, y = cx + 175 * math.cos(a), cy + 150 * math.sin(a)
        out.append(f'<line class="sig" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="5 5"/>')
        w, h = 92, 46
        out.append(f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
        gx, gy = x, y + 12
        for k in range(9):
            ta = math.radians(200 + k * 17.5)
            r1, r2 = 15, 19 if k % 2 == 0 else 17
            out.append(f'<line x1="{gx + r1*math.cos(ta):.1f}" y1="{gy + r1*math.sin(ta):.1f}" x2="{gx + r2*math.cos(ta):.1f}" y2="{gy + r2*math.sin(ta):.1f}" stroke="{MUTED}" stroke-width="1"/>')
        na = math.radians(200 + (0.35 + 0.08 * i) * 140)
        out.append(f'<line class="needle" x1="{gx}" y1="{gy}" x2="{gx + 14*math.cos(na):.1f}" y2="{gy + 14*math.sin(na):.1f}" stroke="{ACC}" stroke-width="1.6" '
                   f'style="transform-origin:{gx:.1f}px {gy:.1f}px;--a:{6 + r.random()*8:.1f}deg;animation-duration:{4.5 + r.random()*4:.1f}s;animation-delay:{-r.random()*6:.1f}s"/>')
        out.append(f'<circle cx="{gx}" cy="{gy}" r="1.8" fill="{INK}"/>')
    out.append(f'<circle class="halo" cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{FAINT}" stroke-width="1" stroke-dasharray="2 6"/>')
    out.append(f'<circle cx="{cx}" cy="{cy - 8}" r="10" fill="{ACC}"/>')
    out.append(f'<path d="M{cx-20} {cy+22} Q{cx} {cy-2} {cx+20} {cy+22}" fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    css = f"""
line.sig {{ animation: flow10 2.2s linear infinite; }}
line.needle {{ animation: sway ease-in-out infinite; }}
@keyframes sway {{ 0%, 100% {{ transform: rotate(calc(var(--a) * -1)); }} 50% {{ transform: rotate(var(--a)); }} }}
circle.halo {{ transform-origin: {cx}px {cy}px; animation: spin 40s linear infinite; }}
"""
    return svg("".join(out), css)

def accent():
    r = random.Random(3); out = []
    centers = [(120,110,34),(250,70,26),(230,200,30),(330,150,22)]
    for cx,cy,s in centers:
        for _ in range(26):
            out.append(f'<circle cx="{r.gauss(cx,s):.1f}" cy="{r.gauss(cy,s*0.8):.1f}" r="{r.choice([1.6,2,2.4])}" fill="currentColor" opacity="{r.uniform(.25,.6):.2f}"/>')
    out.append(f'<circle cx="230" cy="200" r="62" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 6" opacity=".5"/>')
    out.append(f'<circle cx="230" cy="200" r="4" fill="{ACC}"/>')
    out.append(f'<path d="M230 200 L330 150" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="3 4"/>')
    return f'<svg class="intro-accent" viewBox="0 0 420 300" aria-hidden="true">{"".join(out)}</svg>'

OUT.mkdir(parents=True, exist_ok=True)
for name, fn in [("diffusion-models-for-recsys", diffusion), ("llm-recsys-landscape", landscape), ("opro-and-gr2", opro), ("may-2026-paper-notes", towers), ("creator-flywheel", flywheel), ("llm-takeover-recsys", orchestra)]:
    (OUT/f"{name}.svg").write_text(fn()); print("wrote", name)
pathlib.Path(sys.argv[2]).write_text(accent()); print("wrote accent")
