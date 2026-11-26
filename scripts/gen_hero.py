"""Hero banner, section headings and the closing call-to-action."""
import base64
from html import escape

import textwrap
from random import Random

from assetlib import (AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, OUT, PANEL, PANEL2, RM, ROSE, SKY,
                      cur, logo, logo_box, mono_tile, pd, round_path, write)


def hero():
    """Calm statement: name, what I do and the proof, centred. One even field of soft light fills the upper half, a ripple passing
    through it again and again in the same five colours as the result columns; the words themselves stay still, and below, the five results light up one after another."""
    W, H, T = 1000, 490, 6.0
    nus = base64.b64encode((OUT / "nus-logo.png").read_bytes()).decode()
    DES, BLD, SHP, VAL = "#b09ee5", "#4fc3bb", "#6f9ee8", "#efa467"          # background glows and the value phrase

    def at(t, dur=T):
        return f'style="animation-delay:{t - dur:.2f}s"'

    def text(x, y, s, size, weight, fill, extra="", fam=FONT):
        return f'<text x="{x}" y="{y}" text-anchor="middle" style="font:{weight} {size}px {fam};fill:{fill};{extra}">{escape(s)}</text>'

    ink = lambda c, w=2.4: f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
    RINGS, BEAT = 16, 3.6
    rings = [""] * RINGS
    step = 25
    cols = ("#4fc3bb", "#efa467", "#6f9ee8", "#b09ee5", "#b7db63")          # left to right, matching the five result columns
    for row in range(11):
        y = 18 + row * step + 2
        for c in range(39):
            x = 25 + c * step
            dist = (((x - 500) / 1.7) ** 2 + (y - 150) ** 2) ** .5           # elliptical, so the ripple matches the card's shape
            # the same dots everywhere; only a smooth dimming behind the words so they stay crisp
            quiet = min(1.0, max(0.0, ((((x - 500) / 330) ** 2 + ((y - 168) / 112) ** 2) ** .5 - .75) / .5))
            op = .26 + .74 * quiet
            k = int(dist / 330 * RINGS * 1.0) % RINGS
            rings[k] += f'<circle cx="{x}" cy="{y}" r="2.7" fill="{cols[min(4, int(x / 200))]}" fill-opacity="{op:.2f}"/>'
    scene = "".join(f'<g class="ripple" style="animation-delay:{k * BEAT / RINGS * 1.0 - BEAT:.2f}s">{dots}</g>' for k, dots in enumerate(rings) if dots)

    # ---- the proof: five results
    results = [("FORD, INDIA", "ford", "$350K+", "annual business value", "conversational AI", "#4fc3bb"),
               ("TRIANZ, INDIA", "trianz", "$1.6M+", "revenue generated", "AI consulting clients", "#efa467"),
               ("ST ENGINEERING, SINGAPORE", "stengg", "$150K", "projected savings a year", "client: Singapore Police Force", "#6f9ee8"),
               ("360DIALOG, GERMANY", "360dialog", "$235K", "fraud losses prevented", "per year", "#b09ee5"),
               ("CLANITY, INDIA", "clanity", "500+", "active users", "founded the company", "#b7db63")]
    band, bw = "", 944 / 5
    for i, (label, slug, m, c1, c2, col) in enumerate(results):
        x = 28 + i * bw
        cx = x + bw / 2
        t = i * .45
        if i:
            band += f'<line x1="{x:.1f}" y1="316" x2="{x:.1f}" y2="452" stroke="#fff" stroke-opacity=".1"/>'
        mark = logo_box(slug, cx - 60, 333, 120, 29, bg=PANEL, align="xMidYMid") or mono_tile(label[:2], col, cx - 15, 333, 29)
        band += (f'<rect class="proof" {at(t, 3.0)} x="{x + 5:.1f}" y="305" width="{bw - 10:.1f}" height="158" rx="16" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-width="1.8"/>'
                 f'{mark}' + text(cx, 323, label, 10, 700, col, f"letter-spacing:{0.4 if len(label) > 20 else 1.4}px", MONO)
                 + text(cx, 399, m, 36, 800, INK, "letter-spacing:-1px") + text(cx, 424, c1, 12.5, 700, BODY) + text(cx, 443, c2, 11, 500, MUTED))

    css = ("@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1}}.rise{animation:rise .8s ease-out both}"
           "@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(70px,22px)}}.drift{animation:drift 14s ease-in-out infinite}.drift2{animation:drift 18s ease-in-out infinite reverse}"
           "@keyframes ripple{0%,100%{opacity:.2}22%{opacity:1}50%{opacity:.2}}.ripple{opacity:.2;animation:ripple 3.6s ease-in-out infinite}"
           "@keyframes proof{0%{opacity:0}9%,24%{opacity:1}44%,100%{opacity:0}}.proof{opacity:0;animation:proof 3s ease-in-out infinite}")
    css += RM

    glows = "".join(f'<radialGradient id="{i}"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
                    for i, c, o in (("a1", BLD, .20), ("a2", DES, .20), ("a3", SHP, .15)))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{glows}<linearGradient id="money" gradientUnits="userSpaceOnUse" x1="424" y1="0" x2="706" y2="0"><stop offset="0.000" stop-color="#d4f86a"/><stop offset="0.200" stop-color="#45e38a"/><stop offset="0.400" stop-color="#d4f86a"/><stop offset="0.600" stop-color="#45e38a"/><stop offset="0.800" stop-color="#d4f86a"/><stop offset="1.000" stop-color="#45e38a"/></linearGradient><linearGradient id="aurora" gradientUnits="userSpaceOnUse" x1="640" y1="0" x2="750" y2="0"><stop offset="0.000" stop-color="#4fe0cf"/><stop offset="0.333" stop-color="#7fb2ff"/><stop offset="0.667" stop-color="#bda6ff"/><stop offset="1.000" stop-color="#ff9fd0"/></linearGradient><clipPath id="c"><path d="{round_path(W, H, 0, 0, 22, 22)}"/></clipPath></defs>
  <style>{css}</style>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    <ellipse class="drift" cx="240" cy="40" rx="440" ry="250" fill="url(#a1)"/><ellipse class="drift2" cx="760" cy="60" rx="440" ry="250" fill="url(#a2)"/><ellipse class="drift" cx="500" cy="520" rx="560" ry="200" fill="url(#a3)"/>
  </g>
  <g clip-path="url(#c)">{scene}</g>
  <g class="rise">{text(500, 116, "Apurva Anand", 80, 800, INK, "letter-spacing:-2.5px")}</g>
  <g class="rise" style="animation-delay:.2s">
    <text x="500" y="167" text-anchor="middle" style="font:500 22px {FONT};fill:{BODY}">I design, build and ship GenAI and ML solutions at enterprise scale</text>
    <text x="500" y="198" text-anchor="middle" style="font:500 22px {FONT};fill:{BODY}">that generate <tspan style="fill:url(#money);font-weight:800">measurable business value</tspan>.</text>
    <rect x="262" y="222" width="106" height="48" rx="10" fill="#ffffff"/>
    <image href="data:image/png;base64,{nus}" x="268" y="226" width="94" height="40" preserveAspectRatio="xMidYMid meet"/>
    <text x="384" y="242" style="font:800 18px {FONT};fill:{INK}">M.S., Business Analytics</text>
    <text x="384" y="266" style="font:600 16px {FONT};fill:{INK}">National University of Singapore<tspan style="fill:{MUTED}">  ·  </tspan><tspan style="fill:url(#aurora);font-weight:800">6 yrs in AI/ML</tspan></text>
  </g>
  <rect x="28" y="300" width="944" height="168" rx="22" fill="{PANEL}" fill-opacity=".72" stroke="#fff" stroke-opacity=".1"/>
  {band}
</svg>"""
    write("hero.svg", svg)


def heading(name, label, col_a, col_b):
    css = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".l{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both}" + RM)
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="58" viewBox="0 0 1000 58">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col_a}"/><stop offset="1" stop-color="{col_b}"/></linearGradient></defs>
  <style>{css}</style>
  <rect width="1000" height="66" rx="14" fill="{BG}"/>
  <text x="22" y="37" style="font:800 30px {FONT};fill:{INK};letter-spacing:-.3px">{escape(label)}</text>
  <rect class="l" x="22" y="49" width="956" height="3" rx="1.5" fill="url(#g)"/>
</svg>""")


def _mix(a, b, t):
    pa, pb = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


ACC_T = 0.7243         # share of the accent line (card + email bar, as rendered) that the card covers
ACC_MID = _mix(EM, AM, ACC_T)
NAV_T = 0.1463         # share of the hero's accent line covered by the menu bar above it
NAV_MID = _mix(EM, AM, NAV_T)


def cta():
    """Closing banner: delivery is a loop, not a line. Six stages sit on a ring; a current circulates through them and the
    last arc feeds back into the problem (iteration). Client outcomes sit under the headline."""
    import math
    from assetlib import ORANGE
    W, H = 1000, 352
    cx, cy, R = 772, 188, 96
    stages = [("THE PROBLEM", ORANGE), ("UNDERSTAND", SKY), ("DESIGN", LAV), ("BUILD", EM), ("SHIP", EM), ("VALUE", AM)]
    T = 9.0
    pos = [(cx + R * math.sin(math.radians(i * 60)), cy - R * math.cos(math.radians(i * 60))) for i in range(6)]

    def arc(i, j, col, dash=""):
        (x0, y0), (x1, y1) = pos[i], pos[j]
        d = f"M{x0:.1f} {y0:.1f} A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}"
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".55" stroke-width="3" stroke-linecap="round" {dash}/>'

    ring = "".join(arc(i, i + 1, stages[i + 1][1]) for i in range(5))
    (vx, vy), (px, py) = pos[5], pos[0]
    ring += (f'<path d="M{vx:.1f} {vy:.1f} A{R} {R} 0 0 1 {px:.1f} {py:.1f}" fill="none" stroke="{ORANGE}" stroke-opacity=".7" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 8"/>'
             f'<path d="M{px - 9:.1f} {py - 7:.1f} L{px + 1:.1f} {py:.1f} L{px - 9:.1f} {py + 7:.1f}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(-8,0)"/>')
    loop = f"M{cx} {cy - R} A{R} {R} 0 1 1 {cx} {cy + R} A{R} {R} 0 1 1 {cx} {cy - R}"
    nodes = ""
    for i, ((t, col), (x, y)) in enumerate(zip(stages, pos)):
        last = i == 5
        r = 14 if last else 12
        if i in (1, 2):
            lx, ly, anc = x + 22, y + 5, "start"
        elif i in (4, 5):
            lx, ly, anc = x - 22, y + 5, "end"
        elif i == 0:
            lx, ly, anc = x, y - 24, "middle"
        else:
            lx, ly, anc = x, y + 36, "middle"
        nodes += (f'<circle class="nh" style="animation-delay:{i * T / 6:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{r + 9}" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-opacity=".9"/>'
                  f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BG}" stroke="{col}" stroke-width="2.8"/>'
                  + (f'<path d="M{x - 6:.1f} {y:.1f} l4.5 5 l8 -10" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' if last
                     else f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}"/>')
                  + f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anc}" style="font:800 12.5px {MONO};fill:{col};letter-spacing:1.6px">{t}</text>')
    chips = ""
    x = 56
    for k, (arrow, label, w) in enumerate((("↑", "Revenue", 130), ("↓", "Cost", 104), ("↓", "Time to decision", 200), ("↓", "Risk", 104))):
        chips += (f'<rect x="{x}" y="262" width="{w}" height="40" rx="20" fill="{EM}" fill-opacity=".09" stroke="{EM}" stroke-opacity=".5"/>'
                  f'<rect class="hl" style="animation-delay:{k * .9}s" x="{x}" y="262" width="{w}" height="40" rx="20" fill="{EM}" fill-opacity=".3" stroke="{EM}"/>'
                  f'<text x="{x + 16}" y="289" style="font:800 20px {FONT};fill:{EM}">{arrow}</text>'
                  f'<text x="{x + 42}" y="288" style="font:700 17px {FONT};fill:{INK}">{label}</text>')
        x += w + 10
    css = ("@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1}}"
           "@keyframes live{0%,100%{opacity:1}50%{opacity:.35}}"
           "@keyframes hl{0%{opacity:0}6%,22%{opacity:1}30%,100%{opacity:0}}"
           f"@keyframes nh{{0%{{opacity:0;transform:scale(.7)}}4%,14%{{opacity:1;transform:scale(1)}}22%,100%{{opacity:0;transform:scale(1.15)}}}}.nh{{transform-box:fill-box;transform-origin:center;opacity:0;animation:nh {T}s ease-in-out infinite}}"
           "@keyframes scr{0%,8%{opacity:0}14%,34%{opacity:1}44%,100%{opacity:0}}.scr{opacity:0;animation:scr 9s ease-in-out infinite}"
           "@keyframes ln{0%,36%{stroke-dashoffset:100;opacity:1}58%,90%{stroke-dashoffset:0;opacity:1}98%,100%{stroke-dashoffset:0;opacity:0}}.ln{stroke-dasharray:100;stroke-dashoffset:100;animation:ln 9s ease-in-out infinite}"
           "@keyframes ck{0%,58%{opacity:0;transform:scale(.4)}66%,90%{opacity:1;transform:scale(1)}98%,100%{opacity:0;transform:scale(1)}}.ck{transform-box:fill-box;transform-origin:center;opacity:0;animation:ck 9s ease-out infinite}"
           "@keyframes spin{to{transform:rotate(360deg)}}.spin{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}"
           ".a{animation:in .8s ease-out both}.b{animation:in .8s .15s ease-out both}.live{animation:live 2.4s ease-in-out infinite}"
           ".hl{opacity:0;animation:hl 3.6s ease-in-out infinite}" + FLOW_CSS + RM)
    write("cta.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{EM}"/><stop offset="1" stop-color="{ACC_MID}"/></linearGradient>
    <linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{EM}"/><stop offset="1" stop-color="{AM}"/></linearGradient>
    <radialGradient id="glow" cx=".77" cy=".53" r=".42"><stop offset="0" stop-color="{AM}" stop-opacity=".13"/><stop offset="1" stop-color="{AM}" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".07"/></pattern>
    {BLUR}
    <clipPath id="c"><rect width="{W}" height="{H}"/></clipPath>
  </defs>
  <style>{css}</style>
  <g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{PANEL}"/><rect width="{W}" height="{H}" fill="url(#dots)"/><rect width="{W}" height="{H}" fill="url(#glow)"/></g>
  <g class="a">
    <circle class="live" cx="60" cy="58" r="5" fill="{EM}"/>
    <text x="76" y="63" style="font:700 14px {MONO};fill:{EM};letter-spacing:3px">OPEN TO CONVERSATIONS</text>
    <text x="54" y="122" style="font:800 44px {FONT};fill:{INK};letter-spacing:-.5px">Got a hard problem?</text>
    <text x="54" y="174" style="font:800 44px {FONT};fill:url(#tg);letter-spacing:-.5px">Let's ship the solution.</text>
  </g>
  <text class="b" x="56" y="214" style="font:500 19px {FONT};fill:{BODY}">Tell me what you want to move. I'll show you how I'd build it.</text>
  <g class="a" style="animation-delay:.2s">{chips}</g>
  <circle class="spin" cx="{cx}" cy="{cy}" r="{R - 26}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="1.5" stroke-dasharray="3 9"/>
  <g>
    <path class="scr" d="M{cx - 38} {cy + 4} l9 -20 l8 34 l9 -38 l9 36 l8 -30 l8 24 l9 -10" fill="none" stroke="{ORANGE}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" style="animation-duration:{T}s"/>
    <path class="ln" pathLength="100" d="M{cx - 38} {cy + 4} H{cx + 24}" fill="none" stroke="{EM}" stroke-width="3.6" stroke-linecap="round" style="animation-duration:{T}s"/>
    <g class="ck" style="animation-duration:{T}s"><circle cx="{cx + 36}" cy="{cy + 4}" r="13" fill="{BG}" stroke="{AM}" stroke-width="2.6"/><path d="M{cx + 30} {cy + 4} l4.5 5 l8 -10" fill="none" stroke="{AM}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>
  </g>
  {ring}
  <g filter="url(#blur)"><path class="cur" pathLength="100" d="{loop}" stroke="{INK}" stroke-width="9" stroke-opacity=".4" style="animation-duration:{T}s"/></g>
  <path class="cur" pathLength="100" d="{loop}" stroke="{INK}" stroke-width="3.6" style="animation-duration:{T}s"/>
  {nodes}
</svg>""")


def button(name, label, col, slug):
    w = int(len(label) * 10.6 + 112)
    ic = logo(slug, 26, 13, 26, bg="#1d2026") or ""
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="52" viewBox="0 0 {w} 52">
  <rect x=".75" y=".75" width="{w - 1.5}" height="50.5" rx="26" fill="{PANEL}"/>
  <rect x=".75" y=".75" width="{w - 1.5}" height="50.5" rx="26" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5"/>
  {ic}
  <text x="66" y="32" style="font:700 17px {FONT};fill:{INK}">{escape(label)}</text>
  <text x="{w - 30}" y="32" text-anchor="middle" style="font:700 17px {FONT};fill:{col}">→</text>
</svg>""")


def nav_pill(name, label, col):
    """A tab-style link pill. GitHub READMEs cannot run JavaScript, so these jump to a section instead of switching content."""
    w = int(len(label) * 10.2 + 52)
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44">
  <rect x=".75" y=".75" width="{w - 1.5}" height="42.5" rx="21.25" fill="{PANEL}"/>
  <rect x=".75" y=".75" width="{w - 1.5}" height="42.5" rx="21.25" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".7" stroke-width="1.5"/>
  <circle cx="22" cy="22" r="4.5" fill="{col}"/>
  <text x="36" y="28" style="font:700 15px {FONT};fill:{INK}">{escape(label)}</text>
</svg>""")


# One calm, confident colour family for every heading (cool blue -> soft indigo). Research (practitioner colour-psychology guides and clothing/job-applicant
# studies) most consistently links blue and blue-violet with trust and competence, and warns that saturated green and red read worse. Both ends were tuned
# for lightness so each keeps >= ~3.8:1 contrast on white, GitHub dark dimmed (#22272e) and GitHub dark (#0d1117): the best any single colour can do on both.
HEAD_A, HEAD_B = "#3383de", "#6e78e1"


def heading_adaptive(slug, label, col_a=None, col_b=None, top=0):
    """ONE bare-text heading image that reads on a white page and on every GitHub dark theme (no theme switching needed)."""
    css = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".l{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both}" + RM)
    tw = round(len(label) * 16.6)
    H = 58 + top      # `top` adds air above the heading (used where it follows a card with no text margin of its own)
    write(f"h-{slug}.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{H}" viewBox="0 0 1000 {H}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{HEAD_A}"/><stop offset="1" stop-color="{HEAD_B}"/></linearGradient>
  <linearGradient id="t" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{tw}" y2="0"><stop offset="0" stop-color="{HEAD_A}"/><stop offset="1" stop-color="{HEAD_B}"/></linearGradient></defs>
  <style>{css}</style>
  <g transform="translate(0,{top})"><text x="0" y="38" style="font:800 30px {FONT};fill:url(#t);letter-spacing:-.3px">{escape(label)}</text>
  <rect class="l" x="0" y="52" width="1000" height="3" rx="1.5" fill="url(#g)"/></g>
</svg>""")
