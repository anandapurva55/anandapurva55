#!/usr/bin/env python3
"""Generates every visual used by README.md as animated-but-calm SVG.

GitHub never runs JavaScript in READMEs, but it renders SVG (with CSS animation) inside <img>.
Everything here is pure SVG + CSS, honours prefers-reduced-motion, and inlines brand logos from
assets/logos (fetched by scripts/fetch_logos.py) because an SVG shown through <img> cannot load
external images.   Run:  python3 scripts/generate_assets.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_compose
import gen_frame
import gen_hero
import gen_nav
import gen_sections
import gen_repos
import gen_stack
import gen_toolbox
from assetlib import AM, EM, LAV, OUT, ROSE, SKY

if __name__ == "__main__":
    for stale in ("stats.svg", "award.svg", "h-connect.svg", "education.svg", "experience.svg", "h-edu.svg", "h-exp.svg", "pipeline.svg",
                  "h-projects.svg", "h-work.svg", "h-rel.svg", "capabilities.svg", "reliability.svg", "tech.svg", "btn-linkedin.svg",
                  "tile-causal.svg.bak"):
        (OUT / stale).unlink(missing_ok=True)
    gen_hero.hero()
    gen_repos.generate()
    gen_stack.stack()
    n_logo, n_mono = gen_toolbox.toolbox()
    gen_nav.generate(sum(len(g[3]) for g in gen_toolbox.GROUPS))
    gen_hero.cta()
    gen_hero.heading_adaptive("award", "Global award-winning work", AM, LAV, top=25)
    gen_hero.heading_adaptive("academic", "Academic Excellence Award", AM, EM, top=9)
    gen_hero.heading_adaptive("projects", "Built on top of my day job", SKY, EM, top=8)
    gen_hero.heading_adaptive("expertise", "From algorithms to production AI", EM, AM, top=19)
    gen_hero.heading_adaptive("tech", "Tools & technologies I use", LAV, AM, top=19)
    gen_hero.heading_adaptive("contact", "Get in touch", ROSE, AM, top=19)
    for stale in ("h-featured.svg", "h-built.svg", "h-stack.svg", "h-toolbox.svg", "h-about.svg", "btn-email.svg", "btn-whatsapp.svg", "nav-stack.svg", "nav-toolbox.svg", "bar-award.svg", "bar-demo.svg", "sec-award.svg", "sec-projects.svg"):
        (OUT / stale).unlink(missing_ok=True)
    # separate rounded cards with real gaps (transparent margins); the page shows through between them
    # each box is drawn ONCE as a master, then cut into clickable slices at integer coordinates (identical edges, no seams)
    gen_compose.compose("m-top.svg", [(f"nav-{n}.svg", i * 200, 0) for i, n in enumerate(("award", "projects", "expertise", "tech", "contact"))] + [("hero.svg", 0, 84)], base="#0e0f11")
    gen_frame.frame("m-top.svg", 4, 4, rx=22, fill=None, border=False)
    gen_compose.slice_master("m-top.svg", [("top-awards.svg", 0, 0, 204, 88), ("top-projects.svg", 204, 0, 200, 88), ("top-expertise.svg", 404, 0, 200, 88),
                                           ("top-tech.svg", 604, 0, 200, 88), ("top-contact.svg", 804, 0, 204, 88), ("top-hero.svg", 0, 88, 1008, 494)])
    for t in ("claims", "mcp-bench", "multicloud", "causal", "complaint", "taxi"):
        gen_frame.frame(f"tile-{t}.svg", 10, 10, rx=22, fill=None)
    gen_compose.compose("m-contact.svg", [("cta.svg", 0, 0), ("bar-email.svg", 0, 352), ("bar-whatsapp.svg", 500, 352)], base="#17191d")
    gen_frame.frame("m-contact.svg", 4, 4, rx=22, fill=None, border=False)
    gen_compose.slice_master("m-contact.svg", [("contact-card.svg", 0, 0, 1008, 356), ("contact-email.svg", 0, 356, 504, 138), ("contact-whatsapp.svg", 504, 356, 504, 138)])
    gen_frame.frame("stack.svg", 0, 10, rx=22, fill=None)
    gen_frame.frame("toolbox.svg", 0, 10, rx=22, fill=None)
    # Content-hashed filenames. GitHub redirects image requests and drops any ?query, so a version tag is useless;
    # the only reliable cache-buster is a filename that changes whenever the image changes.
    import hashlib, re
    from assetlib import WRITTEN
    readme = Path(__file__).resolve().parent.parent / "README.md"
    txt = readme.read_text()
    for name in sorted(WRITTEN):
        f = OUT / name
        if not f.exists():
            continue
        stem, ext = f.stem, f.suffix
        new = f"{stem}.{hashlib.sha256(f.read_bytes()).hexdigest()[:8]}{ext}"
        for old in OUT.glob(f"{stem}.????????{ext}"):          # drop older hashed copies of the same image
            if old.name != new:
                old.unlink()
        txt = re.sub(rf"assets/{re.escape(stem)}(?:\.[0-9a-f]{{8}})?{re.escape(ext)}(?:\?v=[0-9a-f]+)?", f"assets/{new}", txt)
        f.replace(OUT / new)                                   # the hashed file is the published one
    readme.write_text(txt)
    print(f"assets written: {len([p for p in OUT.iterdir() if p.is_file()])}  (toolbox: {n_logo} logos, {n_mono} monograms)")
