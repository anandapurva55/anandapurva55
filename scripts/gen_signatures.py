"""The living background of each skill-set box: one always-running scene per skill set, filling the whole box behind its logos.

They are complements, not variations: each draws what its skill set does, in its box's colour, on a shared beat (pulses repeat
every 3 s, travelling currents every 6 s, outer orbits up to 12 s). Drawn in local coordinates 0..w, 0..h and clipped to the box by the caller."""
from math import cos, pi, sin
from random import Random

CSS = ("@keyframes sg-tw{0%,100%{opacity:.3}50%{opacity:1}}.sg-tw{animation:sg-tw 3s ease-in-out infinite}"
       "@keyframes sg-run{to{stroke-dashoffset:-100}}.sg-run{stroke-dasharray:14 86;animation:sg-run 6s linear infinite}"
       "@keyframes sg-orb{to{stroke-dashoffset:-100}}.sg-orb{stroke-dasharray:22 78;animation:sg-orb 9s linear infinite}"
       "@keyframes sg-hex{0%,30%,100%{opacity:0}12%{opacity:1}}.sg-hex{opacity:0;animation:sg-hex 6s ease-in-out infinite}"
       "@keyframes sg-ui{0%,100%{opacity:.18;transform:translateY(9px) scale(.9)}35%,65%{opacity:1;transform:translateY(0) scale(1)}}.sg-ui{transform-box:fill-box;transform-origin:center;animation:sg-ui 3s ease-in-out infinite}"
       "@keyframes sg-step{0%{transform:scale(1);opacity:.7}6%,16%{transform:scale(1.14);opacity:1}26%,100%{transform:scale(1);opacity:.7}}.sg-step{animation:sg-step 6s ease-in-out infinite}"
       "@keyframes sg-draw{0%{stroke-dashoffset:100;opacity:0}4%{opacity:1}14%,88%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}.sg-draw{stroke-dasharray:100;animation:sg-draw 6s ease-out infinite}"
       "@keyframes sg-req{0%{transform:translateX(0);opacity:0}5%{opacity:1}42%{transform:translateX(903px);opacity:1}48%,100%{transform:translateX(903px);opacity:0}}.sg-req{opacity:0;animation:sg-req 6s ease-in-out infinite}"
       "@keyframes sg-res{0%,48%{transform:translateX(903px);opacity:0}54%{opacity:1}92%{transform:translateX(0);opacity:1}98%,100%{transform:translateX(0);opacity:0}}.sg-res{opacity:0;animation:sg-res 6s ease-in-out infinite}"
       "@keyframes sg-commit{0%{opacity:0;transform:scale(.3)}7%{opacity:1;transform:scale(1.25)}12%,88%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(1)}}.sg-commit{transform-box:fill-box;transform-origin:center;animation:sg-commit 6s ease-out infinite}"
       "@keyframes sg-branch{0%,8%{stroke-dashoffset:100;opacity:1}64%,90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}.sg-branch{stroke-dasharray:100;animation:sg-branch 6s linear infinite}"
       "@keyframes sg-merge{0%,63%{opacity:0;transform:scale(.6)}68%{opacity:1;transform:scale(1)}88%,100%{opacity:0;transform:scale(2.2)}}.sg-merge{opacity:0;transform-box:fill-box;transform-origin:center;animation:sg-merge 6s ease-out infinite}"
       "@keyframes sg-beam{0%{stroke-dashoffset:16;opacity:0}2%{opacity:1}15%{opacity:1}18%,100%{stroke-dashoffset:-100;opacity:0}}.sg-beam{opacity:0;stroke-dasharray:16 120;animation:sg-beam 6s ease-in-out infinite}"
       "@keyframes sg-glow{0%,100%{opacity:.12}6%{opacity:1}28%{opacity:.12}}.sg-glow{opacity:.12;animation:sg-glow 6s ease-out infinite}"
       "@keyframes sg-heart{0%,100%{transform:scale(.8) rotate(0deg)}50%{transform:scale(1.15) rotate(45deg)}}.sg-heart{animation:sg-heart 3s ease-in-out infinite}"
       "@keyframes sg-ring{0%{opacity:0;transform:scale(.7)}4%{opacity:1}20%,100%{opacity:0;transform:scale(1.35)}}.sg-ring{opacity:0;transform-box:fill-box;transform-origin:center;animation:sg-ring 6s ease-out infinite}"
       "@keyframes sg-back{to{stroke-dashoffset:100}}.sg-back{stroke-dasharray:10 90;animation:sg-back 6s linear infinite}"
       "@keyframes sg-bar{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}.sg-bar{transform-box:fill-box;transform-origin:50% 100%;animation:sg-bar 3s ease-in-out infinite}"
       "@keyframes sg-rise{0%{transform:translateY(8px);opacity:0}30%,70%{opacity:1}100%{transform:translateY(-14px);opacity:0}}.sg-rise{animation:sg-rise 3s ease-in-out infinite}"
       "@keyframes sg-spin{to{transform:rotate(360deg)}}.sg-spin{animation:sg-spin 6s linear infinite}")


def _line(d, col, o=.3, extra=""):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{o}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def _flow(d, col, cls="sg-run", delay=0.0):
    return (f'<path class="{cls}" style="animation-delay:{delay}s" pathLength="100" d="{d}" fill="none" stroke="{col}" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _dot(x, y, col, r=3, cls="sg-tw", delay=0.0):
    return f'<circle class="{cls}" style="animation-delay:{delay}s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'


def _net(col, w, h):                  # a network spread through the box, signals travelling its links
    rng = Random(1)
    nx, ny = 11, max(3, round(h / 70) + 1)
    pts = [[(i * w / (nx - 1) + rng.uniform(-24, 24), j * h / (ny - 1) + rng.uniform(-18, 18)) for j in range(ny)] for i in range(nx)]
    o, k = "", 0
    for i in range(nx - 1):
        for j in range(ny):
            for dj in (0, 1 if (i + j) % 2 else -1):
                if 0 <= j + dj < ny:
                    (x1, y1), (x2, y2) = pts[i][j], pts[i + 1][j + dj]
                    d = f"M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}"
                    o += _line(d, col, .22)
                    if rng.random() < .3:
                        o += _flow(d, col, delay=-k * .8)
                        k += 1
    return o + "".join(_dot(x, y, col, 3.2, delay=-(i * .4 + j * .7)) for i, c in enumerate(pts) for j, (x, y) in enumerate(c))


def neural(col, w, h):                # Generative & agentic AI: calls travel from the middle of the box to each tool in turn, which lights up as it is reached
    lite = "#efe9ff"
    cx, cy = 514, 134                                   # in the gap between the two logo rows
    targets = [(64 + c * 100, 82) for c in range(10)] + [(64 + c * 100, 182) for c in range(9)]
    order = [(k * 7) % len(targets) for k in range(len(targets))]       # calls hop around the wall instead of sweeping across it
    o = f'<g opacity=".3">{_net(col, w, h)}</g>'
    o += (f'<defs><radialGradient id="sgg"><stop offset="0" stop-color="{col}" stop-opacity=".9"/><stop offset=".45" stop-color="{col}" stop-opacity=".3"/>'
          f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>')
    calls = ""
    for slot, i in enumerate(order):
        tx, ty = targets[i]
        dx, dy = tx - cx, ty - cy
        dist = (dx * dx + dy * dy) ** .5
        ex, ey = tx - dx / dist * 30, ty - dy / dist * 30                # stop at the logo's edge
        mx, my = (cx + ex) / 2, (cy + ey) / 2 + (-24 if ty < cy else 24) * min(1, abs(dx) / 200)
        d = f"M{cx} {cy}Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}"
        t = slot * 6 / len(targets)
        o += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.4"/>'
        for width, op, c in ((8, .35, col), (2.8, 1, lite)):
            calls += (f'<path class="sg-beam" style="animation-delay:{t - 6:.2f}s" pathLength="100" d="{d}" fill="none" stroke="{c}" stroke-opacity="{op}" '
                      f'stroke-width="{width}" stroke-linecap="round"/>')
        calls += (f'<circle class="sg-glow" style="animation-delay:{t + .7 - 6:.2f}s" cx="{tx}" cy="{ty}" r="46" fill="url(#sgg)"/>'
                  f'<circle class="sg-ring" style="animation-delay:{t + .7 - 6:.2f}s" cx="{tx}" cy="{ty}" r="29" fill="none" stroke="{lite}" stroke-width="2"/>')
    o += calls
    # no emblem at the centre (it read as one more logo): only a soft light that breathes where the calls begin
    o += f'<g transform="translate({cx},{cy})"><ellipse class="sg-tw" cx="0" cy="0" rx="90" ry="46" fill="url(#sgg)"/></g>'
    return o


def fit(col, w, h):                   # ML: gradient descent, optimisers stepping down a loss surface to the minimum
    cx, cy = w * .58, h * .52
    o = "".join(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{r * 3.1:.0f}" ry="{r:.0f}" transform="rotate(-6 {cx:.0f} {cy:.0f})" fill="none" '
                f'stroke="{col}" stroke-opacity="{.46 - i * .045:.2f}" stroke-width="1.5"/>' for i, r in enumerate((14, 36, 62, 92, 128, 170, 218)))
    starts = ((12, h * .12), (w - 12, h * .1), (30, h * .94), (w - 30, h * .9), (w * .3, 10))
    for k, (x, y) in enumerate(starts):
        pts, px, py = [(x, y)], x, y
        for n in range(7):                  # zig-zag steps that shrink as the minimum gets closer
            px += (cx - px) * .42
            py += (cy - py) * .42 + (1 if n % 2 else -1) * 15 * .7 ** n
            pts.append((px, py))
        d = "M" + "L".join(f"{a:.0f} {b:.0f}" for a, b in pts + [(cx, cy)])
        o += _line(d, col, .3) + _flow(d, col, delay=-k * 1.2)
        o += "".join(_dot(a, b, col, 2.6, delay=-(k * .4 + n * .3)) for n, (a, b) in enumerate(pts[:5]))
    return o + _dot(cx, cy, col, 6)


def bars(col, w, h):                  # Data: a live bar chart rising along the floor of the box
    rng = Random(3)
    o = "".join(_line(f"M0 {h * q:.0f}H{w}", col, .14) for q in (.3, .55, .8))
    for i in range(int(w // 26)):
        bh = h * rng.uniform(.18, .72)
        o += f'<rect class="sg-bar" style="animation-delay:{-i * .21:.2f}s" x="{8 + i * 26}" y="{h - bh:.0f}" width="14" height="{bh:.0f}" rx="3" fill="{col}" fill-opacity=".45"/>'
    return o


def loop(col, w, h):                  # MLOps: one great build -> ship -> monitor loop circling the whole box
    cx, cy, rx, ry = w / 2, h / 2, w * .46, h * .62
    d = (f"M{cx} {cy}C{cx - rx * .35} {cy - ry} {cx - rx} {cy - ry} {cx - rx} {cy}S{cx - rx * .35} {cy + ry} {cx} {cy}"
         f"S{cx + rx} {cy - ry} {cx + rx} {cy}S{cx + rx * .35} {cy + ry} {cx} {cy}Z")
    return _line(d, col, .28) + _flow(d, col) + _flow(d, col, delay=-2) + _flow(d, col, delay=-4)


def cloud(col, w, h):                 # AWS: a honeycomb of services, a wave of activity rolling across the whole box
    r = 24
    dx, dy = r * 3 ** .5, r * 1.5
    o, row = "", 0
    while row * dy < h + r:
        for c in range(int(w / dx) + 2):
            x, y = c * dx + (dx / 2 if row % 2 else 0), row * dy
            pts = " ".join(f"{x + (r - 3) * sin(k * pi / 3):.1f},{y - (r - 3) * cos(k * pi / 3):.1f}" for k in range(6))
            o += (f'<polygon points="{pts}" fill="none" stroke="{col}" stroke-opacity=".2" stroke-width="1.4"/>'
                  f'<polygon class="sg-hex" style="animation-delay:{(x / w) * 6 + row * .25 - 12:.2f}s" points="{pts}" fill="{col}" fill-opacity=".3" stroke="{col}" stroke-width="1.4"/>')
        row += 1
    return o


def orbit(col, w, h):                 # GCP: large currents sweeping along shared orbits, the widest reaching both edges of the box
    cx, cy = w / 2, h / 2
    o = _dot(cx, cy, col, 7)
    for i, r in enumerate((30, 62, 96, 132, 168, 204)):
        rx, ry = r * 2.7, r * .5
        d = f"M{cx - rx:.0f} {cy:.0f}a{rx:.0f} {ry:.0f} 0 1 0 {2 * rx:.0f} 0a{rx:.0f} {ry:.0f} 0 1 0 {-2 * rx:.0f} 0"
        o += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".7" stroke-width="2.4"/>'
        dur = 6 + i * 1.2
        for k in range(1 if i < 2 else 2):          # outer orbits carry two currents, opposite each other
            st = f"animation-delay:{-i * 1.7 - k * dur / 2:.1f}s;animation-duration:{dur}s"
            for width, op in ((7, .25), (2.8, 1)):   # a soft glow under a bright core
                o += (f'<path class="sg-orb" style="{st}" pathLength="100" d="{d}" fill="none" stroke="{col}" stroke-width="{width}" '
                      f'stroke-opacity="{op}" stroke-linecap="round"/>')
    return o


def radar(col, w, h):                 # Security & observability: a radar sweeping the box, a heartbeat running across it
    r = w * .2
    o = f'<g transform="translate({w * .8:.0f},{h / 2:.0f})">'
    o += "".join(f'<circle r="{r * q:.0f}" fill="none" stroke="{col}" stroke-opacity=".26" stroke-width="1.5"/>' for q in (.25, .5, .75, 1))
    x, y = r * cos(-pi / 5), r * sin(-pi / 5)
    o += (f'<g class="sg-spin"><path d="M0 0H{r:.0f}A{r:.0f} {r:.0f} 0 0 0 {x:.0f} {y:.0f}Z" fill="{col}" fill-opacity=".2"/><path d="M0 0H{r:.0f}" stroke="{col}" stroke-width="2"/></g>'
          f'{_dot(-60, -24, col, 3)}{_dot(44, 30, col, 3, delay=-1.5)}</g>')
    base = h * .84
    d = f"M0 {base:.0f}" + "".join(f"H{x}l8 -18l11 30l9 -17l7 5" for x in range(90, int(w) - 60, 190)) + f"H{w}"
    return o + _line(d, col, .26) + _flow(d, col) + _flow(d, col, delay=-3)


def api(col, w, h):                   # Backend: a request going out through client -> gateway -> validation -> service -> data, and the response coming home
    ink = f'fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    cy, bw, bh = h * .52, 78, 62
    xs = [445 + i * 132 for i in range(5)]
    client = f'<rect {ink} x="-26" y="-18" width="52" height="34" rx="5"/><path {ink} d="M-26 -8H26"/>' + "".join(_dot(-19 + k * 7, -13, col, 2, delay=-k * .4) for k in range(3)) + f'<path {ink} d="M-14 2H6M-14 9H14"/>'
    gate = f'<path {ink} d="M0 -21L21 -13V1C21 13 11 19 0 23C-11 19 -21 13 -21 1V-13Z"/><path {ink} d="M-8 -5l-6 6l6 6M8 -5l6 6l-6 6M3 -8l-6 18"/>'
    valid = f'<path {ink} d="M-17 -21H8L18 -11V21H-17Z M8 -21V-11H18"/><path {ink} d="M-9 -7H4M-9 1H10"/><path {ink} d="M-7 11l5 5l11 -11"/>'
    teeth = "".join(f'<path d="M{14 * cos(k * pi / 4):.1f} {14 * sin(k * pi / 4):.1f}L{21 * cos(k * pi / 4):.1f} {21 * sin(k * pi / 4):.1f}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>' for k in range(8))
    work = f'<g class="sg-spin">{teeth}<circle {ink} r="13"/><circle {ink} r="5"/></g>'
    data = f'<ellipse {ink} cx="0" cy="-15" rx="19" ry="7"/><path {ink} d="M-19 -15V15C-19 19 -10 22 0 22S19 19 19 15V-15M-19 -5C-19 -1 -10 2 0 2S19 -1 19 -5M-19 5C-19 9 -10 12 0 12S19 9 19 5"/>'
    x0, x1, top, bot = xs[0], xs[-1], 17, h - 15
    o = ""
    for y, y_in, cls in ((top, cy - bh / 2, "sg-run"), (bot, cy + bh / 2, "sg-back")):      # request lane above, response lane below
        lane = f"M18 {y}H{w - 18:.0f}"                                                    # both lanes run the whole width of the box
        o += _line(lane, col, .45) + _flow(lane, col, cls) + _flow(lane, col, cls, -3)
        o += "".join(_line(f"M{x} {y}V{y_in:.0f}", col, .45) for x in xs)
    for k, (x, icon) in enumerate(zip(xs, (client, gate, valid, work, data))):
        o += (f'<g transform="translate({x},{cy:.0f})"><g class="sg-step" style="animation-delay:{k * .55 - 6:.2f}s">'
              f'<rect x="{-bw / 2}" y="{-bh / 2}" width="{bw}" height="{bh}" rx="13" fill="#121018" stroke="{col}" stroke-width="1.8"/>'
              f'<rect x="{-bw / 2}" y="{-bh / 2}" width="{bw}" height="{bh}" rx="13" fill="{col}" fill-opacity=".12"/>{icon}</g></g>')
    for y, cls, label, pw, fill in ((top, "sg-req", "REQUEST  \u2192", 104, col), (bot, "sg-res", "\u2190  200 OK", 88, "#7be0ad")):
        o += (f'<g transform="translate(70,{y})"><g class="{cls}"><rect x="{-pw / 2}" y="-10" width="{pw}" height="20" rx="10" fill="{fill}"/>'
              f'<text y="4" text-anchor="middle" style="font:800 11px monospace;fill:#101014">{label}</text></g></g>')
    return o


def ui(col, w, h):                    # Frontend & data apps: an interface assembling across the box
    rng = Random(9)
    o, x, i = "", 14, 0
    while x < w - 40:
        bw = rng.choice((70, 110, 150))
        bw = min(bw, w - 14 - x)
        y = 14
        while y < h - 20:
            bh = min(rng.choice((20, 34, 52)), h - 12 - y)
            o += (f'<g opacity="{.55 if x < 390 else 1}"><rect class="sg-ui" style="animation-delay:{(x / w) * 3 + (y / h) * .8 - 6:.2f}s" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{col}" fill-opacity=".18" '
                  f'stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/></g>')
            y += bh + 9
            i += 1
        x += bw + 10
    return o


def typing(col, w, h):                # AI coding assistants: the whole agent loop, ask -> plan -> write -> test -> ship, and round again
    ink = f'fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    cy, bw, bh = h * .52, 78, 66
    xs = [445 + i * 132 for i in range(5)]

    def draw_in(d, delay, width=2.6):       # a stroke that writes itself once per loop
        return (f'<path class="sg-draw" style="animation-delay:{delay - 6:.2f}s" pathLength="100" d="{d}" fill="none" stroke="{col}" '
                f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    ask = (f'<path {ink} d="M-22 -16H22a6 6 0 0 1 6 6V6a6 6 0 0 1-6 6H-6l-12 10V12h-4a6 6 0 0 1-6-6V-10a6 6 0 0 1 6-6Z"/>'
           + "".join(_dot(-11 + k * 11, -2, col, 3, delay=-k * .5) for k in range(3)))
    plan = "".join(f'<rect {ink} x="-26" y="{y - 5}" width="10" height="10" rx="2.5"/>' + draw_in(f"M-24 {y}l3 3l6 -7", .9 + k * .35, 2.4)
                   + draw_in(f"M-8 {y}H{24 - k * 7}", 1.0 + k * .35) for k, y in enumerate((-17, 0, 17)))
    write = (f'<path {ink} d="M-30 -15H30"/>' + "".join(_dot(-24 + k * 7, -21, col, 2, delay=-k * .4) for k in range(3))
             + "".join(draw_in(f"M{x0} {y}H{x1}", 1.9 + k * .3, 3.6) for k, (x0, y, x1) in enumerate(((-24, -6, 8), (-14, 4, 24), (-14, 14, 12), (-24, 24, -4)))))
    test = (f'<path {ink} d="M-27 -17l9 8l-9 8M-12 0H2"/>'
            + "".join(draw_in(f"M{x - 5} 14l4 5l8 -10", 3.2 + k * .3, 3) for k, x in enumerate((-18, 0, 18))))
    ship = (f'<circle {ink} cx="-16" cy="16" r="5"/><circle {ink} cx="-16" cy="-16" r="5"/><circle {ink} cx="18" cy="-2" r="5"/>'
            f'<path {ink} d="M-16 -11V11"/>' + draw_in("M18 3C18 15 2 16 -11 16", 4.3) + draw_in("M6 14l7 8l14 -17", 4.8, 3.4))
    rail = f"M{xs[0]} {cy:.0f}H{xs[-1]}"
    back = f"M{xs[-1]} {cy + bh / 2:.0f}C{xs[-1]} {h + 4} {xs[-1] - 90} {h - 8} {xs[-1] - 190} {h - 8}H120C50 {h - 8} 18 {h - 30:.0f} 18 {cy:.0f}S60 10 150 10H{xs[0] - 70}C{xs[0] - 20} 10 {xs[0]} 12 {xs[0]} {cy - bh / 2:.0f}"
    o = _line(rail, col, .4) + _flow(rail, col) + _flow(rail, col, delay=-3) + _line(back, col, .22) + _flow(back, col, delay=-1.5)
    for k, (x, icon) in enumerate(zip(xs, (ask, plan, write, test, ship))):
        o += (f'<g transform="translate({x},{cy:.0f})"><g class="sg-step" style="animation-delay:{k * 1.0 - 6:.1f}s">'
              f'<rect x="{-bw / 2}" y="{-bh / 2}" width="{bw}" height="{bh}" rx="13" fill="#141016" stroke="{col}" stroke-width="1.8"/>'
              f'<rect x="{-bw / 2}" y="{-bh / 2}" width="{bw}" height="{bh}" rx="13" fill="{col}" fill-opacity=".12"/>{icon}</g></g>')
    return f'<g transform="translate(0,0)">{o}</g>'


def branches(col, w, h):              # Languages & dev tools: main runs along the floor; a feature branches off, gains commits and merges back
    main_y, top = h - 14, 18
    start, end = 384, w - 62                 # the branch rises in the gap between two logos
    path = (f"M{start} {main_y:.0f}C{start + 36} {main_y:.0f} {start + 24} {top} {start + 62} {top}H{end - 100}"
            f"C{end - 30} {top} {end - 84} {main_y:.0f} {end} {main_y:.0f}")
    main = f"M18 {main_y:.0f}H{w - 18:.0f}"
    pale = "#d6f5e2"          # the feature branch: a paler tint of the same green

    def tag(x, y, text, tw, fill, cls, delay):
        return (f'<g transform="translate({x:.0f},{y:.0f})"><g class="{cls}" style="animation-delay:{delay}s"><rect x="{-tw / 2}" y="-10" width="{tw}" height="20" rx="10" fill="{fill}"/>'
                f'<text y="4" text-anchor="middle" style="font:800 11px monospace;fill:#101412">{text}</text></g></g>')

    def commit(x, y, c, delay):             # a commit lands: it pops in and stays until the loop restarts
        return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6.5" fill="#0f1613" stroke="{c}" stroke-opacity=".4" stroke-width="2"/>'
                f'<circle class="sg-commit" style="animation-delay:{delay - 6:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="6.5" fill="{c}"/>')

    o = _line(main, col, .75) + _flow(main, col) + _flow(main, col, delay=-3)
    o += _line(path, pale, .3) + f'<path class="sg-branch" pathLength="100" d="{path}" fill="none" stroke="{pale}" stroke-width="3" stroke-linecap="round"/>'
    o += "".join(commit(x, main_y, col, i * .12) for i, x in enumerate((64, 164, 264, start)))
    xs = [start + 90, start + 160, end - 190, end - 120]      # the label sits in the clear middle
    o += "".join(commit(x, top, pale, 1.0 + i * .6) for i, x in enumerate(xs))
    o += tag((xs[1] + xs[2]) / 2, top, "FEATURE BRANCH", 118, pale, "sg-commit", -4.4)
    o += (f'<circle class="sg-merge" cx="{end}" cy="{main_y:.0f}" r="11" fill="none" stroke="{col}" stroke-width="3"/>'
          + commit(end, main_y, col, 3.9) + tag(end - 6, main_y - 34, "MERGED \u2713", 82, col, "sg-commit", -2.0))
    return o


BY_KEY = [("GENERATIVE", neural), ("ML & DATA", fit), ("DATA & ANALYTICS", bars), ("MLOPS", loop), ("AMAZON", cloud), ("GOOGLE", orbit),
          ("SECURITY", radar), ("BACKEND", api), ("FRONTEND", ui), ("AI CODING", typing), ("LANGUAGES", branches)]


def scene(title, col, w, h):
    for key, fn in BY_KEY:
        if title.startswith(key):
            return fn(col, w, h)
    raise KeyError(f"no background scene for skill set: {title}")
