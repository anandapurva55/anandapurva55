"""Shared helpers for the README asset generator: palette, text wrapping, logo inlining
and the animated "current" strokes used across the page."""
import base64
import itertools
import re
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
LOGOS = OUT / "logos"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

# warm graphite + semantic accents (green = results, amber = achievement)
BG, PANEL, PANEL2 = "#0e0f11", "#17191d", "#1f2228"
INK, BODY, MUTED = "#f4f0e8", "#d9d5cc", "#a29e95"
EM, AM, SKY, LAV, ROSE = "#56d6a0", "#f2b24d", "#7db4f0", "#8b7cf6", "#e8a1c5"
ORANGE = "#ee8658"   # ANSI "warning" orange: used for the guarded sandbox project

# Motion rules (see README notes): ambient loops only, 3-10 s, linear for "flow", ease-in-out for pulses,
# and everything stops under prefers-reduced-motion.
RM = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
FLOW_CSS = ("@keyframes flow{from{stroke-dashoffset:12}to{stroke-dashoffset:-100}}"
            ".cur{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:12 100;animation:flow 3.2s linear infinite}")
BLUR = '<filter id="blur" x="-30%" y="-300%" width="160%" height="700%"><feGaussianBlur stdDeviation="3"/></filter>'


WRITTEN = set()      # every asset the generator produced (used to give them content-hashed filenames)


def write(name, svg):
    WRITTEN.add(name)
    (OUT / name).write_text(svg, encoding="utf-8")


def wrap(text, width_px, fs, factor=0.53):
    return textwrap.wrap(text, max(6, int(width_px / (fs * factor))), break_on_hyphens=False)


def lines_svg(lines, x, y, fs, fill, lh, weight=400, family=FONT, anchor="start"):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" text-anchor="{anchor}" style="font:{weight} {fs}px {family};fill:{fill}">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )


def pd(pts):
    return "M" + " L".join(f"{x} {y}" for x, y in pts)


def cur(d, col, delay=0.0, dur=3.2, core=3.5, glow=8, base=True):
    """A faint trace with a bright pulse travelling along it (needs BLUR + FLOW_CSS in the svg)."""
    st = f'animation-delay:{delay}s;animation-duration:{dur}s'
    b = f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".13" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>' if base else ""
    return (b + f'<g filter="url(#blur)"><path class="cur" pathLength="100" style="{st}" d="{d}" stroke="{col}" stroke-width="{glow}" stroke-opacity=".45"/></g>'
            f'<path class="cur" pathLength="100" style="{st}" d="{d}" stroke="{col}" stroke-width="{core}"/>')


# ----------------------------------------------------------------- colour maths
def _lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + .05) / (lb + .05)


# ------------------------------------------------------------------- logo inlining
_uid = itertools.count(1)


def _find(slug):
    if not slug:
        return None
    for ext in (".svg", ".png"):
        f = LOGOS / f"{slug}{ext}"
        if f.exists():
            return f
    return None


def has_logo(slug):
    return _find(slug) is not None


LIFT_DARK = {"aws"}   # wordmarks whose dark lettering would vanish on the dark page


def logo(slug, x, y, size, bg=PANEL, plate=True, tint=None):
    """Inline a logo file as a nested <svg>. Ids are made unique, currentColor becomes light ink, and
    a logo whose colours would vanish on the dark background gets a light circular plate."""
    f = _find(slug)
    if not f:
        return None
    if f.suffix == ".png":
        data = base64.b64encode(f.read_bytes()).decode()
        return f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{size}" height="{size}" preserveAspectRatio="xMidYMid meet"/>'
    s = f.read_text()
    m = re.search(r"<svg([^>]*)>", s)
    attrs, inner = m.group(1), s[m.end(): s.rindex("</svg>")]
    vb = re.search(r'viewBox="([^"]+)"', attrs).group(1)
    root_fill = re.search(r'\sfill="([^"]+)"', attrs)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    # editor metadata (Inkscape, RDF, Dublin Core) uses namespaces the page does not declare: drop it
    inner = re.sub(r"<metadata.*?</metadata>", "", inner, flags=re.S)
    inner = re.sub(r"<(sodipodi|inkscape|rdf|cc|dc):(\w+)[^>]*?>.*?</\1:\2>", "", inner, flags=re.S)
    inner = re.sub(r"<(sodipodi|inkscape|rdf|cc|dc):[^>]*?/>", "", inner)
    inner = re.sub(r"\s(?:sodipodi|inkscape|rdf|cc|dc|xml):[\w-]+=\"[^\"]*\"", "", inner)
    uid = next(_uid)
    inner = re.sub(r'\bid="([^"]+)"', lambda mm: f'id="u{uid}_{mm.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda mm: f"url(#u{uid}_{mm.group(1)})", inner)
    inner = re.sub(r'((?:xlink:)?href)="#([^"]+)"', lambda mm: f'{mm.group(1)}="#u{uid}_{mm.group(2)}"', inner)
    inner = inner.replace("currentColor", tint or INK)
    if slug in LIFT_DARK:
        inner = re.sub(r'fill="(#[0-9A-Fa-f]{3,6})"', lambda mm: f'fill="{INK}"' if contrast(mm.group(1), bg) < 2.2 else mm.group(0), inner)
    fill = root_fill.group(1).replace("currentColor", tint or INK) if root_fill else None
    colours = [c for c in re.findall(r'(?:fill|stop-color)="(#[0-9A-Fa-f]{3,6})"', inner)]
    if fill and fill.startswith("#"):
        colours.append(fill)
    plate_svg = ""
    if colours:
        light = [c for c in colours if contrast(c, bg) >= 2.6]
        if not light:
            if fill and fill.startswith("#") and len(colours) == 1:
                fill = INK                      # single-colour mark: just lift it
            elif plate:
                r = size * .62
                plate_svg = f'<circle cx="{x + size / 2}" cy="{y + size / 2}" r="{r:.1f}" fill="{INK}" fill-opacity=".94"/>'
    fa = f' fill="{fill}"' if fill else ""
    for k, v in re.findall(r'\s(stroke(?:-[a-z]+)?)="([^"]+)"', attrs):     # outline icons keep their stroke settings on the root
        fa += f' {k}="{v.replace("currentColor", tint or INK)}"'
    return f'{plate_svg}<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}"{fa}>{inner}</svg>'


def mono_tile(text, col, x, y, size):
    """Stand-in for tools without a public logo: an honest monogram, not an invented mark."""
    fs = size * (.34 if len(text) <= 3 else .27)
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .26:.1f}" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6" stroke-width="1.6"/>'
            f'<text x="{x + size / 2}" y="{y + size / 2 + fs * .36}" text-anchor="middle" style="font:800 {fs:.1f}px {MONO};fill:{col}">{escape(text)}</text>')


def logo_box(slug, x, y, w, h, bg=PANEL2, align="xMinYMid"):
    """Fit a logo (any aspect ratio) inside a w x h box, left-aligned by default. Used for wide company marks."""
    f = _find(slug)
    if not f:
        return None
    if f.suffix == ".png":
        data = base64.b64encode(f.read_bytes()).decode()
        return f'<image href="data:image/png;base64,{data}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{align} meet"/>'
    inner = logo(slug, 0, 0, 100, bg=bg)           # reuse id-rewriting and colour fixes
    m = re.search(r'<svg x="0" y="0" width="100" height="100" viewBox="([^"]+)"(.*?)</svg>', inner, flags=re.S)
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{m.group(1)}" preserveAspectRatio="{align} meet"{m.group(2)}</svg>'


def aspect(slug):
    """Width / height of a logo file (used to give very wide wordmarks a wider slot)."""
    f = _find(slug)
    if not f:
        return 1.0
    if f.suffix == ".png":
        b = f.read_bytes()
        w, h = int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
        return w / h
    m = re.search(r'viewBox="([\d.\s-]+)"', f.read_text())
    if m:
        v = [float(t) for t in m.group(1).split()]
        return v[2] / v[3]
    return 1.0


def round_path(w, h, tl=0, tr=0, br=0, bl=0):
    """Rectangle path with individually rounded corners (so stacked sections can sit flush with no gaps)."""
    return (f"M0 {tl} " + (f"A{tl} {tl} 0 0 1 {tl} 0 " if tl else "") + f"H{w - tr} " + (f"A{tr} {tr} 0 0 1 {w} {tr} " if tr else "")
            + f"V{h - br} " + (f"A{br} {br} 0 0 1 {w - br} {h} " if br else "") + f"H{bl} " + (f"A{bl} {bl} 0 0 1 0 {h - bl} " if bl else "") + "Z")
