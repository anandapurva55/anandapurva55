"""The living background of each skill-set box: one always-running scene per skill set, filling the whole box behind its logos.

They are complements, not variations: same faintness, same line weight, each in its box's colour and on a calm tempo (multiples of
about 3 s). Drawn in local coordinates 0..w, 0..h and clipped to the box by the caller."""
from math import cos, pi, sin
from random import Random

CSS = ("@keyframes sg-tw{0%,100%{opacity:.3}50%{opacity:1}}.sg-tw{animation:sg-tw 3s ease-in-out infinite}"
       "@keyframes sg-run{to{stroke-dashoffset:-100}}.sg-run{stroke-dasharray:14 86;animation:sg-run 6s linear infinite}"
       "@keyframes sg-back{to{stroke-dashoffset:100}}.sg-back{stroke-dasharray:10 90;animation:sg-back 6s linear infinite}"
       "@keyframes sg-fit{0%{stroke-dashoffset:100}55%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-100}}.sg-fit{stroke-dasharray:100;animation:sg-fit 6s ease-in-out infinite}"
       "@keyframes sg-bar{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}.sg-bar{transform-box:fill-box;transform-origin:50% 100%;animation:sg-bar 3s ease-in-out infinite}"
       "@keyframes sg-rise{0%{transform:translateY(8px);opacity:0}30%,70%{opacity:1}100%{transform:translateY(-14px);opacity:0}}.sg-rise{animation:sg-rise 3s ease-in-out infinite}"
       "@keyframes sg-spin{to{transform:rotate(360deg)}}.sg-spin{animation:sg-spin 6s linear infinite}"
       "@keyframes sg-pop{0%,100%{opacity:.25;transform:scale(.88)}40%,70%{opacity:1;transform:scale(1)}}.sg-pop{transform-box:fill-box;transform-origin:center;animation:sg-pop 6s ease-in-out infinite}"
       "@keyframes sg-type{0%{transform:scaleX(0)}45%,90%{transform:scaleX(1)}100%{transform:scaleX(0)}}.sg-type{transform-box:fill-box;transform-origin:0 50%;animation:sg-type 6s ease-in-out infinite}")


def _line(d, col, o=.3, extra=""):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{o}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def _flow(d, col, cls="sg-run", delay=0.0):
    return (f'<path class="{cls}" style="animation-delay:{delay}s" pathLength="100" d="{d}" fill="none" stroke="{col}" stroke-width="2.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _dot(x, y, col, r=3, cls="sg-tw", delay=0.0):
    return f'<circle class="{cls}" style="animation-delay:{delay}s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'


def neural(col, w, h):                # GenAI: a network spread through the box, signals travelling its links
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


def fit(col, w, h):                   # ML: curves fitting themselves through a cloud of data points
    rng = Random(2)
    f = lambda x, k: h * (.86 - k) - (h * .7) * (x / w) ** 1.4 + 14 * sin(x / 90)
    o = ""
    for n, k in enumerate((0, -.12)):
        d = "M" + "L".join(f"{x} {f(x, k):.0f}" for x in range(0, int(w) + 21, 20))
        o += _line(d, col, .22) + _flow(d, col, "sg-fit", -n * 3)
    for i in range(70):
        x = rng.uniform(10, w - 10)
        o += _dot(x, f(x, -.06) + rng.uniform(-34, 34), col, 2.6, delay=-i * .17)
    return o


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


def cloud(col, w, h):                 # AWS: workloads rising through the whole box
    rng = Random(5)
    o = ""
    for i in range(54):
        x, y, z = rng.uniform(6, w - 16), rng.uniform(18, h - 8), rng.choice((7, 9, 12))
        o += (f'<g class="sg-rise" style="animation-delay:{-rng.uniform(0, 3):.2f}s"><rect x="{x:.0f}" y="{y:.0f}" width="{z}" height="{z}" rx="2.5" fill="{col}" fill-opacity=".55"/>'
              f'<path d="M{x + z / 2:.0f} {y + z + 4:.0f}v18" stroke="{col}" stroke-opacity=".25" stroke-width="1.6" stroke-linecap="round"/></g>')
    return o


def orbit(col, w, h):                 # GCP: services orbiting a shared core
    o = f'<g transform="translate({w * .76:.0f},{h / 2:.0f})">{_dot(0, 0, col, 7)}'
    for i, r in enumerate((34, 62, 94, 130)):
        o += (f'<g transform="scale(2.6,.62)"><circle r="{r}" fill="none" stroke="{col}" stroke-opacity=".28" stroke-width="1.5" vector-effect="non-scaling-stroke"/>'
              f'<g class="sg-spin" style="animation-delay:{-i * 1.7:.1f}s;animation-duration:{9 + i * 3}s"><ellipse cx="{r}" cy="0" rx="1.9" ry="7" fill="{col}"/></g></g>')
    return o + "</g>"


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


def api(col, w, h):                   # Backend: requests and responses on lanes across the box
    o = ""
    for i in range(int(h // 26)):
        y = 18 + i * 26
        d = f"M0 {y}H{w}"
        o += _line(d, col, .15, 'stroke-dasharray="2 9"') + _flow(d, col, "sg-run" if i % 2 == 0 else "sg-back", -i * 1.3)
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
            o += (f'<rect class="sg-pop" style="animation-delay:{-i * .55:.2f}s" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{col}" fill-opacity=".09" '
                  f'stroke="{col}" stroke-opacity=".32" stroke-width="1.5"/>')
            y += bh + 9
            i += 1
        x += bw + 10
    return o


def typing(col, w, h):                # AI coding assistants: code writing itself across the box
    rng = Random(10)
    o, i = "", 0
    for row in range(int((h - 16) // 17)):
        x = 18 + rng.choice((0, 22, 44))
        while x < w - 40:
            bw = rng.randint(28, 130)
            bw = min(bw, w - 16 - x)
            o += f'<rect class="sg-type" style="animation-delay:{row * .45 + (x % 7) * .05 - 6:.2f}s" x="{x}" y="{14 + row * 17}" width="{bw}" height="6" rx="3" fill="{col}" fill-opacity="{rng.uniform(.17, .4):.2f}"/>'
            x += bw + 14
            i += 1
    return o


def branches(col, w, h):              # Languages & dev tools: a commit history branching and merging across the box
    m = h * .82
    o = _line(f"M0 {m:.0f}H{w}", col, .3) + _flow(f"M0 {m:.0f}H{w}", col)
    pts = [(x, m) for x in range(40, int(w), 95)]
    for k, (x0, x1, top) in enumerate(((16, 330, h * .2), (150, 520, h * .5), (400, 720, h * .1), (560, 880, h * .38), (760, w - 12, h * .18))):
        d = f"M{x0} {m:.0f}C{x0 + 40} {m:.0f} {x0 + 30} {top:.0f} {x0 + 80} {top:.0f}H{x1 - 80}C{x1 - 30} {top:.0f} {x1 - 40} {m:.0f} {x1} {m:.0f}"
        o += _line(d, col, .26) + _flow(d, col, delay=-k * 2)
        pts += [(x, top) for x in range(x0 + 110, x1 - 90, 70)]
    return o + "".join(_dot(x, y, col, 4, delay=-i * .3) for i, (x, y) in enumerate(pts))


BY_KEY = [("GENERATIVE", neural), ("ML & DATA", fit), ("DATA & ANALYTICS", bars), ("MLOPS", loop), ("AMAZON", cloud), ("GOOGLE", orbit),
          ("SECURITY", radar), ("BACKEND", api), ("FRONTEND", ui), ("AI CODING", typing), ("LANGUAGES", branches)]


def scene(title, col, w, h):
    for key, fn in BY_KEY:
        if title.startswith(key):
            return fn(col, w, h)
    raise KeyError(f"no background scene for skill set: {title}")
