"""The large backing panel behind the boxes of the Expertise and Tech Stack cards: a deep, layered green blend (not a flat fill) with
soft aurora glows drifting slowly and a faint dot field, in the same spirit as the hero card. The boxes drawn on it keep their own colours."""

CSS = ("@keyframes bk-drift{0%,100%{transform:translate(-60px,0)}50%{transform:translate(90px,40px)}}"
       ".bk-a{animation:bk-drift 14s ease-in-out infinite}.bk-b{animation:bk-drift 18s ease-in-out infinite reverse}")

GLOWS = ("#2fe3a2", "#35c6e8", "#8f86f0", "#b6e36a")          # emerald, sky teal, violet, lime


def backing(w, h):
    defs = ('<linearGradient id="bk-base" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#0f3a2b"/><stop offset=".34" stop-color="#0c2a2c"/><stop offset=".66" stop-color="#112a3c"/><stop offset="1" stop-color="#103726"/></linearGradient>'
            + "".join(f'<radialGradient id="bk-g{i}"><stop offset="0" stop-color="{c}" stop-opacity=".42"/><stop offset=".5" stop-color="{c}" stop-opacity=".16"/>'
                      f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>' for i, c in enumerate(GLOWS))
            + '<pattern id="bk-dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.2" fill="#c9ffe6" fill-opacity=".11"/></pattern>'
            + f'<clipPath id="bk-clip"><rect width="{w}" height="{h}"/></clipPath>')
    step, glows, k, y = 330, "", 0, 40
    while y < h + step / 2:                                    # glows alternate down both edges, so tall cards stay rich all the way
        x = w * (.04 if k % 2 == 0 else .96)
        glows += (f'<ellipse class="{"bk-a" if k % 2 == 0 else "bk-b"}" style="animation-delay:{-k * 2.7:.1f}s" cx="{x:.0f}" cy="{y}" rx="{w * .44:.0f}" ry="290" '
                  f'fill="url(#bk-g{k % len(GLOWS)})"/>')
        y += step
        k += 1
    body = (f'<g clip-path="url(#bk-clip)"><rect width="{w}" height="{h}" fill="url(#bk-base)"/>{glows}<rect width="{w}" height="{h}" fill="url(#bk-dots)"/></g>'
            f'<rect width="{w}" height="{h}" fill="none" stroke="#7fe8c0" stroke-opacity=".18"/>')
    return defs, body
