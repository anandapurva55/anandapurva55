"""Toolbox as a logo wall: real brand marks, no per-tool boxes, with a slow wave of light across it."""
from assetlib import (aspect, logo_box, AM, BG, BLUR, BODY, EM, FLOW_CSS, FONT, INK, LAV, MONO, MUTED, PANEL, RM, ROSE, SKY, cur, escape, has_logo, logo,
                      mono_tile, pd, wrap, write)

# (label, logo slug or None, monogram for tools that have no public logo)
GROUPS = [
    # (title, colour, badge logo for the title, items, "also" line for tools without a public logo)
    ("GENERATIVE & AGENTIC AI", EM, None,
     [("MCP", "mcp"), ("RAG", "i-rag"), ("Semantic Search", "i-semantic"), ("Embeddings", "i-embed"), ("Fine-tuning (SFT)", "i-finetune"),
      ("LoRA / QLoRA", "i-qlora"), ("Prompt Engineering", "i-prompt"), ("LLM-as-a-Judge", "i-judge"), ("Strands Agents", "strands"),
      ("AutoGen", "autogen"), ("LangChain", "langchain-i"), ("Hugging Face", "huggingface"), ("Claude", "claude"), ("Gemini", "googlegemini"),
      ("GPT", "openai"), ("Llama", "meta"), ("Qwen", "qwen"), ("Amazon Nova", "nova"), ("Ollama", "ollama")],
     None),
    ("ML & DATA SCIENCE", AM, None,
     [("PyTorch", "pytorch"), ("TensorFlow", "tensorflow"), ("Keras", "keras"), ("scikit-learn", "scikitlearn"), ("XGBoost", "xgboost"),
      ("LightGBM", "lightgbm"), ("Optuna", "optuna"), ("SHAP", "shap"), ("statsmodels", "statsmodels"), ("linearmodels", "linearmodels"),
      ("NumPy", "numpy"), ("Pandas", "pandas"), ("SciPy", "scipy"), ("Matplotlib", "matplotlib"), ("seaborn", "seaborn"),
      ("Jupyter", "jupyter"), ("Gurobi", "gurobi"), ("Ray", "ray"), ("NLTK", "nltk"), ("lifelines", "lifelines")],
     None),
    ("DATA & ANALYTICS", SKY, None,
     [("Snowflake", "snowflake"), ("PostgreSQL", "postgresql"), ("SQLite", "sqlite"), ("Apache Spark", "apachespark"),
      ("Apache Arrow", "apachearrow"), ("Tableau", "tableau")],
     None),
    ("MLOPS", ROSE, None,
     [("MLflow", "mlflow"), ("Evidently", "evidently-light"), ("Terraform", "terraform"), ("Docker", "docker"), ("Kubernetes", "kubernetes"),
      ("GitHub Actions", "githubactions"), ("Tekton", "tekton")],
     None),
    ("AMAZON WEB SERVICES (AWS)", AM, "aws",
     [("Bedrock", "bedrock"), ("SageMaker", "sagemaker"), ("Lambda", "lambda"), ("EC2", "ec2"), ("ECS", "ecs"), ("Fargate", "fargate"),
      ("App Runner", "apprunner"), ("S3", "s3"), ("DynamoDB", "dynamodb"), ("RDS", "rds"), ("Glue", "glue"), ("Athena", "athena"),
      ("OpenSearch", "opensearch"), ("CloudFront", "cloudfront"), ("CloudWatch", "cloudwatch"), ("Step Functions", "stepfunctions"),
      ("Cognito", "cognito"), ("WAF", "waf"), ("IAM", "iam"), ("EventBridge", "eventbridge"), ("QuickSight", "quicksight"),
      ("CloudFormation", "cloudformation"), ("CDK", "cdk"), ("CodeBuild", "codebuild"), ("ECR", "ecr"),
      ("Secrets Manager", "secretsmanager"), ("Load Balancer", "elb"), ("SNS", "sns"), ("VPC", "vpc"), ("Systems Manager", "ssm")],
     None),
    ("GOOGLE CLOUD PLATFORM (GCP)", LAV, "googlecloud",
     [("BigQuery", "bigquery"), ("Cloud Run", "cloudrun"), ("Cloud Build", "cloudbuild"), ("Cloud Storage", "googlecloudstorage"),
      ("Cloud Logging", "cloudlogging"), ("Cloud Scheduler", "cloudscheduler"), ("Vertex AI", "vertexai"), ("Apigee", "apigee"),
      ("Model Armor", "modelarmor")],
     None),
    ("SECURITY & OBSERVABILITY", SKY, None,
     [("Dynatrace", "dynatrace"), ("Prometheus", "prometheus"), ("SonarQube", "sonar"), ("FOSSA", "fossa-i"), ("Cycode", "cycode"),
      ("Dependabot", "dependabot"), ("Entra ID", "entra")],
     None),
    ("BACKEND & APIS", LAV, None,
     [("FastAPI", "fastapi"), ("Pydantic", "pydantic"), ("WhatsApp API", "whatsapp")],
     None),
    ("FRONTEND & DATA APPS", SKY, None,
     [("React", "react"), ("TypeScript", "typescript"), ("Vite", "vite"), ("Streamlit", "streamlit")],
     None),
    ("AI CODING ASSISTANTS", ROSE, None,
     [("Claude Code", "claudecode"), ("Codex", "codex"), ("GitHub Copilot", "githubcopilot"), ("Google Antigravity", "antigravity")],
     None),
    ("LANGUAGES & DEV TOOLS", EM, None,
     [("Python", "python"), ("SQL", "sql"), ("GitHub", "github"), ("VS Code", "vscode"), ("Cursor", "cursor"), ("Postman", "postman"), ("Hoppscotch", "hoppscotch"),
      ("Jira", "jira"), ("pytest", "pytest")],
     None),
]


def toolbox():
    W, cols, cw, rh = 1000, 10, 100, 100
    y, out, n_logo, n_mono = 0, "", 0, 0
    for gi, (title, col, badge, items, also) in enumerate(GROUPS):
        bx = 0
        if badge:                                  # brand badge lives in the title, so the grid does not repeat it
            out += logo(badge, 0, y - 6, 34, bg=BG) or ""
            bx = 46
        out += f'<text x="{bx}" y="{y + 20}" style="font:800 14px {MONO};fill:{col};letter-spacing:2.6px">{escape(title)}</text>'
        tx = bx + 40 + len(title) * 10.4
        out += cur(pd([(tx, y + 15), (W, y + 15)]), col, gi * .8, 5.5, 2.6, 6)
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
            out += f'<g class="tl" style="animation-delay:{gi * .5 + r * .22 + c * .07:.2f}s">{mark}{lab}</g>'
        y += ((len(items) - 1) // cols + 1) * rh
        y += 14
    H = y
    css = ("@keyframes wave{0%,16%,100%{opacity:.8;transform:scale(1)}7%{opacity:1;transform:scale(1.09)}}"
           ".tl{transform-box:fill-box;transform-origin:center;animation:wave 14s ease-in-out infinite}" + FLOW_CSS + RM)
    pad, head_h = 28, 0
    from gen_sections import GROW
    gdef, ghead = "", ""
    write("toolbox.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * pad}" height="{H + 2 * pad + head_h}" viewBox="0 0 {W + 2 * pad} {H + 2 * pad + head_h}">
  <defs>{BLUR}{gdef}</defs>
  <style>{css}{GROW}</style>
  <rect width="{W + 2 * pad}" height="{H + 2 * pad + head_h}" fill="{BG}" stroke="#fff" stroke-opacity=".08"/>
  {ghead}
  <g transform="translate({pad},{pad + head_h})">{out}</g>
</svg>""")
    return n_logo, n_mono


def lines_for(name):
    if len(name) <= 13:
        return [name]
    return wrap(name, 100, 11.5, .6)
