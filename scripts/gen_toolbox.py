"""Toolbox as a logo wall: real brand marks, no per-tool boxes, with a slow wave of light across it."""
from gen_backing import CSS as BK_CSS, backing
from assetlib import (aspect, logo_box, AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, PANEL, RM, ROSE, SKY, cur, escape, has_logo, logo,
                      mono_tile, pd, wrap, write)

# (label, logo slug or None, monogram for tools that have no public logo)
# Soft, soothing colours, one per skill set. No red, no black; chosen so every pair stays visibly different (CIEDE2000 >= 14)
# and each reads clearly on the dark card.
PALETTE = {
    "GENERATIVE": "#b09ee5",   # lavender: imagination
    "ML & DATA":  "#b0d46a",   # pistachio: models that grow
    "DATA & ANA": "#9fe0f5",   # sky: flowing data
    "MLOPS":      "#4fc3bb",   # sea teal: a steady pipeline
    "AMAZON":     "#efa467",   # apricot: AWS
    "GOOGLE":     "#6f9ee8",   # cornflower: Google Cloud
    "SECURITY":   "#f6dc80",   # butter: a watchful light
    "BACKEND":    "#cc6fe2",   # plum: services behind the scenes
    "FRONTEND":   "#e99cca",   # orchid pink: design
    "AI CODING":  "#e3c3b4",   # almond: a companion
    "LANGUAGES":  "#66cc8a",   # leaf green: code
}


GROUPS = [
    # (title, colour, badge logo for the title, items, "also" line for tools without a public logo)
    ("GENERATIVE & AGENTIC AI", PALETTE["GENERATIVE"], None,
     [("MCP", "mcp"), ("RAG", "i-rag"), ("Semantic Search", "i-semantic"), ("Embeddings", "i-embed"), ("Fine-tuning (SFT)", "i-finetune"),
      ("LoRA / QLoRA", "i-qlora"), ("Prompt Engineering", "i-prompt"), ("LLM-as-a-Judge", "i-judge"), ("Strands Agents", "strands"),
      ("AutoGen", "autogen"), ("LangChain", "langchain-i"), ("Hugging Face", "huggingface"), ("Claude", "claude"), ("Gemini", "googlegemini"),
      ("GPT", "openai"), ("Llama", "meta"), ("Qwen", "qwen"), ("Amazon Nova", "nova"), ("Ollama", "ollama")],
     None),
    ("ML & DATA SCIENCE", PALETTE["ML & DATA"], None,
     [("PyTorch", "pytorch"), ("TensorFlow", "tensorflow"), ("Keras", "keras"), ("scikit-learn", "scikitlearn"), ("XGBoost", "xgboost"),
      ("LightGBM", "lightgbm"), ("Optuna", "optuna"), ("SHAP", "shap"), ("statsmodels", "statsmodels"), ("linearmodels", "linearmodels"),
      ("NumPy", "numpy"), ("Pandas", "pandas"), ("SciPy", "scipy"), ("Matplotlib", "matplotlib"), ("seaborn", "seaborn"),
      ("Jupyter", "jupyter"), ("Gurobi", "gurobi"), ("Ray", "ray"), ("NLTK", "nltk"), ("lifelines", "lifelines")],
     None),
    ("DATA & ANALYTICS", PALETTE["DATA & ANA"], None,
     [("Snowflake", "snowflake"), ("PostgreSQL", "postgresql"), ("SQLite", "sqlite"), ("Apache Spark", "apachespark"),
      ("Apache Arrow", "apachearrow"), ("Tableau", "tableau")],
     None),
    ("MLOPS", PALETTE["MLOPS"], None,
     [("MLflow", "mlflow"), ("Evidently", "evidently-light"), ("Terraform", "terraform"), ("Docker", "docker"), ("Kubernetes", "kubernetes"),
      ("GitHub Actions", "githubactions"), ("Tekton", "tekton")],
     None),
    ("AMAZON WEB SERVICES (AWS)", PALETTE["AMAZON"], "aws",
     [("Bedrock", "bedrock"), ("SageMaker", "sagemaker"), ("Lambda", "lambda"), ("EC2", "ec2"), ("ECS", "ecs"), ("Fargate", "fargate"),
      ("App Runner", "apprunner"), ("S3", "s3"), ("DynamoDB", "dynamodb"), ("RDS", "rds"), ("Glue", "glue"), ("Athena", "athena"),
      ("OpenSearch", "opensearch"), ("CloudFront", "cloudfront"), ("CloudWatch", "cloudwatch"), ("Step Functions", "stepfunctions"),
      ("Cognito", "cognito"), ("WAF", "waf"), ("IAM", "iam"), ("EventBridge", "eventbridge"), ("QuickSight", "quicksight"),
      ("CloudFormation", "cloudformation"), ("CDK", "cdk"), ("CodeBuild", "codebuild"), ("ECR", "ecr"),
      ("Secrets Manager", "secretsmanager"), ("Load Balancer", "elb"), ("SNS", "sns"), ("VPC", "vpc"), ("Systems Manager", "ssm")],
     None),
    ("GOOGLE CLOUD PLATFORM (GCP)", PALETTE["GOOGLE"], "googlecloud",
     [("BigQuery", "bigquery"), ("Cloud Run", "cloudrun"), ("Cloud Build", "cloudbuild"), ("Cloud Storage", "googlecloudstorage"),
      ("Cloud Logging", "cloudlogging"), ("Cloud Scheduler", "cloudscheduler"), ("Vertex AI", "vertexai"), ("Apigee", "apigee"),
      ("Model Armor", "modelarmor")],
     None),
    ("SECURITY & OBSERVABILITY", PALETTE["SECURITY"], None,
     [("Dynatrace", "dynatrace"), ("Prometheus", "prometheus"), ("SonarQube", "sonar"), ("FOSSA", "fossa-bear"), ("Cycode", "cycode"),
      ("Dependabot", "dependabot"), ("CodeQL", "codeql"), ("CodeGuardian", "codeguardian", "CG"), ("Entra ID", "entra")],
     None),
    ("BACKEND & APIS", PALETTE["BACKEND"], None,
     [("FastAPI", "fastapi"), ("Pydantic", "pydantic"), ("Uvicorn", "uvicorn"), ("WhatsApp API", "whatsapp")],
     None),
    ("FRONTEND & DATA APPS", PALETTE["FRONTEND"], None,
     [("React", "react"), ("TypeScript", "typescript"), ("Vite", "vite"), ("Streamlit", "streamlit")],
     None),
    ("AI CODING ASSISTANTS", PALETTE["AI CODING"], None,
     [("Claude Code", "claudecode"), ("Codex", "codex"), ("GitHub Copilot", "githubcopilot"), ("Google Antigravity", "antigravity")],
     None),
    ("LANGUAGES & DEV TOOLS", PALETTE["LANGUAGES"], None,
     [("Python", "python"), ("SQL", "sql"), ("GitHub", "github"), ("VS Code", "vscode"), ("Cursor", "cursor"), ("Postman", "postman"), ("Hoppscotch", "hoppscotch"),
      ("Jira", "jira"), ("pytest", "pytest")],
     None),
]


def toolbox():
    from gen_signatures import CSS as SIG_CSS, scene
    W, cols, cw, rh = 1000, 10, 100, 100
    y, out, n_logo, n_mono = 0, "", 0, 0
    adefs = ""
    y = 2                      # the first box sits as close to the top edge as the boxes do to the sides (14)
    for gi, (title, col, badge, items, also) in enumerate(GROUPS):
        bx, y0, before = 0, y, out
        out = ""
        if badge:                                  # brand badge lives in the title, so the grid does not repeat it
            out += logo(badge, 0, y - 6, 34, bg=BG) or ""
            bx = 46
        out += f'<text x="{bx}" y="{y + 20}" style="font:800 14px {MONO};fill:{col};letter-spacing:2.6px">{escape(title)}</text>'
        tx = bx + 40 + len(title) * 10.4
        y += 44
        for k, item in enumerate(items):
            name, slug = item[0], item[1]
            r, c = divmod(k, cols)
            cx = c * cw + cw / 2
            top = y + r * rh
            if slug and aspect(slug) > 2.2:            # wide wordmarks get a wider slot so they stay legible
                mark = logo_box(slug, cx - 47, top + 2, 94, 40, bg=BG, align="xMidYMid")
            else:
                mark = logo(slug, cx - 22, top, 44, bg=BG, tint=col if slug.startswith("i-") else None) if slug else None
            if mark is None:
                mark = mono_tile(item[2] if len(item) > 2 else name[:3].upper(), col, cx - 22, top, 44)
                n_mono += 1
            else:
                n_logo += 1
            label = lines_for(name)
            lab = "".join(f'<text x="{cx}" y="{top + 66 + i * 14}" text-anchor="middle" style="font:600 {11.5 if len(l) <= 12 else 10.5}px {MONO};fill:{BODY}">{escape(l)}</text>' for i, l in enumerate(label))
            out += mark + lab
        y += ((len(items) - 1) // cols + 1) * rh
        # the skill set's own box: an aurora in its colour that is always there, drifting slowly inside the box
        bx0, by0, bw, bh = -14, y0 - 16, W + 28, y - y0 + 14
        adefs += (f'<radialGradient id="a{gi}"><stop offset="0" stop-color="{col}" stop-opacity=".30"/><stop offset=".55" stop-color="{col}" stop-opacity=".13"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
                  f'<clipPath id="c{gi}"><rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="20"/></clipPath>')
        ry = max(bh * .75, 90)
        box = (f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="20" fill="#121316" fill-opacity=".94"/>'
               f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="20" fill="{col}" fill-opacity=".045"/>'
               f'<g clip-path="url(#c{gi})">'
               f'<ellipse class="d1" style="animation-delay:{-gi * 2.3:.1f}s" cx="{W * .24:.0f}" cy="{by0 + bh * .15:.0f}" rx="340" ry="{ry:.0f}" fill="url(#a{gi})"/>'
               f'<ellipse class="d2" style="animation-delay:{-gi * 3.1:.1f}s" cx="{W * .76:.0f}" cy="{by0 + bh * .9:.0f}" rx="360" ry="{ry:.0f}" fill="url(#a{gi})"/>'
               f'<g transform="translate({bx0},{by0})" opacity="{.85 if title.startswith(("AI CODING", "BACKEND", "LANGUAGES")) else .8 if title.startswith("GENERATIVE") else .55}">{scene(title, col, bw, bh)}</g></g>'
               f'<rect class="rim" style="animation-delay:{-gi * .9:.1f}s" x="{bx0}" y="{by0}" width="{bw}" height="{bh}" rx="20" fill="none" stroke="{col}" stroke-width="1.5"/>')
        out = before + box + out
        y += 30
    H = y
    H -= 46                    # drop the trailing gap so the last box is also 14 from the bottom edge
    css = ("@keyframes d1{0%,100%{transform:translate(-90px,0)}50%{transform:translate(260px,14px)}}.d1{animation:d1 14s ease-in-out infinite}"
           "@keyframes d2{0%,100%{transform:translate(90px,0)}50%{transform:translate(-280px,-14px)}}.d2{animation:d2 17s ease-in-out infinite}"
           "@keyframes rim{0%,100%{stroke-opacity:.3}50%{stroke-opacity:.6}}.rim{stroke-opacity:.42;animation:rim 8s ease-in-out infinite}" + SIG_CSS + RM)
    pad, head_h = 28, 0
    from gen_sections import GROW
    gdef, ghead = "", ""
    bk_defs, bk_body = backing(W + 2 * pad, H + 2 * pad + head_h)
    write("toolbox.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * pad}" height="{H + 2 * pad + head_h}" viewBox="0 0 {W + 2 * pad} {H + 2 * pad + head_h}">
  <defs>{adefs}{gdef}{bk_defs}</defs>
  <style>{BK_CSS}{css}{GROW}</style>
  {bk_body}
  {ghead}
  <g transform="translate({pad},{pad + head_h})">{out}</g>
</svg>""")
    return n_logo, n_mono


def lines_for(name):
    if len(name) <= 13:
        return [name]
    return wrap(name, 100, 11.5, .6)
