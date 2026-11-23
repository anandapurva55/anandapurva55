"""The six open-source repos as tiles. Each has its own diagram with a "current" flowing through it,
headline results taken from the repo's own README, and the full list of technologies it uses."""
import math

from assetlib import (ORANGE, AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, PANEL, PANEL2, RM, ROSE, SKY, cur, escape,
                      lines_svg, logo, pd, wrap, write)


# ------------------------------------------------------------------ small blocks
def stats_row(items, x, y, w, col):
    n = len(items)
    cw = w / n
    out, maxl = "", 1
    for i, (big, cap) in enumerate(items):
        cx = x + i * cw
        caps = wrap(cap, cw - 16, 11.5, .55)
        maxl = max(maxl, len(caps))
        if i:
            out += f'<line x1="{cx - 10}" y1="{y}" x2="{cx - 10}" y2="{y + 30 + len(caps) * 15}" stroke="#fff" stroke-opacity=".1"/>'
        out += f'<text x="{cx}" y="{y + 26}" style="font:800 26px {FONT};fill:{col}">{escape(big)}</text>'
        out += lines_svg(caps, cx, y + 45, 11.5, MUTED, 15)
    return out, y + 36 + maxl * 15


def tools_block(groups, col, x, y, w, label_w, fs=12.5):
    out, yy = "", y
    for label, text in groups:
        lines = wrap(text, w - label_w, fs, .54)
        out += f'<text x="{x}" y="{yy + 11}" style="font:700 10.5px {MONO};fill:{col};letter-spacing:1.3px">{escape(label)}</text>'
        out += lines_svg(lines, x + label_w, yy + 12, fs, BODY, 18)
        yy += len(lines) * 18 + 9
    return out, yy


def node(x, y, w, h, title, sub, col, fs=13.5, subfs=10, fill=PANEL2, sw=1.6):
    t = f'<text x="{x + w / 2}" y="{y + h / 2 + (-1 if sub else 5)}" text-anchor="middle" style="font:700 {fs}px {FONT};fill:{INK}">{escape(title)}</text>'
    s = f'<text x="{x + w / 2}" y="{y + h / 2 + 15}" text-anchor="middle" style="font:500 {subfs}px {MONO};fill:{MUTED}">{escape(sub)}</text>' if sub else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{col}" stroke-opacity=".6" stroke-width="{sw}"/>{t}{s}'


def pill(x, y, w, h, text, col, fs=11):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".6"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + fs * .36}" text-anchor="middle" style="font:700 {fs}px {MONO};fill:{INK}">{escape(text)}</text>')


# ------------------------------------------------------------------- diagrams
def d_claims(x, y, w, h, col):
    nodes = [("Claim files", "S3 + BDA"), ("Guardrails", "attack filter"), ("Agents", "Strands graph"), ("Rules engine", "code decides"), ("Human", "signs off")]
    n, nw, nh = 5, 92, 60
    gap = (w - n * nw) / (n - 1)
    cy = y + h * .54
    xs = [x + i * (nw + gap) for i in range(n)]
    out = cur(pd([(xs[0] + nw / 2, cy), (xs[-1] + nw / 2, cy)]), col, 0, 4.6, 3.4, 8)
    out += cur(pd([(xs[0] + nw / 2, cy), (xs[-1] + nw / 2, cy)]), AM, 2.3, 4.6, 3.4, 8, base=False)
    for i, (t, s) in enumerate(nodes):
        out += node(xs[i], cy - nh / 2, nw, nh, t, s, AM if i == 4 else col, sw=2 if i == 4 else 1.6, fill=PANEL2)
    ax = xs[2]
    # tools and memory feeding the agents, each with its own short current
    for j, (lab, dx) in enumerate((("RAG", -8), ("MCP", nw - 46))):
        px = ax + dx
        sc = (EM, LAV)[j]
        out += cur(pd([(px + 27, y + 34), (px + 27, cy - nh / 2)]), sc, .4 + j * .7, 2.2, 3, 6)
        out += pill(px, y + 8, 54, 26, lab, sc)
    out += cur(pd([(ax + nw / 2, y + h - 36), (ax + nw / 2, cy + nh / 2)]), ROSE, 1.1, 2.2, 3, 6)
    out += pill(ax + nw / 2 - 34, y + h - 34, 68, 26, "Memory", ROSE)
    out += f'<text x="{xs[4] + nw / 2}" y="{cy + nh / 2 + 26}" text-anchor="middle" style="font:700 10px {MONO};fill:{AM};letter-spacing:1.2px">HUMAN GATE</text>'
    return out


def d_mcp(x, y, w, h, col):
    out = ""
    ys = [y + 22, y + 56, y + 90]
    for lab, yy in zip("ABC", ys):
        out += (f'<rect x="{x}" y="{yy}" width="46" height="26" rx="7" fill="{PANEL2}" stroke="{MUTED}" stroke-opacity=".6"/>'
                f'<text x="{x + 23}" y="{yy + 17}" text-anchor="middle" style="font:700 12px {MONO};fill:{BODY}">{lab}</text>')
        out += cur(pd([(x + 46, yy + 13), (x + 84, y + 78)]), col, ys.index(yy) * .5, 3.4, 2.6, 6)
    out += f'<text x="{x + 23}" y="{y + 134}" text-anchor="middle" style="font:800 20px {FONT};fill:{AM}">≠</text>'
    sx, sw = x + 84, 226
    out += (f'<rect x="{sx}" y="{y + 4}" width="{sw}" height="{h - 8}" rx="14" fill="{col}" fill-opacity=".05" stroke="{col}" stroke-width="1.6" stroke-dasharray="6 5"/>'
            f'<text x="{sx + 14}" y="{y + 24}" style="font:700 10px {MONO};fill:{col};letter-spacing:1.4px">NO NETWORK · READ-ONLY</text>')
    ax, ay = sx + 48, y + 84
    out += f'<circle cx="{ax}" cy="{ay}" r="24" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2"/><text x="{ax}" y="{ay + 4}" text-anchor="middle" style="font:800 11px {MONO};fill:{INK}">Agent</text>'
    for k, (lab, tx, ty) in enumerate((("fs", sx + 138, y + 44), ("code", sx + 182, y + 44), ("git", sx + 138, y + 98), ("calc", sx + 182, y + 98))):
        out += cur(pd([(ax + 24, ay), (tx + 18, ty + 11)]), SKY, k * .45, 2.8, 2.4, 5)
        out += f'<rect x="{tx}" y="{ty}" width="36" height="22" rx="6" fill="{PANEL2}" stroke="{SKY}" stroke-opacity=".6"/><text x="{tx + 18}" y="{ty + 15}" text-anchor="middle" style="font:700 10.5px {MONO};fill:{INK}">{lab}</text>'
    jx, jy = x + w - 36, y + 96
    out += cur(pd([(sx + sw, jy), (jx - 28, jy)]), AM, .9, 3, 3, 7)
    out += (f'<circle cx="{jx}" cy="{jy}" r="26" fill="{AM}" fill-opacity=".14" stroke="{AM}" stroke-width="2"/>'
            f'<text x="{jx}" y="{jy - 3}" text-anchor="middle" style="font:800 11px {MONO};fill:{INK}">Judge</text>'
            f'<text x="{jx}" y="{jy + 11}" text-anchor="middle" style="font:600 9.5px {MONO};fill:{AM}">15/15</text>')
    out += (f'<path d="M{sx + sw} {y + 30} L{x + w - 52} {y + 18}" stroke="{AM}" stroke-width="2" stroke-dasharray="3 5" fill="none"/>'
            f'<path d="M{x + w - 140} {y + 25} l10 10 m0 -10 l-10 10" stroke="{AM}" stroke-width="2.4" stroke-linecap="round" transform="translate(6,0)"/>'
            f'<text x="{x + w - 6}" y="{y + 20}" text-anchor="end" style="font:700 10px {MONO};fill:{MUTED}">web</text>')
    return out


def d_causal(x, y, w, h, col):
    cw = 250
    ax_y = y + h - 22
    out = (f'<line x1="{x}" y1="{ax_y}" x2="{x + cw}" y2="{ax_y}" stroke="{MUTED}" stroke-opacity=".6"/><line x1="{x}" y1="{y + 4}" x2="{x}" y2="{ax_y}" stroke="{MUTED}" stroke-opacity=".6"/>')
    xi = x + cw * .48
    out += f'<line x1="{xi}" y1="{y + 4}" x2="{xi}" y2="{ax_y}" stroke="{MUTED}" stroke-dasharray="3 4"/><text x="{xi + 6}" y="{y + 14}" style="font:600 10px {MONO};fill:{MUTED}">adoption</text>'
    out += f'<path d="M{x + 6} {y + 86} L{x + cw - 4} {y + 70}" stroke="{MUTED}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    out += f'<text x="{x + cw - 4}" y="{y + 94}" text-anchor="end" style="font:600 10px {MONO};fill:{MUTED}">control</text>'
    tr = f"M{x + 6} {y + 86} L{xi} {y + 80} L{x + cw - 4} {y + 24}"
    out += f'<path class="draw" pathLength="100" d="{tr}" fill="none" stroke="{col}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
    out += f'<text x="{x + cw - 4}" y="{y + 16}" text-anchor="end" style="font:700 10px {MONO};fill:{col}">treated</text>'
    bx = x + cw + 34
    rows = (("TRUE", 3.18, EM, "−3.18"), ("C-S", 2.96, SKY, "−2.96"), ("TWFE", 2.58, AM, "−2.58 biased"))
    for i, (lab, v, c, txt) in enumerate(rows):
        yy = y + 20 + i * 38
        out += f'<text x="{bx}" y="{yy}" style="font:700 10px {MONO};fill:{MUTED};letter-spacing:1px">{lab}</text>'
        out += f'<rect x="{bx}" y="{yy + 6}" width="{v / 3.18 * 100:.0f}" height="9" rx="4.5" fill="{c}" class="gbar" style="animation-delay:{i * .25}s"/>'
        out += f'<text x="{bx + v / 3.18 * 100 + 6:.0f}" y="{yy + 14}" style="font:700 10.5px {MONO};fill:{INK}">{txt}</text>'
    return out


def d_hybrid(x, y, w, h, col):
    cy = y + h * .44
    ns = [("Feedback", 0, 64), ("DistilBERT", 82, 82), ("Calibrate", 182, 70), ("Rules", 270, 56)]
    out = cur(pd([(x + 32, cy), (x + 326, cy)]), col, 0, 3.4, 3.2, 7)
    for t, nx, nw in ns:
        out += node(x + nx, cy - 19, nw, 38, t, "", col, fs=11.5)
    outs = (("Auto-reply", EM, -50), ("Review", AM, 0), ("Escalate", ORANGE, 50))
    for k, (t, c, dy) in enumerate(outs):
        out += cur(pd([(x + 326, cy), (x + 344, cy), (x + 344, cy + dy), (x + 360, cy + dy)]), c, .6 + k * .5, 2.8, 3, 6)
        out += pill(x + 360, cy + dy - 14, w - 360, 28, t, c, 11.5)
    py = y + h - 24
    out += (f'<path d="M{x + 298} {cy + 19} V{py - 4}" stroke="{LAV}" stroke-width="2" stroke-dasharray="3 4" fill="none"/>'
            f'<rect x="{x + 70}" y="{py - 4}" width="264" height="28" rx="14" fill="{LAV}" fill-opacity=".12" stroke="{LAV}" stroke-opacity=".6"/>'
            f'<text x="{x + 70 + 132}" y="{py + 14}" text-anchor="middle" style="font:700 11px {MONO};fill:{INK}">LLM explains only · Nova Lite</text>')
    return out


def d_multicloud(x, y, w, h, col):
    cy = y + h / 2
    out = cur(pd([(x + 76, cy), (x + 104, cy)]), col, 0, 2.6, 3.2, 7)
    out += node(x, cy - 30, 76, 60, "AI client", "MCP · stdio", col, fs=12.5, subfs=9.5)
    out += node(x + 104, cy - 36, 92, 72, "server.py", "read-only", col, fs=13, subfs=10.5, sw=2)
    for k, (cy2, c, lab, icons) in enumerate(((y + 33, SKY, "GOOGLE CLOUD", ["bigquery", "cloudrun", "cloudbuild", "googlecloudstorage"]),
                                               (y + h - 33, AM, "AWS", ["athena", "ecs", "lambda", "codebuild", "s3", "cloudwatch"]))):
        out += cur(pd([(x + 196, cy), (x + 214, cy), (x + 214, cy2), (x + 232, cy2)]), c, .7 + k * .6, 3, 3.2, 7)
        bx, bw = x + 232, w - 232
        out += f'<rect x="{bx}" y="{cy2 - 31}" width="{bw}" height="62" rx="14" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".55"/>'
        out += f'<text x="{bx + 14}" y="{cy2 - 14}" style="font:700 9.5px {MONO};fill:{c};letter-spacing:1.3px">{lab}</text>'
        for j, ic in enumerate(icons):
            out += logo(ic, bx + 14 + j * 31, cy2 - 6, 24, bg=PANEL) or ""
    return out


def d_nyc(x, y, w, h, col):
    n, split = 60, 42
    pts = []
    for i in range(n):
        px = x + w * i / (n - 1)
        v = .5 + .28 * math.sin(i / 4.1) + .12 * math.sin(i / 1.7) + i * .003
        pts.append((px, y + 8 + (1 - v) * 78))
    solid = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts[:split])
    dash = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts[split - 1:])
    sx = pts[split - 1][0]
    out = f'<rect x="{sx:.1f}" y="{y}" width="{x + w - sx:.1f}" height="96" rx="8" fill="{col}" fill-opacity=".1"/>'
    out += cur(solid, col, 0, 5.2, 3.2, 7)
    out += f'<path d="{dash}" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="2 6" stroke-linecap="round"/>'
    out += f'<text x="{x + w - 8}" y="{y + 90}" text-anchor="end" style="font:700 10.5px {MONO};fill:{col}">next-hour forecast · 254 zones</text>'
    nodes = [("Data", "3M trips"), ("Train", "XGB · LGBM"), ("Registry", "MLflow"), ("Serve", "FastAPI · ECS"), ("Monitor", "drift · SageMaker")]
    n_, nw, nh = 5, 92, 50
    gap = (w - n_ * nw) / (n_ - 1)
    cy = y + 150
    xs = [x + i * (nw + gap) for i in range(n_)]
    out += cur(pd([(xs[0] + nw / 2, cy), (xs[-1] + nw / 2, cy)]), EM, 0, 4.4, 3.4, 8)
    for i, (t, s) in enumerate(nodes):
        out += node(xs[i], cy - nh / 2, nw, nh, t, s, EM if i < 4 else SKY, fs=13, subfs=9)
    loop = pd([(xs[4] + nw / 2, cy + nh / 2), (xs[4] + nw / 2, cy + 52), (xs[1] + nw / 2, cy + 52), (xs[1] + nw / 2, cy + nh / 2)])
    out += cur(loop, SKY, 1.2, 4.4, 3, 7)
    out += f'<text x="{(xs[1] + xs[4]) / 2 + nw / 2}" y="{cy + 70}" text-anchor="middle" style="font:700 10px {MONO};fill:{SKY};letter-spacing:1.2px">DRIFT  →  RETRAIN</text>'
    return out


# ------------------------------------------------------------------- motifs
def motif(kind, w, h, col):
    o = ""
    if kind == "dots":
        o = f'<pattern id="mt" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".08"/></pattern><rect width="{w}" height="{h}" fill="url(#mt)"/>'
    elif kind == "hatch":
        o = f'<pattern id="mt" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="14" stroke="{col}" stroke-opacity=".07" stroke-width="2"/></pattern><rect width="{w}" height="{h}" fill="url(#mt)"/>'
    elif kind == "grid":
        o = f'<pattern id="mt" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern><rect width="{w}" height="{h}" fill="url(#mt)"/>'
    elif kind == "arcs":
        o = "".join(f'<circle cx="{w}" cy="0" r="{r}" fill="none" stroke="{col}" stroke-opacity=".08"/>' for r in (80, 130, 180, 230))
    elif kind == "hex":
        o = f'<pattern id="mt" width="34" height="30" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="1.6" fill="{col}" fill-opacity=".14"/><circle cx="21" cy="19" r="1.6" fill="{col}" fill-opacity=".14"/></pattern><rect width="{w}" height="{h}" fill="url(#mt)"/>'
    return o


# ---------------------------------------------------------------------- tiles
TILES = [
    dict(file="tile-claims.svg", wide=True, n="01", flag="FLAGSHIP · AWS", col=SKY, draw=d_claims, dh=230, motif="dots",
         title="Agentic Claims Adjudication",
         desc="Multi-agent AI that reads a motor claim, retrieves the policy wording and recommends a decision. Plain code calculates the payout, and a person always signs off.",
         stats=[("98.7%", "decision accuracy on 78 held-out claims"), ("0", "red-team attacks succeeded (29)"), ("$0.035", "model cost per claim, optimised"), ("523", "automated tests")],
         tools=[("AI · AGENTS", "Strands Agents · MCP · Amazon Bedrock (Nova 2 Lite, Claude Haiku 4.5, Claude Sonnet 4.6) · Bedrock Guardrails · Knowledge Bases on S3 Vectors · Titan Text Embeddings V2 · Bedrock Data Automation · AgentCore Memory · RAG · QLoRA fine-tuning (Transformers, PEFT, TRL, bitsandbytes) on SageMaker"),
                ("APP", "Python 3.12 · FastAPI · Pydantic · boto3 · React 19 · TypeScript · Vite · Vitest · uv"),
                ("AWS", "ECS Fargate · ALB · CloudFront · WAF · Cognito · Secrets Manager · S3 · DynamoDB · Glue · Athena · QuickSight · CloudWatch · AWS CDK"),
                ("QUALITY", "pytest · moto · Ruff · mypy · GitHub Actions · CodeQL · Dependabot · GitHub Pages · red-team suite")]),
    dict(file="tile-mcp-bench.svg", wide=False, n="02", flag="AGENT EVALS", col=ORANGE, draw=d_mcp, dh=140, motif="hatch",
         title="Conflicting-Evidence Benchmark",
         desc="Do tool-using agents reconcile sources that disagree? Docker sandboxes with no network, MCP tools, and answers graded claim by claim by a calibrated LLM judge.",
         stats=[("3", "scenarios"), ("4", "MCP servers"), ("15/15", "judge calibration"), ("0", "network access")],
         tools=[("AGENT · JUDGE", "Qwen 2.5 7B agent via Ollama · GPT-4.1 mini judge · claim-based LLM grading"),
                ("SANDBOX", "MCP servers (filesystem, code execution, git, calculator) · Docker, read-only and no network"),
                ("BUILD", "Python 3.11 · PyYAML · httpx · uv · pytest · Ruff · GitHub Actions · CodeQL")]),
    dict(file="tile-multicloud.svg", wide=False, n="03", flag="MCP SERVER", col=LAV, draw=d_multicloud, dh=140, motif="hex",
         title="Multi-Cloud MCP Server",
         desc="A read-only MCP server that lets AI clients inspect your own GCP and AWS: run SQL, check builds and deployments, read logs, behind safety and cost guards.",
         stats=[("2", "clouds"), ("10", "cloud services"), ("1", "server, many clients")],
         tools=[("MCP", "Python · MCP (FastMCP, stdio) · works with Claude Code, Codex, Cursor, GitHub Copilot"),
                ("GOOGLE CLOUD", "BigQuery · Cloud Run · Cloud Build · Cloud Logging · Cloud Storage · Google Cloud client libraries"),
                ("AWS", "Athena · Glue Data Catalog · S3 · ECS · Lambda · CodeBuild · CloudWatch Logs · boto3"),
                ("QUALITY", "pytest · moto · GitHub Actions")]),
    dict(file="tile-causal.svg", wide=False, n="04", flag="BENCHMARK", col=EM, draw=d_causal, dh=140, motif="grid",
         title="Causal Inference Agent Benchmark",
         desc="Can an LLM act as a data scientist? Six Gemini models run survival analysis, staggered difference-in-differences, treatment-effect heterogeneity and mixed models on synthetic hospital data with known truth.",
         stats=[("6", "Gemini models"), ("14", "automated tests"), ("4", "methods chained")],
         tools=[("METHODS", "Kaplan-Meier · Cox proportional hazards · staggered DiD (TWFE, Callaway-Sant'Anna) · heterogeneous treatment effects · mixed-effects models"),
                ("PYTHON 3.12", "pandas · NumPy · SciPy · statsmodels · lifelines · linearmodels · scikit-learn · Matplotlib · seaborn"),
                ("LLM + TOOLS", "Gemini API (google-genai) · Jupyter (jupytext, nbconvert) · pytest · GitHub Actions")]),
    dict(file="tile-complaint.svg", wide=False, n="05", flag="HYBRID AI", col=ROSE, draw=d_hybrid, dh=140, motif="arcs",
         title="Hybrid Complaint Risk AI",
         desc="Triage for customer feedback: a fine-tuned DistilBERT, a calibrated decision layer and review rules choose the action. The LLM only explains it.",
         stats=[("0.69", "macro-F1"), ("346/355", "high-risk cases reach a person"), ("71%", "answered automatically")],
         tools=[("MODELS", "DistilBERT fine-tuned with PyTorch and Hugging Face Transformers (int8) · scikit-learn (TF-IDF, logistic regression baseline) · NumPy decision layer with temperature calibration · TensorFlow and Keras LSTM baseline"),
                ("LLM", "Amazon Bedrock (Nova Lite) for explanations"),
                ("SERVING", "FastAPI · Pydantic · Docker · ECS Fargate · ALB · CloudFront · WAF · Secrets Manager · CloudFormation · CloudWatch (EMF metrics, alarms) · GitHub Actions with OIDC · pytest")]),
    dict(file="tile-taxi.svg", wide=True, n="06", flag="MLOPS · AWS", col=AM, draw=d_nyc, dh=230, motif="grid",
         title="NYC Taxi Demand and Fare Forecasting",
         desc="End-to-end MLOps: forecast hourly pickups across 254 New York zones and quote fares, tracked in MLflow, served on AWS, monitored for drift and defined entirely in Terraform.",
         stats=[("0.968", "demand model R²"), ("0.962", "fare model R²"), ("373 ms", "p95 latency over HTTPS"), ("68", "AWS resources in Terraform")],
         tools=[("MODELS · DATA", "XGBoost · LightGBM · scikit-learn · Optuna · pandas · NumPy · PyArrow · SciPy · SHAP · Evidently"),
                ("MLOPS", "MLflow 3 · skops · uv · Docker · Terraform · GitHub Actions · CodeBuild · ECR · Dependabot"),
                ("SERVING · APP", "FastAPI · Pydantic · Uvicorn · Prometheus · Streamlit · Plotly · stlite · GitHub Pages"),
                ("AWS", "ECS Fargate · ALB · CloudFront · VPC · IAM · Parameter Store · S3 · Glue · Athena · CloudWatch · Data Firehose · SNS · SageMaker Processing and Pipelines · EventBridge Scheduler"),
                ("QUALITY", "pytest · Ruff · pip-audit")]),
]


def build(t, h=None):
    wide = t["wide"]
    w = 1000 if wide else 500
    col, pad = t["col"], 28
    body = ""
    if wide:
        tw = 380
        tl = wrap(t["title"], tw, 30, .56)
        body += lines_svg(tl, pad, 82, 30, INK, 36, 800)
        dl = wrap(t["desc"], tw, 15)
        yy = 82 + (len(tl) - 1) * 36 + 30
        body += lines_svg(dl, pad, yy, 15, BODY, 23)
        left_bottom = yy + len(dl) * 23
        dx, dy, dw = 440, 56, w - 440 - pad
        body += t["draw"](dx, dy, dw, t["dh"], col)
        y = max(left_bottom, dy + t["dh"]) + 26
        label_w = 124
    else:
        tw = w - 2 * pad
        tl = wrap(t["title"], tw, 23, .56)
        body += lines_svg(tl, pad, 76, 23, INK, 28, 800)
        dl = wrap(t["desc"], tw, 14)
        yy = 76 + (len(tl) - 1) * 28 + 26
        body += lines_svg(dl, pad, yy, 14, BODY, 20)
        dy = yy + len(dl) * 20 + 16
        body += t["draw"](pad, dy, tw, t["dh"], col)
        y = dy + t["dh"] + 24
        label_w = 116
    sx, y2 = stats_row(t["stats"], pad, y, w - 2 * pad, col)
    body += sx
    tb, y3 = tools_block(t["tools"], col, pad, y2 + 6, w - 2 * pad, label_w, 12.5)
    body += f'<line x1="{pad}" y1="{y2 - 2}" x2="{w - pad}" y2="{y2 - 2}" stroke="#fff" stroke-opacity=".09"/>' + tb
    nat = y3 + 20
    return w, nat, body


def render(t, w, h, body):
    col = t["col"]
    css = ("@keyframes draw{0%{stroke-dashoffset:100;opacity:1}55%{stroke-dashoffset:0}92%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}"
           "@keyframes gbar{from{transform:scaleX(.04)}35%,100%{transform:scaleX(1)}}"
           ".draw{stroke-dasharray:100;animation:draw 6.5s ease-in-out infinite}"
           ".gbar{transform-box:fill-box;transform-origin:0 50%;animation:gbar 6.5s ease-out infinite}" + FLOW_CSS + RM)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <radialGradient id="gl" cx="1" cy="0" r="1"><stop offset="0" stop-color="{col}" stop-opacity=".2"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
    {BLUR}
    <clipPath id="c"><rect width="{w}" height="{h}"/></clipPath>
  </defs>
  <style>{css}</style>
  <g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{PANEL}"/>{motif(t["motif"], w, h, col)}<rect width="{w}" height="{h}" fill="url(#gl)"/></g>
  <rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" fill="none" stroke="{col}" stroke-opacity=".42" stroke-width="1.5"/>
  <text x="28" y="38" style="font:800 13px {MONO};fill:{col};letter-spacing:2px">{t["n"]} · {t["flag"]}</text>
  <text x="{w - 28}" y="38" text-anchor="end" style="font:600 12px {MONO};fill:{MUTED};letter-spacing:1px">VIEW REPO ↗</text>
  {body}
</svg>"""


def generate():
    built = {t["file"]: (t,) + build(t) for t in TILES}
    rows = [["tile-claims.svg"], ["tile-mcp-bench.svg", "tile-multicloud.svg"], ["tile-causal.svg", "tile-complaint.svg"], ["tile-taxi.svg"]]
    for row in rows:
        h = max(built[f][2] for f in row)
        for f in row:
            t, w, _, body = built[f]
            write(f, render(t, w, h, body))
