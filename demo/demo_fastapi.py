# demo/demo_fastapi.py
"""
Improved FastAPI demo for TechGuru:
- Serves a friendly landing page at /
- Serves Images/ as static files under /images
- Exposes endpoints: /explain, /generate-tests, /bughunt, /scaffold, /run-tests
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

# load dotenv if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from app import agent_core, code_tools, scaffolder, srs_scheduler

app = FastAPI(title="TechGuru Demo API")

# Mount static Images folder (make sure Images/ exists in repo root)
images_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Images"))
if os.path.isdir(images_path):
    app.mount("/images", StaticFiles(directory=images_path), name="images")

# Friendly root page
@app.get("/", response_class=HTMLResponse)
def root():
    banner_url = "/images/banner_1.png" if os.path.exists(os.path.join(images_path, "banner_1.png")) else ""
    logo_url = "/images/logo_1.png" if os.path.exists(os.path.join(images_path, "logo_1.png")) else ""
    html = f"""
    <html>
      <head>
        <title>TechGuru — Demo</title>
        <meta charset="utf-8" />
      </head>
      <body style="font-family: Inter, Roboto, Arial; background:#0b1220; color:#e6eef8; text-align:center; padding:30px;">
        <div style="max-width:900px; margin: auto;">
          {f'<img src="{banner_url}" alt="TechGuru banner" style="max-width:100%; height:auto; border-radius:8px; margin-bottom:20px;" />' if banner_url else '<h1>TechGuru</h1>'}
          <h2 style="color:#9bdcff; margin-top:8px;">Your AI Pair-Programmer That Actually Teaches You</h2>
          <p style="color:#cfeffd; font-size:16px;">Interactive API docs: <a href="/docs">/docs (Swagger UI)</a></p>
          <p style="margin-top:24px; color:#a9cfe6;">API endpoints: <code>/explain</code>, <code>/generate-tests</code>, <code>/bughunt</code>, <code>/scaffold</code>, <code>/run-tests</code></p>
          <div style="margin-top:28px; font-size:13px; color:#92bfdc">Demo server running on <strong>127.0.0.1:8000</strong></div>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

# Request models
class CodeIn(BaseModel):
    code: str
    lang: str = "python"

class ScaffoldIn(BaseModel):
    project_name: str = "sample_project"

# API endpoints (same as before)
@app.post("/explain")
def explain(body: CodeIn):
    res = agent_core.explain_code(body.code, lang=body.lang)
    return res

@app.post("/generate-tests")
def generate_tests(body: CodeIn):
    test_text = agent_core.generate_tests(body.code, n_tests=5, language=body.lang)
    return {"tests": test_text}

@app.post("/bughunt")
def bughunt(body: CodeIn):
    res = agent_core.bug_hunt_and_fix(body.code)
    return res

@app.post("/scaffold")
def scaffold(body: ScaffoldIn):
    files = agent_core.scaffold_project(body.project_name)
    # Optionally, write files into demo/<project_name> so /run-tests can run them
    demo_root = os.path.join(os.path.dirname(__file__), body.project_name)
    os.makedirs(demo_root, exist_ok=True)
    for rel_path, content in files.items():
        # files keys are like "project_name/..."
        # write into demo/<project_name>/...
        parts = rel_path.split("/", 1)
        if len(parts) == 2:
            _, subpath = parts
        else:
            subpath = rel_path
        full = os.path.join(os.path.dirname(__file__), body.project_name, subpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
    return {"files_written": list(files.keys()), "demo_dir": f"demo/{body.project_name}"}

@app.get("/run-tests")
def run_tests(project: str = "sample_project"):
    # run pytest in demo/<project>
    project_root = os.path.join(os.path.dirname(__file__), project)
    if not os.path.isdir(project_root):
        raise HTTPException(status_code=404, detail=f"Project not found: {project_root}")
    code, out = code_tools.run_pytest(project_root)
    return {"exit_code": code, "output": out}
