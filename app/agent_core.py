# app/agent_core.py
"""
TechGuru agent core (model-safe): prefers available Gemini flash models,
supports env overrides, retries/backoff, and offline fallback.

Model-env vars supported:
- GOOGLE_API_KEY           (required to call remote models)
- GOOGLE_MODEL             (global override, single name)
- GOOGLE_MODEL_DEEP        (preferred model for deep tasks)
- GOOGLE_MODEL_FAST        (preferred model for fast/light tasks)

Default preferred models (in order):
- gemini-2.5-flash-lite
- gemini-2.0-flash

This file is intentionally defensive: if model calls fail (404, 429, permission),
it will try alternatives and ultimately fall back to a local stub response.
"""
import os
import json
import time
from typing import Any, Dict, List

# Safe import of google-genai (optional)
try:
    from google import genai
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

# Default model preferences based on your account snapshot
DEFAULT_PREFERRED = [
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]

# Allow user overrides via env vars
ENV_MODEL = os.getenv("GOOGLE_MODEL", "").strip() or None
ENV_MODEL_DEEP = os.getenv("GOOGLE_MODEL_DEEP", "").strip() or None
ENV_MODEL_FAST = os.getenv("GOOGLE_MODEL_FAST", "").strip() or None

PREFERRED_MODELS = []
if ENV_MODEL:
    PREFERRED_MODELS.append(ENV_MODEL)
if ENV_MODEL_DEEP:
    PREFERRED_MODELS.append(ENV_MODEL_DEEP)
if ENV_MODEL_FAST:
    PREFERRED_MODELS.append(ENV_MODEL_FAST)
# then the known defaults
for m in DEFAULT_PREFERRED:
    if m not in PREFERRED_MODELS:
        PREFERRED_MODELS.append(m)

# remove empty/None
PREFERRED_MODELS = [m for m in PREFERRED_MODELS if m]

# call-time helper to build genai client
def _make_genai_client():
    if not HAS_GENAI:
        return None
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

# Generic safe call wrapper with retry/backoff and model fallback
def _call_gemini_with_fallback(prompt: str,
                               models: List[str] = None,
                               short_response: bool = False,
                               max_attempts_per_model: int = 2) -> str:
    """
    Try each model in 'models' list (or PREFERRED_MODELS) until one returns text.
    Handles common errors (NOT_FOUND for model, rate limit 429) and retries/backoffs.
    If no client or all models fail, returns offline fallback text.
    """
    client = _make_genai_client()
    if client is None:
        return _offline_stub(prompt)

    # decide the models to try
    models_to_try = models if models else PREFERRED_MODELS
    last_exception = None

    for model_name in models_to_try:
        if not model_name:
            continue
        for attempt in range(1, max_attempts_per_model + 1):
            try:
                # Do a minimal generate_content call; SDKs differ, so be permissive.
                # We pass model and contents only and rely on SDK for default settings.
                resp = client.models.generate_content(model=model_name, contents=prompt)
                # resp may have attribute .text or a nested structure; handle common cases
                text = getattr(resp, "text", None)
                if text is None:
                    # Try to convert resp to string
                    text = str(resp)
                return text
            except Exception as e:
                last_exception = e
                msg = str(e).lower()
                # If model not found (404 / NOT_FOUND), break to next model immediately
                if "not found" in msg or "not_supported" in msg or "not_supported" in msg or "404" in msg:
                    # try next model
                    break
                # Rate limit or quota issues - wait and retry a small number of times
                if "rate" in msg or "quota" in msg or "429" in msg:
                    backoff = min(2 ** attempt, 8)
                    time.sleep(backoff)
                    continue
                # Some SDKs raise TypeError for unexpected kwargs — treat this as non-fatal and return error string
                if isinstance(e, TypeError):
                    return f"[GENAI ERROR] SDK TypeError for model={model_name}: {e}"
                # For other exceptions, try model again a couple times then move on
                time.sleep(0.5)
                continue
        # exhausted attempts for this model, try next
    # All models failed
    return f"[GENAI ERROR] All model attempts failed. Last exception: {repr(last_exception)}"

def _offline_stub(prompt: str) -> str:
    # Compact simulated fallback; used for tests or when no API key present.
    return f"[FALLBACK] Simulated response (prompt head): {prompt[:300].replace(chr(10),' ')}"

# Convenience wrappers for common agent tasks
def explain_code(source_code: str, lang: str = "python") -> Dict[str, Any]:
    """
    Returns structured explanation. Attempts to parse JSON from model response; otherwise returns a fallback dict.
    """
    prompt = (
        f"You are a senior software instructor. Language: {lang}.\n\n"
        "Given the following source code, produce JSON with keys:\n"
        "- summary: 3-sentence high-level summary for a student\n"
        "- line_comments: list of objects {line:int, comment:str} for important lines only\n"
        "- complexity: time/space complexity (informal)\n"
        "- micro_exercises: 3 short practice problems inspired by this code (one-liners)\n\n"
        "Return only valid JSON.\n\n"
        f"Source code:\n'''{source_code}'''\n"
    )
    # prefer DEEP model list (env override or default order)
    models = []
    if ENV_MODEL_DEEP:
        models.append(ENV_MODEL_DEEP)
    models.extend([m for m in PREFERRED_MODELS if m not in models])
    out = _call_gemini_with_fallback(prompt, models=models)
    try:
        return json.loads(out)
    except Exception:
        # structured fallback
        lines = source_code.splitlines()
        line_comments = [{"line": i+1, "comment": "Review this line."} for i in range(min(4, len(lines)))]
        return {
            "summary": out[:400],
            "line_comments": line_comments,
            "complexity": "O(n)?? (fallback)",
            "micro_exercises": [
                "Write tests for this function (basic/edge cases).",
                "Refactor to improve readability.",
                "Add input validation."
            ]
        }

def generate_tests(source_code: str, n_tests: int = 5, language: str = "python") -> str:
    prompt = (
        "You are an expert test author. Given the following code module, produce a pytest test file.\n"
        f"Language: {language}. Create {n_tests} meaningful test cases covering normal and edge cases.\n"
        "Return only the content of the test file.\n\n"
        f"Module:\n'''{source_code}'''\n"
    )
    # test generation can be token-heavy; prefer DEEP then FAST
    models = []
    if ENV_MODEL_DEEP:
        models.append(ENV_MODEL_DEEP)
    if ENV_MODEL_FAST and ENV_MODEL_FAST not in models:
        models.append(ENV_MODEL_FAST)
    models.extend([m for m in PREFERRED_MODELS if m not in models])
    return _call_gemini_with_fallback(prompt, models=models)

def bug_hunt_and_fix(source_code: str) -> Dict[str, Any]:
    prompt = (
        "You are a careful code reviewer. Read the code and:\n"
        "1) List up to 5 possible bugs or anti-patterns with severity (low/med/high).\n"
        "2) For each, provide a suggested fix as a unified diff (---/+++ style) if possible.\n"
        "Return JSON with keys: issues (list) and refactor (short paragraph).\n\n"
        f"Code:\n'''{source_code}'''\n"
    )
    models = []
    if ENV_MODEL_DEEP:
        models.append(ENV_MODEL_DEEP)
    models.extend([m for m in PREFERRED_MODELS if m not in models])
    out = _call_gemini_with_fallback(prompt, models=models)
    try:
        return json.loads(out)
    except Exception:
        return {
            "issues": [
                {"issue": "Potential missing input validation", "severity": "medium", "patch": "--- a/file.py\n+++ b/file.py\n@@\n-    ...\n+    # add validation\n"},
            ],
            "refactor": out[:400]
        }

def scaffold_project(project_name: str = "sample_project", language: str = "python") -> Dict[str, str]:
    # deterministic lightweight scaffold; doesn't call model (cheap)
    files = {
        f"{project_name}/README.md": f"# {project_name}\n\nGenerated by TechGuru scaffold.",
        f"{project_name}/src/__init__.py": "",
        f"{project_name}/src/main.py": "def main():\n    return 'Hello from TechGuru scaffold'\n",
        f"{project_name}/tests/test_main.py": (
            "from src.main import main\n\n"
            "def test_main():\n"
            "    assert main() == 'Hello from TechGuru scaffold'\n"
        ),
        f"{project_name}/.github/workflows/ci.yml": (
            "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v4\n        with:\n          python-version: '3.10'\n      - run: pip install -r requirements.txt\n      - run: pytest -q\n"
        )
    }
    return files
