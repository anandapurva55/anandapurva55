"""One section with one message, in the order a reader should take it in (answer first, then support):

    Strong foundations  ->  classical ML, DL and NLP  ->  generative and agentic AI  ->  production

Design rules taken from the research: lead with the answer, label every connection with a verb, keep one level of
abstraction per tier, and keep each tier small enough to read at a glance."""
from assetlib import (AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, PANEL, PANEL2, RM, ROSE, SKY, cur, escape,
                      lines_svg, logo, pd, wrap, write)


def tier_frame(x, y, w, h, col, num, name, takeaway):
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="22" fill="{PANEL}" stroke="{col}" stroke-opacity=".42"/>'
            f'<text x="{x + 26}" y="{y + 36}" style="font:800 14px {MONO};fill:{col};letter-spacing:2.6px">{num}  {escape(name)}</text>'
            f'<text x="{x + w - 26}" y="{y + 37}" text-anchor="end" style="font:800 17px {FONT};fill:{INK}">{escape(takeaway)}</text>')


# ------------------------------------------------------------ capability icons
def icon(kind, col):
    s = f'fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "prompt":
        return f'<g {s}><path d="M-15 -12h30a3 3 0 0 1 3 3v14a3 3 0 0 1-3 3h-14l-9 8v-8h-7a3 3 0 0 1-3-3v-14a3 3 0 0 1 3-3z"/><path d="M-8 -3h16M-8 3h9"/></g>'
    if kind == "search":
        return f'<g {s}><circle cx="-3" cy="-3" r="12"/><path d="M6 6L17 17"/></g><circle cx="-3" cy="-3" r="2.6" fill="{col}"/>'
    if kind == "train":
        return (f'<g {s}><path d="M-12 -16V16M0 -16V16M12 -16V16"/></g><circle cx="-12" cy="-4" r="4.6" fill="{col}"/>'
                f'<circle cx="0" cy="8" r="4.6" fill="{col}"/><circle cx="12" cy="-8" r="4.6" fill="{col}"/>')
    if kind == "agents":
        return (f'<g {s}><path d="M0 -13L-14 11M0 -13L14 11M-14 11H14"/></g><circle cx="0" cy="-13" r="5.4" fill="{col}"/>'
                f'<circle cx="-14" cy="11" r="5.4" fill="{col}"/><circle cx="14" cy="11" r="5.4" fill="{col}"/>')
    if kind == "plug":
        return f'<g {s}><rect x="-11" y="-3" width="22" height="15" rx="5"/><path d="M-5 -3V-14M5 -3V-14M0 12V19"/></g>'
    return f'<g {s}><path d="M0 -16V14M-14 -8H14M-14 -8l-6 12h12zM14 -8l-6 12h12zM-8 16h16"/></g>'


# ------------------------------------------------------------ production visuals
VW, VH = 237, 60


def v_guard(col):
    gx = VW * .52
    out = (f'<line x1="0" y1="{VH / 2}" x2="{VW}" y2="{VH / 2}" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>'
           f'<rect x="{gx - 3}" y="2" width="6" height="{VH - 4}" rx="3" fill="{col}" fill-opacity=".85"/>')
    for cls, c in (("pass", EM), ("blk", AM), ("pass2", EM)):
        out += f'<circle class="{cls}" cx="6" cy="{VH / 2}" r="6" fill="{c}"/>'
    return out


def v_observe(col):
    m = VH / 2
    d = f"M0 {m} L40 {m} L47 {m - 12} L54 {m + 14} L63 {m - 24} L72 {m + 20} L79 {m} L132 {m} L139 {m - 7} L146 {m + 7} L153 {m} L{VW} {m}"
    return cur(d, col, 0, 3.4, 3.4, 7)


def v_eval(col):
    n = 14
    bw = (VW - (n - 1) * 4) / n
    hs = [.6, .8, .95, .5, .85, .9, .7, .96, .55, .88, .92, .66, .8, .97]
    out = ""
    for i, hh in enumerate(hs):
        bh = hh * (VH - 6)
        out += f'<rect class="bar" style="animation-delay:{i * .08}s" x="{i * (bw + 4):.1f}" y="{VH - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="2.5" fill="{EM if hh > .62 else AM}"/>'
    out += f'<line x1="0" y1="{VH - .62 * (VH - 6)}" x2="{VW}" y2="{VH - .62 * (VH - 6)}" stroke="{INK}" stroke-opacity=".5" stroke-dasharray="3 4"/>'
    return out


def v_fallback(col):
    names, w_, g_ = ["Gemini", "GPT", "Llama", "Qwen"], 53, 8
    out = ""
    for i, n in enumerate(names):
        x = i * (w_ + g_)
        out += (f'<rect x="{x}" y="11" width="{w_}" height="38" rx="10" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-opacity=".4"/>'
                f'<text x="{x + w_ / 2}" y="34" text-anchor="middle" style="font:700 11px {MONO};fill:{BODY}">{n}</text>')
        if i < 3:
            out += f'<path d="M{x + w_ + 1} 30 h6" stroke="{col}" stroke-width="2"/>'
    for i in range(4):                                      # every provider takes its turn, left to right
        out += f'<rect class="hl" style="animation-delay:{i * .9}s" x="{i * (w_ + g_)}" y="11" width="{w_}" height="38" rx="10" fill="{EM}" fill-opacity=".32" stroke="{EM}"/>'
    return out


def v_cost(col):
    out = f'<text x="0" y="9" style="font:700 9.5px {MONO};fill:{MUTED};letter-spacing:1px">COST PER CLAIM  $0.049 → $0.035</text>'
    out += f'<rect x="0" y="14" width="{VW}" height="6" rx="3" fill="#fff" fill-opacity=".22"/>'
    out += f'<rect class="gbar" x="0" y="23" width="{VW * .71:.0f}" height="6" rx="3" fill="{col}"/>'
    out += f'<text x="0" y="46" style="font:700 9.5px {MONO};fill:{MUTED};letter-spacing:1px">LATENCY  p50 14 ms · p95 373 ms</text>'
    out += f'<rect x="0" y="51" width="{VW}" height="6" rx="3" fill="{col}" fill-opacity=".3"/>'
    out += f'<rect class="gbar" style="animation-delay:.3s" x="0" y="51" width="{VW * 14 / 373 * 2.2:.0f}" height="6" rx="3" fill="{EM}"/>'
    return out


def v_iac(col):
    labs = ["IaC", "CI", "Image", "Cloud"]
    w_ = 50
    g_ = (VW - 4 * w_) / 3
    cy = VH / 2
    out = cur(pd([(w_ / 2, cy), (VW - w_ / 2, cy)]), col, 0, 2.4, 3.4, 8)
    for i, l in enumerate(labs):
        x = i * (w_ + g_)
        out += (f'<rect x="{x}" y="{cy - 17}" width="{w_}" height="34" rx="10" fill="{PANEL2}" stroke="{col}" stroke-opacity=".6"/>'
                f'<text x="{x + w_ / 2}" y="{cy + 4}" text-anchor="middle" style="font:700 11px {MONO};fill:{INK}">{l}</text>')
    return out


CARDS = [
    ("Security and guardrails", EM, v_guard, "Prompt-injection filtering, Entra ID behind an API gateway, and SAST, license and supply-chain scans in CI/CD.", []),
    ("Observability", SKY, v_observe, "Distributed tracing, metrics and alarms, plus synthetic canary queries that alert only on a real regression.", []),
    ("Evaluation at scale", ROSE, v_eval, "LLM-as-a-Judge regression suites score relevance over 5,000+ queries per release: measured, not eyeballed.", []),
    ("Reliability", LAV, v_fallback, "Multi-provider model fallback, fail-open guardrails and a human in the loop wherever a wrong answer is costly.", []),
    ("Latency and cost", AM, v_cost, "Measured, not guessed: model cost cut from $0.049 to $0.035 per claim; p95 373 ms end to end over HTTPS.", []),
    ("Cloud and infrastructure", SKY, v_iac, "AWS and GCP defined as code with Terraform, CDK and CloudFormation, containerised and shipped through CI/CD.", []),
]


def stack():
    W, x0, tw = 1000, 76, 924
    gap = 52                                       # room for the verb that connects one tier to the next
    out = ""
    ys = {}

    # ---- answer first: the whole message in one line, before any detail
    out += (f'<text x="2" y="38" style="font:800 34px {FONT};letter-spacing:-.5px"><tspan fill="{LAV}">Strong foundations</tspan>'
            f'<tspan fill="{MUTED}">  ·  </tspan><tspan fill="{EM}">modern AI</tspan><tspan fill="{MUTED}">  ·  </tspan><tspan fill="{AM}">production discipline</tspan></text>'
            f'<text x="2" y="70" style="font:500 17px {FONT};fill:{BODY}">The mathematics tells me why a model works. GenAI and agents let me build with it.</text>'
            f'<text x="2" y="95" style="font:500 17px {FONT};fill:{BODY}">Production engineering keeps it fast, safe, affordable and working.</text>')
    y = 130

    # ---- tier 1: foundations
    h1 = 132
    ys[1] = y
    out += tier_frame(x0, y, tw, h1, LAV, "01", "FOUNDATIONS", "I know why models work.")
    syms = [("∇", "calculus", EM), ("A·x", "linear algebra", AM), ("P(A|B)", "probability", SKY), ("σ²", "statistics", ROSE)]
    bw = (tw - 48 - 3 * 14) / 4
    for i, (s_, l_, c) in enumerate(syms):
        bx = x0 + 24 + i * (bw + 14)
        out += (f'<g class="glow" style="animation-delay:{i * 1.2}s"><rect x="{bx}" y="{y + 58}" width="{bw}" height="56" rx="14" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".5"/>'
                f'<text x="{bx + 18}" y="{y + 94}" style="font:800 24px {MONO};fill:{c}">{escape(s_)}</text>'
                f'<text x="{bx + bw - 18}" y="{y + 92}" text-anchor="end" style="font:600 15px {FONT};fill:{BODY}">{l_}</text></g>')
    conns = [(y + h1, "so I can choose the right model")]
    y += h1 + gap

    # ---- tier 2: classical ML -> DL -> NLP
    h2 = 186
    ys[2] = y
    out += tier_frame(x0, y, tw, h2, SKY, "02", "CLASSICAL ML  ·  DEEP LEARNING  ·  NLP", "I pick the right model for the problem.")
    steps = [("Classical ML", "regression · classification · gradient boosting · causal inference · survival analysis"),
             ("Deep learning", "PyTorch · TensorFlow · Keras"),
             ("NLP", "transformers · DistilBERT · text classification · NLTK")]
    nw = 266
    g2 = (tw - 48 - 3 * nw) / 2
    cy = y + 112
    line = pd([(x0 + 24 + nw / 2, cy), (x0 + 24 + 2 * (nw + g2) + nw / 2, cy)])
    out += cur(line, SKY, 0, 4.8, 3.4, 8) + cur(line, EM, 2.4, 4.8, 3.4, 8, base=False)
    for i, (t, s_) in enumerate(steps):
        nx = x0 + 24 + i * (nw + g2)
        out += (f'<rect x="{nx}" y="{y + 62}" width="{nw}" height="100" rx="16" fill="{PANEL2}" stroke="{SKY}" stroke-opacity=".55" stroke-width="1.6"/>'
                f'<text x="{nx + 20}" y="{y + 92}" style="font:800 20px {FONT};fill:{INK}">{t}</text>'
                + lines_svg(wrap(s_, nw - 40, 12, .6), nx + 20, y + 114, 12, MUTED, 17, 500, MONO))
    conns.append((y + h2, "then I moved to"))
    y += h2 + gap

    # ---- tier 3: the LLM hub, with a current flowing along every spoke
    h3 = 330
    ys[3] = y
    out += tier_frame(x0, y, tw, h3, EM, "03", "GENERATIVE & AGENTIC AI", "I build LLM systems, not demos.")
    hx, hy = x0 + tw / 2, y + 184
    nodes = [  # title, sub, x, y, w, h, side
        ("Prompt Engineering", "intent classification and entity extraction", hx - 160, y + 58, 320, 58, "top"),
        ("RAG and semantic search", "grounded answers from your own data", x0 + 24, y + 100, 290, 74, "left"),
        ("Fine-tuning", "SFT with LoRA and QLoRA", x0 + 24, y + 214, 290, 74, "left"),
        ("Multi-agent systems", "orchestrated agents with tools, memory and humans in the loop", x0 + tw - 24 - 290, y + 100, 290, 74, "right"),
        ("MCP servers", "custom tools for AI clients", x0 + tw - 24 - 290, y + 214, 290, 74, "right"),
        ("LLM-as-a-Judge", "scalable evaluation and regression tests", hx - 150, y + 258, 300, 58, "bottom"),
    ]
    spoke_cols = [EM, AM, SKY, LAV, ROSE, EM]
    for k, (t, s_, nx, ny, nw_, nh, side) in enumerate(nodes):
        if side == "left":
            p_ = [(nx + nw_, ny + nh / 2), (hx - 52, hy)]
        elif side == "right":
            p_ = [(hx + 52, hy), (nx, ny + nh / 2)]
        elif side == "top":
            p_ = [(hx, ny + nh), (hx, hy - 52)]
        else:
            p_ = [(hx, hy + 52), (hx, ny)]
        out += cur(pd(p_), spoke_cols[k], k * .5, 2.4, 3.4, 8)
    for k, (t, s_, nx, ny, nw_, nh, side) in enumerate(nodes):
        sub = wrap(s_, nw_ - 28, 12.5, .53)
        out += (f'<rect x="{nx}" y="{ny}" width="{nw_}" height="{nh}" rx="14" fill="{PANEL2}" stroke="{spoke_cols[k]}" stroke-opacity=".6" stroke-width="1.6"/>'
                f'<text x="{nx + nw_ / 2}" y="{ny + 25}" text-anchor="middle" style="font:800 16px {FONT};fill:{INK}">{escape(t)}</text>'
                + lines_svg(sub, nx + nw_ / 2, ny + 44, 12.5, MUTED, 16, 500, anchor="middle"))
    out += (f'<circle class="breath" cx="{hx}" cy="{hy}" r="58" fill="none" stroke="{EM}" stroke-width="2"/>'
            f'<circle cx="{hx}" cy="{hy}" r="52" fill="{PANEL2}" stroke="{EM}" stroke-opacity=".7" stroke-width="2"/>'
            f'<text x="{hx}" y="{hy + 9}" text-anchor="middle" style="font:800 24px {MONO};fill:{INK}">LLM</text>')
    conns.append((y + h3, "and I ship it with"))
    y += h3 + gap

    # ---- tier 4: production, with the platform badges up front
    cw, ch = (tw - 48 - 2 * 16) / 3, 220
    h4 = 92 + 2 * ch + 16 + 24
    ys[4] = y
    out += tier_frame(x0, y, tw, h4, AM, "04", "PRODUCTION", "I keep it fast, safe and affordable.")
    for j, ic in enumerate(["aws", "googlecloud", "terraform", "docker", "kubernetes", "githubactions"]):
        out += logo(ic, x0 + 26 + j * 46, y + 52, 30, bg=PANEL) or ""
    for i, (title, col, vis, cap, _logos) in enumerate(CARDS):
        r, c = divmod(i, 3)
        cx_ = x0 + 24 + c * (cw + 16)
        cy_ = y + 92 + r * (ch + 16)
        out += (f'<rect x="{cx_ + .5}" y="{cy_ + .5}" width="{cw - 1}" height="{ch - 1}" rx="18" fill="{PANEL2}" stroke="{col}" stroke-opacity=".4"/>'
                f'<text x="{cx_ + 22}" y="{cy_ + 34}" style="font:800 17px {FONT};fill:{INK}">{escape(title)}</text>'
                f'<g transform="translate({cx_ + 22},{cy_ + 52})">{vis(col)}</g>'
                + lines_svg(wrap(cap, cw - 44, 13), cx_ + 22, cy_ + 52 + VH + 26, 13, BODY, 18))
    H = y + h4

    # ---- connectors: a verb on every link, with the current flowing through it
    spine_pts = pd([(30, ys[1] + 40), (30, ys[4] + 40)])
    spine = cur(spine_pts, AM, 0, 6.5, 3.6, 9) + cur(spine_pts, EM, 3.2, 6.5, 3.6, 9, base=False)
    cols = {1: LAV, 2: SKY, 3: EM, 4: AM}
    for n in (1, 2, 3, 4):
        spine += (f'<circle cx="30" cy="{ys[n] + 40}" r="15" fill="{BG}" stroke="{cols[n]}" stroke-width="2.6"/>'
                  f'<text x="30" y="{ys[n] + 45}" text-anchor="middle" style="font:800 14px {MONO};fill:{cols[n]}">{n}</text>')
        out += f'<path d="M45 {ys[n] + 40} H{x0}" stroke="{cols[n]}" stroke-opacity=".5" stroke-width="2"/>'
    for yy, label in conns:
        out += (f'<text x="{x0 + 8}" y="{yy + 33}" style="font:700 15px {FONT};fill:{BODY}"><tspan fill="{AM}">↓</tspan>  {escape(label)}</text>')

    css = ("@keyframes pass{0%{transform:translateX(0);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateX(225px);opacity:0}}"
           "@keyframes blk{0%{transform:translateX(0);opacity:0}8%{opacity:1}45%{transform:translateX(118px);opacity:1}60%{transform:translateX(112px);opacity:0}100%{transform:translateX(112px);opacity:0}}"
           "@keyframes hl{0%{opacity:0}6%,22%{opacity:1}30%,100%{opacity:0}}"
           "@keyframes bar{0%{transform:scaleY(.08)}35%,100%{transform:scaleY(1)}}"
           "@keyframes gbar{0%{transform:scaleX(.04)}40%,100%{transform:scaleX(1)}}"
           "@keyframes glow{0%,100%{opacity:.78}50%{opacity:1}}@keyframes breath{0%,100%{opacity:.35}50%{opacity:1}}"
           "@keyframes ring{0%{opacity:0;transform:scale(.92)}30%{opacity:.7}100%{opacity:0;transform:scale(1.22)}}"
           ".pass{animation:pass 3.6s linear infinite}.pass2{animation:pass 3.6s 1.8s linear infinite}.blk{animation:blk 3.6s linear .9s infinite}"
           ".hl{opacity:0;animation:hl 3.6s ease-in-out infinite}"
           ".bar{transform-box:fill-box;transform-origin:50% 100%;animation:bar 4.5s ease-out infinite}"
           ".gbar{transform-box:fill-box;transform-origin:0 50%;animation:gbar 3.6s ease-out infinite}"
           ".glow{animation:glow 7s ease-in-out infinite}.breath{animation:breath 3.2s ease-in-out infinite}"
           ".ring{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring 4.5s ease-out infinite}" + FLOW_CSS + RM)
    pad, head_h = 22, 80
    chain_x = [522 + (i - 2) * 190 for i in range(5)]
    chain_cols = [LAV, SKY, EM, ROSE, AM]
    chain_names = ["MATH", "ML", "GENAI", "AGENTS", "PRODUCTION"]
    cy_ = pad + 42
    chain = cur(pd([(chain_x[0], cy_), (chain_x[-1], cy_)]), EM, 0, 4.4, 3.4, 8)
    for xx, cc, nm in zip(chain_x, chain_cols, chain_names):
        chain += (f'<circle cx="{xx}" cy="{cy_}" r="7" fill="{BG}" stroke="{cc}" stroke-width="2.6"/><circle cx="{xx}" cy="{cy_}" r="2.6" fill="{cc}"/>'
                  f'<text x="{xx}" y="{cy_ - 16}" text-anchor="middle" style="font:700 10.5px {MONO};fill:{MUTED};letter-spacing:1.4px">{nm}</text>')
    from gen_sections import GROW
    gdef, ghead = "", ""
    write("stack.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * pad}" height="{H + 2 * pad + head_h}" viewBox="0 0 {W + 2 * pad} {H + 2 * pad + head_h}">
  <defs>{BLUR}{gdef}</defs>
  <style>{css}{GROW}</style>
  <rect width="{W + 2 * pad}" height="{H + 2 * pad + head_h}" fill="{BG}" stroke="#fff" stroke-opacity=".08"/>
  {ghead}
  {chain}
  <g transform="translate({pad},{pad + head_h})">{spine}{out}</g>
</svg>""")
