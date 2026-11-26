"""Tab row, award link bars and contact bars. All are flush, square-edged panels so the page reads as one dark column."""
from assetlib import (AM, BG, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, PANEL, PANEL2, RM, ROSE, SKY, BLUR, cur, escape, logo, pd,
                      round_path, wrap, write)

CSS = ("@keyframes tw{0%,100%{opacity:.25;transform:scale(.7)}50%{opacity:1;transform:scale(1.15)}}"
       "@keyframes ping{0%{opacity:.7;transform:scale(.6)}100%{opacity:0;transform:scale(1.5)}}"
       "@keyframes hl{0%{opacity:.15}12%,32%{opacity:1}44%,100%{opacity:.15}}"
       "@keyframes wave{0%,100%{opacity:.45}50%{opacity:1}}"
       ".tw{transform-box:fill-box;transform-origin:center;animation:tw 2.4s ease-in-out infinite}"
       ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}"
       ".lay{opacity:.15;animation:hl 3.6s ease-in-out infinite}.wv{animation:wave 3.6s ease-in-out infinite}"
       "@keyframes lift{0%,100%{transform:translateY(0)}50%{transform:translateY(-2.5px)}}.lift{animation:lift 3.6s ease-in-out infinite}"
       "@keyframes glint{0%,55%{opacity:0;transform:translateX(-2px)}70%{opacity:.9;transform:translateX(5px)}100%{opacity:0;transform:translateX(8px)}}.glint{animation:glint 3.6s ease-in-out infinite}"
       "@keyframes grow{0%,10%{stroke-dashoffset:10}45%,100%{stroke-dashoffset:0}}.grow{stroke-dasharray:10;animation:grow 3.6s ease-in-out infinite}"
       "@keyframes node{0%,40%{opacity:0;transform:scale(.3)}55%,100%{opacity:1;transform:scale(1)}}.node{transform-box:fill-box;transform-origin:center;animation:node 3.6s ease-out infinite}"
       "@keyframes build{0%,8%{opacity:0;transform:translateY(7px)}30%,85%{opacity:1;transform:translateY(0)}100%{opacity:0;transform:translateY(0)}}.build{animation:build 3.6s ease-in-out infinite}"
       "@keyframes pop{0%,100%{opacity:.4;transform:scale(.88)}15%,30%{opacity:1;transform:scale(1.12)}45%{opacity:.9;transform:scale(1)}}.pop{transform-box:fill-box;transform-origin:center;animation:pop 3.6s ease-in-out infinite}"
       "@keyframes letter{0%,15%,100%{transform:translateY(0)}45%,70%{transform:translateY(-6px)}}.letter{animation:letter 3.6s ease-in-out infinite}"
       "@keyframes flap{0%,15%,100%{transform:scaleY(1)}45%,70%{transform:scaleY(-.7)}}.flap{transform-box:fill-box;transform-origin:50% 0%;animation:flap 3.6s ease-in-out infinite}" + FLOW_CSS + RM)


def glyph(kind, col):
    """Each icon performs a tiny, meaningful loop (about 4s) instead of a generic border effect."""
    s = f'fill="none" stroke="{col}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "award":      # trophy lifts and glints, stars pop
        return (f'<g class="lift"><g {s}><path d="M-6 -11H6V-3a6 6 0 0 1-12 0Z"/><path d="M-6 -8H-11a4 4 0 0 0 5 7"/><path d="M6 -8H11a4 4 0 0 1-5 7"/><path d="M0 3V8M-5 11H5"/></g>'
                f'<path class="glint" d="M-3 -8L-3 -2" stroke="#fff" stroke-width="2" stroke-linecap="round"/></g>'
                f'<path class="tw" d="M14 -14l1.4 3.2 3.2 1.4-3.2 1.4-1.4 3.2-1.4-3.2-3.2-1.4 3.2-1.4z" fill="{AM}"/>'
                f'<path class="tw" style="animation-delay:.8s" d="M-15 -4l1 2.2 2.2 1-2.2 1-1 2.2-1-2.2-2.2-1 2.2-1z" fill="{AM}"/>'
                f'<path class="tw" style="animation-delay:1.6s" d="M15 8l.8 1.8 1.8.8-1.8.8-.8 1.8-.8-1.8-1.8-.8 1.8-.8z" fill="{AM}"/>')
    if kind == "projects":   # a commit is drawn: line grows from the base, then the new node lights up
        return (f'<g {s}><circle cx="-8" cy="-9" r="3.2"/><circle cx="-8" cy="9" r="3.2"/><path d="M-8 -6V6" opacity=".55"/>'
                f'<path class="grow" pathLength="10" d="M-8 0H5.5"/></g>'
                f'<circle class="node" cx="9" cy="0" r="3.2" fill="{col}" stroke="{col}" stroke-width="2.3"/>'
                f'<circle class="ping" cx="9" cy="0" r="6" fill="none" stroke="{col}" stroke-width="2"/>')
    if kind == "stack":      # layers assemble from the bottom up
        out = ""
        for i, dy in enumerate((9, 0, -9)):
            out += (f'<path class="build" style="animation-delay:{i * .5}s" d="M0 {dy - 6}L13 {dy}L0 {dy + 6}L-13 {dy}Z" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2.2" stroke-linejoin="round"/>')
        return out
    if kind == "toolbox":    # logos pop one after another
        out = ""
        for i, (slug, x, y) in enumerate((("aws", -16, -16), ("pytorch", 2, -16), ("python", 2, 2), ("docker", -16, 2))):
            out += f'<g class="pop" style="animation-delay:{i * .6}s">{logo(slug, x, y, 15, bg=BG) or ""}</g>'
        return out
    if kind == "mail":       # flap opens and a letter slides out
        return (f'<g {s}><rect class="letter" x="-7" y="-6" width="14" height="10" rx="1.5" fill="{col}" fill-opacity=".3"/>'
                f'<path d="M-12 -4V8a2 2 0 0 0 2 2H10a2 2 0 0 0 2-2V-4"/>'
                f'<path class="flap" d="M-12 -4L0 5 12 -4" /></g>'
                f'<circle class="ping" cx="0" cy="0" r="14" fill="none" stroke="{col}" stroke-width="2"/>')
    return f'<path d="M-6 -9L10 0L-6 9Z" fill="{col}" fill-opacity=".25" stroke="{col}" stroke-width="2.4" stroke-linejoin="round"/>'     # play


BUBBLE = {"Awards": "See awards", "Projects": "Explore", "Expertise": "Dive in", "Tech Stack": "See tools", "Contact": "Say hi"}


def tab(name, title, col, kind, idx=0):
    """One segment of the menu bar (docked, seamless). Instead of a flowing current, a small speech bubble pops up over every tab at the
    same moment ("See awards", "Explore", ...) with a little tap bounce: it tells the visitor the tabs are clickable."""
    W, H = 200, 84
    T, SLOT = 4.0, 0.0                     # every bubble pops at the same moment, again and again
    label = BUBBLE.get(title, "Click")
    bw = 14 + 6.4 * len(label)
    bx = 124 - bw / 2 + 24
    div = "" if idx == 4 else f'<line x1="{W - .5}" y1="14" x2="{W - .5}" y2="{H - 14}" stroke="#fff" stroke-opacity=".10"/>'
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{BLUR}<linearGradient id="fd" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".10"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
  <style>{CSS}@keyframes bub{{0%{{opacity:0;transform:translateY(8px) scale(.3)}}7%{{opacity:1;transform:translateY(-2px) scale(1.18)}}12%{{transform:translateY(0) scale(1)}}18%{{transform:translateY(-3px) scale(1.04)}}24%{{transform:translateY(0) scale(1)}}78%{{opacity:1;transform:translateY(0) scale(1)}}88%,100%{{opacity:0;transform:translateY(-4px) scale(.85)}}}}.bub{{transform-box:fill-box;transform-origin:50% 100%;opacity:0;animation:bub {T}s ease-out infinite;animation-delay:{idx * SLOT:.1f}s}}</style>
  <rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#fd)"/>
  <rect width="{W}" height="3" fill="{col}" fill-opacity=".85"/>
  <circle cx="38" cy="{H / 2 - 2}" r="34" fill="{col}" fill-opacity=".10"/>
  <circle cx="38" cy="{H / 2 - 2}" r="25" fill="{BG}"/><circle cx="38" cy="{H / 2 - 2}" r="25" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6" stroke-width="1.6"/>
  <g transform="translate(38,{H / 2 - 2}) scale(1.12)">{glyph(kind, col)}</g>
  <text x="76" y="{H / 2 + 6}" style="font:800 22px {FONT};fill:{INK}">{escape(title)}</text>{div}
  <g class="bub"><path d="M{bx + 8:.1f} 26 l-3 -5 h12 z" fill="{col}"/>
    <rect x="{bx:.1f}" y="5" width="{bw:.1f}" height="19" rx="9.5" fill="{col}"/>
    <text x="{bx + bw / 2:.1f}" y="18.2" text-anchor="middle" style="font:800 10.5px {FONT};fill:#0e0f11">{escape(label)}</text></g>
</svg>""")


def bar(name, col, kind, title, sub, tl=0, tr=0, br=0, bl=0, W=500, H=84):
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{BLUR}<clipPath id="c"><path d="{round_path(W, H, tl, tr, br, bl)}"/></clipPath></defs><style>{CSS}</style>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="{col}" fill-opacity=".07"/>
    <rect width="5" height="{H}" fill="{col}"/>
    <line x1="{W - .5}" y1="12" x2="{W - .5}" y2="{H - 12}" stroke="#fff" stroke-opacity=".08"/>
    <circle cx="48" cy="{H / 2}" r="24" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55" stroke-width="1.6"/>
    <g transform="translate(48,{H / 2})">{kind}</g>
    <text x="90" y="{H / 2 - 5}" style="font:800 18px {FONT};fill:{INK}">{escape(title)}</text>
    <text x="90" y="{H / 2 + 17}" style="font:500 13px {FONT};fill:{BODY}">{escape(sub)}</text>
    <text x="{W - 30}" y="{H / 2 + 8}" text-anchor="end" style="font:800 22px {FONT};fill:{col}">→</text>
    {cur(pd([(0, H - 2), (W, H - 2)]), col, 0, 3.6, 3, 6, base=False)}
  </g>
</svg>""")


def contact_bar(name, col, ic, title, sub, kind, W=450, H=102, accent=None, left=True):
    """Footer button docked under the contact card. Each channel has its own story:
    email = a letter flies along the line and lands on the arrow; WhatsApp = typing dots, a bubble, then two ticks."""
    cy = H / 2 - 4
    ly = H - 17
    x0, x1 = 102, W - 96
    wave = ""
    if kind == "mail":
        # email: current circles the logo (clockwise); a draft "subject line" with a blinking caret sits below
        r = 27
        orbit = f"M{56 + r} {cy} A{r} {r} 0 1 1 {56 - r} {cy} A{r} {r} 0 1 1 {56 + r} {cy}"
        wave = cur(orbit, col, 0, 3.2, 3.2, 8, base=False) + cur(orbit, col, -1.6, 3.2, 3.2, 8, base=False)
        anim = (f'<rect x="{x0}" y="{ly - 14}" width="150" height="24" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".45"/>'
                f'<circle class="nbadge" cx="{x0 + 15}" cy="{ly - 2}" r="9" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<circle cx="{x0 + 15}" cy="{ly - 2}" r="5.5" fill="{col}"/>'
                f'<text x="{x0 + 30}" y="{ly + 3}" style="font:600 12.5px {FONT};fill:{INK}">1 new message</text>')
        arrow_delay = "0s"
    else:
        by = ly - 11
        anim = (f'<g class="typing">' + "".join(f'<circle class="d" style="animation-delay:{i * .18}s" cx="{x0 + 8 + i * 11}" cy="{ly}" r="3" fill="{col}"/>' for i in range(3)) + '</g>'
                f'<g class="bub"><rect x="{x0}" y="{by - 3}" width="150" height="24" rx="12" fill="{col}" fill-opacity=".2" stroke="{col}" stroke-opacity=".55"/>'
                f'<text x="{x0 + 13}" y="{by + 13}" style="font:600 12.5px {FONT};fill:{INK}">Hi Apurva, let\'s talk</text>'
                f'<path class="tk1" d="M{x0 + 160} {by + 9}l3.5 3.5 7-8" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path class="tk2" d="M{x0 + 168} {by + 9}l3.5 3.5 7-8" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        wave = ''.join(f'<circle class="wv2" style="animation-delay:{i * 1.1}s" cx="56" cy="{cy}" r="27" fill="none" stroke="{col}" stroke-width="2"/>' for i in range(3))
        arrow_delay = "2.2s"
    CW, CH = 500, H + 32                   # the footer canvas: same scale as the card above, so its background continues seamlessly
    ox, oy = (40 if left else 10), 10      # the button floats inside the card's padding
    write(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">
  <defs>{BLUR}<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="translate({0 if left else -500},0)"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".07"/></pattern>
  <clipPath id="bc"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <linearGradient id="bt" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".16"/><stop offset="1" stop-color="{col}" stop-opacity=".05"/></linearGradient></defs>
  <style>@keyframes gl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}.gl{{animation:gl 3.2s ease-in-out infinite}}{FLOW_CSS}
@keyframes wv2{{0%{{opacity:.75;transform:scale(1)}}100%{{opacity:0;transform:scale(1.9)}}}}.wv2{{transform-box:fill-box;transform-origin:center;animation:wv2 3.3s ease-out infinite}}
@keyframes nb{{0%{{opacity:.8;transform:scale(.7)}}100%{{opacity:0;transform:scale(1.6)}}}}.nbadge{{transform-box:fill-box;transform-origin:center;animation:nb 1.8s ease-out infinite}}
@keyframes fly{{0%{{transform:translateX(0);opacity:0}}8%{{opacity:1}}58%{{transform:translateX({x1 - x0 - 4}px);opacity:1}}66%,100%{{transform:translateX({x1 - x0 + 4}px);opacity:0}}}}.fly{{animation:fly 3.6s ease-in-out infinite}}
@keyframes env{{0%,100%{{transform:translateY(0) rotate(0)}}25%{{transform:translateY(-5px) rotate(-8deg)}}50%{{transform:translateY(-2px) rotate(6deg)}}}}.env{{animation:env 1.6s ease-in-out infinite}}
@keyframes sent{{0%,60%{{opacity:0;transform:scale(.5)}}70%,90%{{opacity:1;transform:scale(1)}}100%{{opacity:0}}}}.sent{{transform-box:fill-box;transform-origin:center;animation:sent 3.6s ease-out infinite}}
@keyframes ty{{0%,4%{{opacity:0}}8%,38%{{opacity:1}}44%,100%{{opacity:0}}}}.typing{{animation:ty 4.2s ease-in-out infinite}}
@keyframes dot{{0%,80%,100%{{opacity:.3;transform:translateY(0)}}40%{{opacity:1;transform:translateY(-3px)}}}}.d{{animation:dot 1s ease-in-out infinite}}
@keyframes bub{{0%,42%{{opacity:0;transform:translateY(5px)}}50%,92%{{opacity:1;transform:translateY(0)}}100%{{opacity:0}}}}.bub{{animation:bub 4.2s ease-out infinite}}
@keyframes tk1{{0%,55%{{opacity:0}}60%,100%{{opacity:.55}}}}.tk1{{animation:tk1 4.2s linear infinite}}
@keyframes tk2{{0%,66%{{opacity:0}}72%,100%{{opacity:1}}}}.tk2{{animation:tk2 4.2s linear infinite}}
@keyframes rp{{0%,{ 'ARR0' }%{{opacity:0;transform:scale(1)}}{ 'ARR1' }%{{opacity:.8;transform:scale(1)}}100%{{opacity:0;transform:scale(1.55)}}}}.rp{{transform-box:fill-box;transform-origin:center;animation:rp {'3.6s' if kind == 'mail' else '4.2s'} ease-out infinite}}{RM}</style>
  <rect width="{CW}" height="{CH}" fill="{PANEL}"/><rect width="{CW}" height="{CH}" fill="url(#dots)"/>
  <g transform="translate({ox},{oy})">
  <rect width="{W}" height="{H}" rx="20" fill="{PANEL2}"/><rect width="{W}" height="{H}" rx="20" fill="url(#bt)"/>
  <g clip-path="url(#bc)">
  <circle class="gl" cx="56" cy="{cy}" r="38" fill="{col}" fill-opacity=".1"/>
  {wave if kind != "mail" else ""}
  <circle cx="56" cy="{cy}" r="27" fill="{PANEL}"/><circle cx="56" cy="{cy}" r="27" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6" stroke-width="1.7"/>
  {wave if kind == "mail" else ""}
  <g transform="translate(56,{cy}) scale(1.2)">{ic}</g>
  <text x="102" y="{H / 2 - 8}" style="font:800 21px {FONT};fill:{INK}">{escape(title)}</text>
  <text x="102" y="{H / 2 + 14}" style="font:500 13.5px {FONT};fill:{BODY}">{escape(sub)}</text>
  {anim}
  <circle class="rp" cx="{W - 46}" cy="{cy}" r="20" fill="none" stroke="{col}" stroke-width="2"/>
  <circle cx="{W - 46}" cy="{cy}" r="20" fill="{col}" fill-opacity=".15" stroke="{col}" stroke-opacity=".6"/>
  <text x="{W - 46}" y="{cy + 8}" text-anchor="middle" style="font:800 22px {FONT};fill:{col}">→</text>
  </g>
  <rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="19.25" fill="none" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>
  </g>
</svg>""".replace("ARR0", "58" if kind == "mail" else "64").replace("ARR1", "66" if kind == "mail" else "72"))


def generate(n_tools):
    tab("nav-award.svg", "Awards", AM, "award", 0)
    tab("nav-projects.svg", "Projects", SKY, "projects", 1)
    tab("nav-expertise.svg", "Expertise", EM, "stack", 2)
    tab("nav-tech.svg", "Tech Stack", LAV, "toolbox", 3)
    tab("nav-contact.svg", "Contact", ROSE, "mail", 4)
    gm = logo("gmail", -12, -12, 24, bg=BG) or ""
    wa = logo("whatsapp", -12, -12, 24, bg=BG) or ""
    contact_bar("bar-email.svg", EM, gm, "Email me", "anandapurva228@gmail.com", "mail", left=True)
    contact_bar("bar-whatsapp.svg", AM, wa, "WhatsApp", "Chat with me directly", "chat", left=False)
