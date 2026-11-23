"""Gives finished SVGs dark gutters (margin) and optional rounded corners.

The page is one dark column. Each image carries its own margin in the page colour, so cards float with space around
them, with no white seams. Rounded outer corners are applied only at the very top and bottom of the column."""
import re
from pathlib import Path

from assetlib import BG, OUT, round_path


def _border(w, h, cr, skip):
    """Outline of a rounded card, leaving out the sides that touch a neighbouring piece (so no seam line is drawn)."""
    tl, tr, br, bl = cr
    segs = [("top", (tl, 0), (w - tr, 0), (tr, w, tr) if tr else None), ("right", (w, tr), (w, h - br), (br, w - br, h) if br else None),
            ("bottom", (w - br, h), (bl, h), (bl, 0, h - bl) if bl else None), ("left", (0, h - bl), (0, tl), (tl, tl, 0) if tl else None)]
    d, pen = "", False
    for name, a, b, arc in segs:
        if name in skip:
            pen = False
            continue
        d += (f"L{a[0]:g} {a[1]:g} " if pen else f"M{a[0]:g} {a[1]:g} ") + f"L{b[0]:g} {b[1]:g} "
        pen = True
        if arc:
            r, ex, ey = arc
            d += f"A{r:g} {r:g} 0 0 1 {ex:g} {ey:g} "
    return d.strip()


def frame(name, mx, my, rx=0, tl=0, tr=0, br=0, bl=0, border=True, fill=BG, radii=None, skip=()):
    f = OUT / name
    myt, myb = my if isinstance(my, tuple) else (my, my)
    mxl, mxr = mx if isinstance(mx, tuple) else (mx, mx)
    mx = mxl
    s = f.read_text()
    root = re.search(r"<svg[^>]*>", s).group(0)
    w = float(re.search(r'\swidth="([\d.]+)', root).group(1))
    h = float(re.search(r'\sheight="([\d.]+)', root).group(1))
    inner = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
    CW, CH = w + mxl + mxr, h + myt + myb
    outer = round_path(CW, CH, tl, tr, br, bl)
    cr = radii if radii is not None else (rx, rx, rx, rx)
    card = round_path(w, h, *cr)
    bcard = round_path(w - 1, h - 1, *[max(c - .5, 0) for c in cr])
    brd = (f'<path transform="translate({mx + .5},{myt + .5})" d="{_border(w - 1, h - 1, [max(c - .5, 0) for c in cr], skip)}" fill="none" stroke="#fff" stroke-opacity=".1"/>'
           if border and (any(cr) or skip) else "")
    f.write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CW:g}" height="{CH:g}" viewBox="0 0 {CW:g} {CH:g}">
  <defs><clipPath id="fr_outer"><path d="{outer}"/></clipPath><clipPath id="fr_card"><path transform="translate({mx},{myt})" d="{card}"/></clipPath></defs>
  <g{' clip-path="url(#fr_outer)"' if fill else ''}>
    {f'<rect width="{CW:g}" height="{CH:g}" fill="{fill}"/>' if fill else ''}
    <g clip-path="url(#fr_card)"><svg x="{mx}" y="{myt}" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}">{inner}</svg></g>
    {brd}
  </g>
</svg>""")
