"""Hero banner, section headings and the closing call-to-action."""
import base64
from html import escape

import textwrap

from assetlib import (AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, OUT, PANEL, PANEL2, RM, ROSE, SKY,
                      cur, logo, logo_box, mono_tile, pd, round_path, write)


def hero():
    W, H = 1000, 490
    nus = base64.b64encode((OUT / "nus-logo.png").read_bytes()).decode()

    # "current flowing": inputs -> AI chip -> business outcomes
    traces = [
        ([(560, 66), (650, 66), (650, 130), (728, 130)], EM, 0.0, "DATA", (560, 52), "start"),
        ([(560, 150), (728, 150)], AM, 0.5, "MODELS", (560, 136), "start"),
        ([(560, 234), (650, 234), (650, 170), (728, 170)], SKY, 1.0, "TOOLS", (560, 220), "start"),
        ([(812, 130), (884, 130), (884, 66), (968, 66)], LAV, 1.7, "REVENUE", (968, 52), "end"),
        ([(812, 150), (968, 150)], EM, 2.2, "SAVINGS", (968, 136), "end"),
        ([(812, 170), (884, 170), (884, 234), (968, 234)], ROSE, 2.7, "USERS", (968, 220), "end"),
    ]
    circuit = term = lab = ""
    for pts, col, dl, name, (lx, ly), anc in traces:
        circuit += cur(pd(pts), col, dl, 3.2)
        for (px, py) in (pts[0], pts[-1]):
            term += f'<circle cx="{px}" cy="{py}" r="6" fill="{BG}" stroke="{col}" stroke-width="2.2"/><circle cx="{px}" cy="{py}" r="2.4" fill="{col}"/>'
        lab += f'<text x="{lx}" y="{ly}" text-anchor="{anc}" style="font:700 11px {MONO};fill:{MUTED};letter-spacing:1.8px">{name}</text>'


    tiles = [
        ("FORD, INDIA", "ford", "$350K+", "annual business value", ["conversational AI"], EM),
        ("TRIANZ, INDIA", "trianz", "$1.6M+", "revenue generated", ["AI consulting clients"], AM),
        ("ST ENGINEERING, SINGAPORE", "stengg", "$150K", "projected savings a year", ["client: Singapore", "Police Force"], SKY),
        ("360DIALOG, GERMANY", "360dialog", "$235K", "fraud losses prevented", ["per year"], LAV),
        ("CLANITY, INDIA", "clanity", "500+", "active users", ["founded the company"], ROSE),
    ]
    tw, tg, ty, th = 176, 14, 288, 188
    tl = ""
    for i, (label, slug, m, c1, c2s, col) in enumerate(tiles):
        x = 32 + i * (tw + tg)
        centred = slug in ("ford", "360dialog", "clanity")   # compact marks sit in the middle; wide wordmarks stay left
        tlab = "".join(f'<text x="{x + 18}" y="{ty + 26 + k * 14}" style="font:700 10.5px {MONO};fill:{col};letter-spacing:1.2px">{escape(l)}</text>'
                      for k, l in enumerate(textwrap.wrap(label, 18)))
        mark = logo_box(slug, x + 18, ty + 46, 140 if centred else 128, 32, bg=PANEL2, align="xMidYMid" if centred else "xMinYMid") or mono_tile(label[:2], col, x + (tw - 32) / 2, ty + 46, 32)
        sub = "".join(f'<text x="{x + 18}" y="{ty + 157 + k * 15}" style="font:400 12px {FONT};fill:{MUTED}">{escape(l)}</text>' for k, l in enumerate(c2s))
        tl += f"""<g class="rise" style="animation-delay:{.5 + i * .1}s"><rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="16" fill="{PANEL2}" stroke="{col}" stroke-opacity=".42"/>
    {tlab}
    {mark}
    <text x="{x + 18}" y="{ty + 118}" style="font:800 32px {FONT};fill:{INK}">{escape(m)}</text>
    <text x="{x + 18}" y="{ty + 141}" style="font:600 13px {FONT};fill:{BODY}">{escape(c1)}</text>
    {sub}</g>"""

    css = ("@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1}}"
           "@keyframes breath{0%,100%{opacity:.4}50%{opacity:1}}"
           "@keyframes hl{0%{opacity:0}5%,18%{opacity:1}26%,100%{opacity:0}}"
           ".rise{animation:rise .8s ease-out both}.breath{animation:breath 3.2s ease-in-out infinite}.hl{opacity:0;animation:hl 4.5s ease-in-out infinite}" + FLOW_CSS + RM)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="tg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{EM}"/><stop offset="1" stop-color="{AM}"/></linearGradient>
    <linearGradient id="gA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAV_MID}"/><stop offset="1" stop-color="{AM}"/></linearGradient>
    <radialGradient id="o1" cx=".1" cy=".95" r=".6"><stop offset="0" stop-color="{EM}" stop-opacity=".14"/><stop offset="1" stop-color="{EM}" stop-opacity="0"/></radialGradient>
    <radialGradient id="o2" cx=".85" cy=".3" r=".5"><stop offset="0" stop-color="{AM}" stop-opacity=".12"/><stop offset="1" stop-color="{AM}" stop-opacity="0"/></radialGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".07"/></pattern>
    {BLUR}
    <clipPath id="c"><path d="{round_path(W, H, 0, 0, 22, 22)}"/></clipPath>
  </defs>
  <style>{css}</style>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#dots)"/>
    <rect width="{W}" height="{H}" fill="url(#o1)"/><rect width="{W}" height="{H}" fill="url(#o2)"/>
  </g>

  <g class="rise">
    <text x="46" y="112" style="font:800 68px {FONT};fill:{INK};letter-spacing:-1.5px">Apurva Anand</text>
  </g>
  <g class="rise" style="animation-delay:.2s">
    <text x="48" y="150" style="font:500 22px {FONT};fill:{BODY}">I design, build and ship GenAI and ML</text>
    <text x="48" y="178" style="font:500 22px {FONT};fill:{BODY}">solutions at enterprise scale that generate</text>
    <text x="48" y="206" style="font:500 22px {FONT};fill:{BODY}"><tspan style="fill:{AM};font-weight:700">measurable business value</tspan>.</text>
    <rect x="48" y="228" width="92" height="40" rx="9" fill="#ffffff"/>
    <image href="data:image/png;base64,{nus}" x="53" y="232" width="82" height="32" preserveAspectRatio="xMidYMid meet"/>
    <text x="154" y="245" style="font:700 15px {FONT};fill:{INK}">M.S., Business Analytics</text>
    <text x="154" y="264" style="font:500 13px {FONT};fill:{MUTED}">National University of Singapore  ·  6 yrs in AI/ML</text>
  </g>

  <g class="rise" style="animation-delay:.25s">
    {circuit}
    {term}
    {lab}
    <rect class="breath" x="722" y="104" width="96" height="92" rx="16" fill="none" stroke="{EM}" stroke-width="2"/>
    <rect x="728" y="110" width="84" height="80" rx="12" fill="{PANEL2}" stroke="{EM}" stroke-opacity=".55"/>
    <text x="770" y="162" text-anchor="middle" style="font:800 30px {MONO};fill:{INK}">AI</text>
  </g>
  {tl}
</svg>"""
    write("hero.svg", svg)


def heading(name, label, col_a, col_b):
    css = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".l{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both}" + RM)
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="66" viewBox="0 0 1000 66">
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


def heading_adaptive(slug, label, col_a, col_b):
    """Transparent heading in two versions; README serves one per GitHub theme through <picture>."""
    css = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".l{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both}" + RM)
    for mode, ink in (("dark", INK), ("light", "#1f2328")):
        write(f"h-{slug}-{mode}.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="66" viewBox="0 0 1000 66">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col_a}"/><stop offset="1" stop-color="{col_b}"/></linearGradient></defs>
  <style>{css}</style>
  <text x="0" y="38" style="font:800 30px {FONT};fill:{ink};letter-spacing:-.3px">{escape(label)}</text>
  <rect class="l" x="0" y="52" width="1000" height="3" rx="1.5" fill="url(#g)"/>
</svg>""")
