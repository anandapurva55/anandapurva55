#!/usr/bin/env python3
"""Downloads brand logos into assets/logos/ so the generator can inline them offline.

Two public sources: Simple Icons (cdn.simpleicons.org) and Iconify (api.iconify.design), which
hosts several logo collections. Logos stay the property of their owners; they are used here only
to name the tools the author works with.
"""
import time
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "logos"
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (logo fetch)"}

# local slug -> Iconify "prefix:name"
ICONIFY = {
    # GenAI
    "openai": "logos:openai-icon", "qwen": "logos:qwen-icon", "nova": "thesvg:nova-aws",
    "langchain-i": "logos:langchain-icon", "mcp": "thesvg:mcp-model-context-protocol",
    # ML / data
    "optuna": "thesvg:optuna", "scipy": "thesvg:scipy", "matplotlib": "logos:matplotlib-icon",
    "jupyter": "logos:jupyter", "seaborn": "logos:seaborn-icon",
    # AWS
    "aws": "logos:aws", "lambda": "logos:aws-lambda", "ec2": "logos:aws-ec2", "ecs": "logos:aws-ecs", "fargate": "logos:aws-fargate",
    "s3": "logos:aws-s3", "dynamodb": "logos:aws-dynamodb", "rds": "logos:aws-rds", "glue": "logos:aws-glue", "athena": "logos:aws-athena",
    "cloudfront": "logos:aws-cloudfront", "cloudwatch": "logos:aws-cloudwatch", "stepfunctions": "logos:aws-step-functions",
    "cognito": "logos:aws-cognito", "waf": "logos:aws-waf", "iam": "logos:aws-iam", "eventbridge": "logos:aws-eventbridge",
    "quicksight": "logos:aws-quicksight", "cloudformation": "logos:aws-cloudformation", "codebuild": "logos:aws-codebuild",
    "secretsmanager": "logos:aws-secrets-manager", "elb": "logos:aws-elb", "sns": "logos:aws-sns", "vpc": "logos:aws-vpc",
    "ssm": "logos:aws-systems-manager", "kinesis": "logos:aws-kinesis",
    # Google Cloud
    "bigquery": "gcp:bigquery", "cloudrun": "gcp:cloud-run", "cloudbuild": "gcp:cloud-build", "apigee": "gcp:apigee-api-platform",
    "vertexai": "gcp:vertexai", "vscode": "logos:visual-studio-code", "claudecode": "logos:claude-code", "cloudlogging": "gcp:cloud-logging", "cloudscheduler": "gcp:cloud-scheduler",
    # DevOps / security / observability
    "githubactions": "logos:github-actions", "dependabot": "logos:dependabot", "sonar": "thesvg:sonar", "fossa-i": "thesvg:fossa",
    "prometheus": "logos:prometheus", "entra": "selfhst:microsoft-entra-id",
    # languages / frameworks / tools
    "typescript": "logos:typescript-icon", "vite": "logos:vite-icon", "pytest": "thesvg:pytest", 
    "pydantic": "logos:pydantic-icon", "tableau": "logos:tableau-icon",
}

# slug -> direct URL (official sources: AWS icon set, project repos, company sites, Fluent Emoji)
DIRECT = {
    "bedrock.svg": "https://raw.githubusercontent.com/AwesomeLogos/aws-icons/master/docs/images/Architecture-Service-Icons/Arch_Machine-Learning/64/Arch_Amazon-Bedrock_64.svg",
    # concepts without a brand mark: distinct colour pictures from Microsoft's open-source Fluent Emoji set (MIT)
    "i-rag.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Books/Flat/books_flat.svg",
    "i-semantic.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Magnifying%20glass%20tilted%20right/Flat/magnifying_glass_tilted_right_flat.svg",
    "i-embed.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Milky%20way/Flat/milky_way_flat.svg",
    "i-prompt.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Memo/Flat/memo_flat.svg",
    "i-finetune.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Control%20knobs/Flat/control_knobs_flat.svg",
    "i-qlora.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Puzzle%20piece/Flat/puzzle_piece_flat.svg",
    "i-judge.svg": "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Balance%20scale/Flat/balance_scale_flat.svg",
    "sagemaker.svg": "https://raw.githubusercontent.com/weibeld/aws-icons-svg/main/q1-2022/Architecture-Service-Icons_01312022/Arch_Machine-Learning/64/Arch_Amazon-SageMaker_64.svg",
    "strands.svg": "https://raw.githubusercontent.com/strands-agents/sdk-python/HEAD/site/src/assets/logo-dark.svg",
    "autogen.png": "https://raw.githubusercontent.com/microsoft/autogen/HEAD/python/docs/src/_static/images/logo/favicon-512x512.png",
    "shap.png": "https://raw.githubusercontent.com/shap/shap/HEAD/docs/artwork/shap_logo_white.png",
    "lightgbm.svg": "https://raw.githubusercontent.com/microsoft/LightGBM/HEAD/R-package/man/figures/logo.svg",
    "xgboost.png": "https://raw.githubusercontent.com/dmlc/dmlc.github.io/master/img/logo-m/xgboost.png",
    "cycode.svg": "https://raw.githubusercontent.com/cycodehq/intellij-platform-plugin/HEAD/src/main/resources/META-INF/pluginIcon.svg",
    "statsmodels.svg": "https://raw.githubusercontent.com/statsmodels/statsmodels/main/docs/source/images/statsmodels-logo-v2-bw.svg",
    "linearmodels.svg": "https://raw.githubusercontent.com/bashtage/linearmodels/main/doc/source/images/logo.svg",
    "evidently.png": "https://raw.githubusercontent.com/evidentlyai/evidently/main/src/evidently/ui/service/assets/static/img/evidently-ai-logo.png",
    "apprunner.svg": "https://raw.githubusercontent.com/weibeld/aws-icons-svg/main/q1-2022/Architecture-Service-Icons_01312022/Arch_Compute/64/Arch_AWS-App-Runner_64.svg",
    "ecr.svg": "https://raw.githubusercontent.com/weibeld/aws-icons-svg/main/q1-2022/Architecture-Service-Icons_01312022/Arch_Containers/64/Arch_Amazon-Elastic-Container-Registry_64.svg",
    "cdk.svg": "https://raw.githubusercontent.com/weibeld/aws-icons-svg/main/q1-2022/Architecture-Service-Icons_01312022/Arch_Developer-Tools/64/Arch_AWS-Cloud-Development-Kit_64.svg",
    "trianz.svg": "https://www.trianz.com/themes/trianz_beta/images/logos/trianz-logo-horizontal-withtagline-inverse.svg",
    "stengg.png": "https://www.stengg.com/images/st-logo-white-footer.png",
    "360dialog.png": "https://framerusercontent.com/images/jIuaZADY7mDxeIXC0MTLYIGQUGI.png",
}

SIMPLE = ["githubcopilot", "sqlite", "apachearrow", "tekton", "hoppscotch", "ford", "python", "pytorch", "tensorflow", "keras", "scikitlearn", "huggingface", "docker", "kubernetes", "terraform", "postgresql", "snowflake",
          "fastapi", "streamlit", "github", "cursor", "postman", "jira", "apachespark", "ray", "langchain", "googlecloud", "googlecloudstorage",
          "dynatrace", "sonarqubeserver", "claude", "googlegemini", "meta", "ollama", "mlflow", "react", "gmail", "whatsapp", "numpy", "pandas",
          "gurobi", "opensearch", "modelcontextprotocol", "fossa", "anthropic"]


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:      # be polite: back off when rate limited
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(4 * (i + 1))


ok, miss = [], []
for slug, ref in ICONIFY.items():
    if (OUT / f"{slug}.svg").exists():           # already downloaded: skip, so re-runs are cheap
        continue
    prefix, name = ref.split(":")
    time.sleep(.4)
    try:
        s = get(f"https://api.iconify.design/{prefix}/{name}.svg")
        assert s.lstrip().startswith("<svg")
        (OUT / f"{slug}.svg").write_text(s)
        ok.append(slug)
    except Exception as e:
        miss.append((slug, ref, str(e)[:40]))
for slug in SIMPLE:
    f = OUT / f"{slug}.svg"
    if f.exists():
        continue
    try:
        s = get(f"https://cdn.simpleicons.org/{slug}")
        assert s.lstrip().startswith("<svg")
        f.write_text(s)
        ok.append(slug)
    except Exception as e:
        miss.append((slug, "simple-icons", str(e)[:40]))
for fname, url in DIRECT.items():
    f = OUT / fname
    if f.exists():
        continue
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
        assert len(data) > 200
        f.write_bytes(data)
        ok.append(fname)
    except Exception as e:
        miss.append((fname, url[-50:], str(e)[:40]))
print("downloaded:", len(ok), "missing:", miss)
