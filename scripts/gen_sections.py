"""Section cards that contain their own title, so every section is one dark card (no separate strip + panel).

GitHub's page is white in light mode and a README cannot colour its background, so each section is drawn as a
self-contained dark card. Text blocks (the award paragraph, the projects intro) live inside the card too."""
import base64
import re
from html import escape

from assetlib import AM, BG, BLUR, BODY, EM, FONT, INK, LAV, MONO, MUTED, OUT, PANEL, RM, SKY, wrap, write

AWARD_TEXT = ("In 2025, at Trianz, one of my former employers and a **digital consulting company**, I built a **real-time agentic voice "
              "assistant** that automates **insurance claims adjustment** through natural conversation, powered by Amazon Nova Sonic and "
              "Nova Pro. It secured **global runner-up recognition** in the 2025 Amazon Nova Partner Demo Competition hosted by AWS, "
              "outperforming **leading global consulting firms** such as **Deloitte and Accenture**. I also presented and explained the "
              "solution as part of the competition demo.")

PROJECTS_TEXT = ("Beyond my professional work, I build end-to-end, open-source systems in my own time. They push the same ideas I use at work "
                 "further, and each one is a complete working project, listed here with everything it uses.")


def plain(text):
    return text.replace("**", "")


def rich_lines(text, width, fs):
    """Word-wrap text that contains **bold** runs; returns lines of (word, is_bold)."""
    toks = []
    for i, seg in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        toks += [(w, i % 2 == 1) for w in seg.split()]
    lines, cur, curw = [], [], 0.0
    sp = fs * .28
    for w, b in toks:
        ww = len(w) * fs * (.585 if b else .525)
        if cur and curw + sp + ww > width:
            lines.append(cur); cur, curw = [], 0.0
        curw += ww + (sp if cur else 0)
        cur.append((w, b))
    if cur:
        lines.append(cur)
    return lines


def emit(lines, x, y, fs, lh, hl):
    out = ""
    for i, l in enumerate(lines):
        spans = ""
        for k, (w, b) in enumerate(l):
            lead = "" if (k == 0 or w[0] in ".,;:!?)") else " "      # no space before punctuation that follows a highlighted word
            style = f' style="font-weight:800;fill:{hl}"' if b else ""
            spans += f"<tspan{style}>{lead}{escape(w)}</tspan>"
        out += f'<text x="{x}" y="{y + i * lh}" style="font:500 {fs}px {FONT};fill:{BODY}" xml:space="preserve">{spans}</text>'
    return out


def title(label, ca, cb, w, gid, x=30, y=56):
    defs = f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ca}"/><stop offset="1" stop-color="{cb}"/></linearGradient>'
    body = (f'<text x="{x}" y="{y}" style="font:800 30px {FONT};fill:{INK};letter-spacing:-.3px">{escape(label)}</text>'
            f'<rect class="l" x="{x}" y="{y + 12}" width="{w - 2 * x}" height="3" rx="1.5" fill="url(#{gid})"/>')
    return defs, body


GROW = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".l{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.2s ease-out both}")


def award_card():
    W, pad = 1000, 44
    defs, head = title("Global award-winning work", AM, LAV, W, "ga", x=pad, y=84)
    lines = rich_lines(AWARD_TEXT, W - 2 * pad, 18)
    ty = 160
    body = emit(lines, pad, ty, 18, 31, AM)
    iy = ty + len(lines) * 31 + 22
    iw = W - 2 * pad
    ih = iw * 588 / 1158
    jpg = base64.b64encode((OUT / "aws-nova-competition-results.jpg").read_bytes()).decode()
    H = int(iy + ih + pad + 18)
    write("sec-award.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{defs}<clipPath id="ic"><rect x="{pad}" y="{iy}" width="{iw}" height="{ih:.0f}" rx="14"/></clipPath></defs>
  <style>{GROW + RM}</style>
  <rect width="{W}" height="{H}" fill="{BG}" stroke="#fff" stroke-opacity=".08"/>
  {head}
  {body}
  <image href="data:image/jpeg;base64,{jpg}" x="{pad}" y="{iy}" width="{iw}" height="{ih:.0f}" clip-path="url(#ic)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="{pad}" y="{iy}" width="{iw}" height="{ih:.0f}" rx="14" fill="none" stroke="#fff" stroke-opacity=".14"/>
</svg>""")


def projects_card():
    W, pad = 1000, 44
    defs, head = title("Built on top of my day job", SKY, EM, W, "gp", x=pad, y=84)
    lines = rich_lines(PROJECTS_TEXT, W - 2 * pad, 18)
    body = emit(lines, pad, 160, 18, 31, AM)
    H = 160 + len(lines) * 31 + 70
    hint = f'<text x="{pad}" y="{H - 22}" style="font:700 12px {MONO};fill:{MUTED};letter-spacing:1.6px">CLICK ANY PROJECT TO OPEN ITS REPOSITORY  ↗</text>'
    write("sec-projects.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{defs}</defs>
  <style>{GROW + RM}</style>
  <rect width="{W}" height="{H}" fill="{BG}" stroke="#fff" stroke-opacity=".08"/>
  {head}
  {body}
  {hint}
</svg>""")
