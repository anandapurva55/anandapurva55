"""Builds each box as ONE master SVG, then cuts it into clickable slices.

Pieces drawn as separate images never share exactly the same edges: each has its own margins and the percentage widths do not sum to
100%. Here the master is drawn once (so tone, glow, dots and rounded outer corners are continuous by construction) and every clickable
slice is simply a window (viewBox) onto that master at integer coordinates, so adjacent slices meet exactly."""
import re

from assetlib import OUT, WRITTEN


def _namespace(svg, p):
    style = "".join(re.findall(r"<style[^>]*>(.*?)</style>", svg, flags=re.S))
    kfs = set(re.findall(r"@keyframes\s+([\w-]+)", style))
    classes = set()
    for m in re.findall(r'\sclass="([^"]+)"', svg):
        classes.update(m.split())
    ids = set(re.findall(r'\sid="([^"]+)"', svg))

    def fix_style(css):
        for k in sorted(kfs, key=len, reverse=True):
            css = re.sub(rf"@keyframes\s+{re.escape(k)}\b", f"@keyframes {p}{k}", css)
            css = re.sub(rf"(animation(?:-name)?\s*:\s*(?:[^;}}]*?\s)?){re.escape(k)}(?=[\s;}}])", rf"\g<1>{p}{k}", css)
        for c in sorted(classes, key=len, reverse=True):
            css = re.sub(rf"\.{re.escape(c)}(?![\w-])", f".{p}{c}", css)
        return css

    svg = re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + fix_style(m.group(2)) + m.group(3), svg, flags=re.S)
    svg = re.sub(r'(\sclass=")([^"]+)(")', lambda m: m.group(1) + " ".join(p + c for c in m.group(2).split()) + m.group(3), svg)
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{p}{i}"').replace(f"url(#{i})", f"url(#{p}{i})").replace(f'href="#{i}"', f'href="#{p}{i}"')
    return svg


def _inner(svg):
    root = re.search(r"<svg[^>]*>", svg).group(0)
    w = float(re.search(r'\swidth="([\d.]+)', root).group(1))
    h = float(re.search(r'\sheight="([\d.]+)', root).group(1))
    return w, h, svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]


def compose(name, pieces, base):
    """pieces: [(file, x, y)] -> master `name` (sources are removed; they are never published on their own)."""
    out, W, H = [], 0, 0
    for k, (f, x, y) in enumerate(pieces):
        w, h, inner = _inner(_namespace((OUT / f).read_text(), f"p{k}_"))
        out.append(f'<svg x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}">{inner}</svg>')
        W, H = max(W, x + w), max(H, y + h)
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:g}" height="{H:g}" viewBox="0 0 {W:g} {H:g}"><rect width="{W:g}" height="{H:g}" fill="{base}"/>{"".join(out)}</svg>', encoding="utf-8")
    for f, _, _ in pieces:
        (OUT / f).unlink(missing_ok=True)
        WRITTEN.discard(f)


def slice_master(master, slices):
    """slices: [(out_name, x, y, w, h)] windows onto the master; the master itself is removed afterwards."""
    _, _, inner = _inner((OUT / master).read_text())
    W, H, _ = _inner((OUT / master).read_text())
    for name, x, y, w, h in slices:
        (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="{x:g} {y:g} {w:g} {h:g}">{inner}</svg>', encoding="utf-8")
        WRITTEN.add(name)
    (OUT / master).unlink(missing_ok=True)
    WRITTEN.discard(master)
