"""
Improved FastAPI demo for TechGuru:
- Serves a friendly landing page at /
- Serves Images/ as static files under /images
- Exposes endpoints: /explain, /generate-tests, /bughunt, /scaffold, /run-tests, /stream, /chat
"""
import os
import json
import asyncio
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

# load dotenv if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Import agent modules
from app import agent_core, code_tools, scaffolder, srs_scheduler

app = FastAPI(title="TechGuru Demo API")

# Static chat UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/chat", response_class=HTMLResponse)
    def chat_ui():
        html_path = os.path.join(static_dir, "chat.html")
        if os.path.exists(html_path):
            return FileResponse(html_path, media_type="text/html")
        return HTMLResponse("<html><body><h3>Chat UI not found</h3></body></html>", status_code=404)

# Mount Images
images_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Images"))
if os.path.isdir(images_path):
    app.mount("/images", StaticFiles(directory=images_path), name="images")

# Helper: stream chunks of text
async def _text_chunker(text: str, chunk_size: int = 120, delay: float = 0.01, max_total: int = 20000):
    """Yield small chunks of text with a slight delay to simulate streaming."""
    if not isinstance(text, str):
        text = str(text)
    if len(text) > max_total:
        text = text[:max_total] + "\n\n[TRUNCATED: response exceeded max length]"
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_size]
        i += chunk_size
        yield chunk
        await asyncio.sleep(delay)

# Simple endpoint to report which model env is configured (helpful for UI/debug)
@app.get("/model")
def model_info():
    return {
        "GOOGLE_API_KEY_set": bool(os.getenv("GOOGLE_API_KEY")),
        "GOOGLE_MODEL": os.getenv("GOOGLE_MODEL"),
        "GOOGLE_MODEL_DEEP": os.getenv("GOOGLE_MODEL_DEEP"),
        "GOOGLE_MODEL_FAST": os.getenv("GOOGLE_MODEL_FAST")
    }

# Streaming endpoint (mode + payload)
@app.post("/stream")
async def stream_endpoint(request: Request):
    """
    POST JSON: { "mode": "explain"|"generate-tests"|"bughunt"|"scaffold", "payload": {...} }
    Returns a streaming plain-text response (chunked).
    """
    try:
        body = await request.json()
    except Exception:
        body = await request.body()
        try:
            body = json.loads(body)
        except Exception:
            body = {}

    mode = body.get("mode", "explain")
    payload = body.get("payload", {}) or {}

    try:
        if mode == "generate-tests":
            text = agent_core.generate_tests(payload.get("code", ""), n_tests=5, language=payload.get("lang", "python"))
        elif mode == "bughunt":
            res = agent_core.bug_hunt_and_fix(payload.get("code", ""))
            text = json.dumps(res, indent=2)
        elif mode == "scaffold":
            files = agent_core.scaffold_project(payload.get("project_name", "sample_project"))
            text = "Scaffolded files:\n" + "\n".join(files.keys())
        else:  # explain
            res = agent_core.explain_code(payload.get("code", ""), lang=payload.get("lang", "python"))
            if isinstance(res, dict) and "summary" in res:
                parts = [f"Summary:\n{res.get('summary')}\n"]
                if res.get("line_comments"):
                    parts.append("Line comments:")
                    for lc in res["line_comments"]:
                        parts.append(f"  line {lc.get('line')}: {lc.get('comment')}")
                if res.get("micro_exercises"):
                    parts.append("\nMicro exercises:")
                    for ex in res["micro_exercises"]:
                        parts.append(f"  - {ex}")
                text = "\n".join(parts)
            else:
                text = str(res)
    except Exception as e:
        tb = traceback.format_exc()
        text = f"[ERROR] Agent failed: {e}\n\n{tb}"

    return StreamingResponse(_text_chunker(text), media_type="text/plain; charset=utf-8")


# Request models
class CodeIn(BaseModel):
    code: str
    lang: str = "python"

class ScaffoldIn(BaseModel):
    project_name: str = "sample_project"


@app.post("/explain")
def explain(body: CodeIn):
    try:
        res = agent_core.explain_code(body.code, lang=body.lang)
        return res
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate-tests")
def generate_tests(body: CodeIn):
    try:
        test_text = agent_core.generate_tests(body.code, n_tests=5, language=body.lang)
        return {"tests": test_text}
    except Exception as e:
        return {"error": str(e)}

@app.post("/bughunt")
def bughunt(body: CodeIn):
    try:
        res = agent_core.bug_hunt_and_fix(body.code)
        return res
    except Exception as e:
        return {"error": str(e)}

@app.post("/scaffold")
def scaffold(body: ScaffoldIn):
    try:
        files = agent_core.scaffold_project(body.project_name)
        demo_dir = os.path.join(os.path.dirname(__file__), body.project_name)
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_projects', body.project_name)
        os.makedirs(demo_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        for rel_path, content in files.items():
            parts = rel_path.split("/", 1)
            subpath = parts[1] if len(parts) == 2 else parts[0]
            # write demo copy
            demo_full = os.path.join(demo_dir, subpath)
            os.makedirs(os.path.dirname(demo_full), exist_ok=True)
            with open(demo_full, "w", encoding="utf-8") as f:
                f.write(content)
            # write data copy
            data_full = os.path.join(data_dir, subpath)
            os.makedirs(os.path.dirname(data_full), exist_ok=True)
            with open(data_full, "w", encoding="utf-8") as f:
                f.write(content)
        return {"files_written": list(files.keys()), "demo_dir": f"demo/{body.project_name}", "data_dir": f"data/sample_projects/{body.project_name}"}
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Scaffold failed: {e}\n\n{tb}")

@app.get("/run-tests")
def run_tests(project: str = "sample_project"):
    project_root = os.path.join(os.path.dirname(__file__), project)
    if not os.path.isdir(project_root):
        raise HTTPException(status_code=404, detail=f"Project not found: {project_root}")
    code, out = code_tools.run_pytest(project_root)
    return {"exit_code": code, "output": out}


# Friendly root page
@app.get("/", response_class=HTMLResponse)
def root():
    banner_url = "/images/banner_1.png" if os.path.exists(os.path.join(images_path, "banner_1.png")) else ""
    html = f"""
    <html>
      <head>
        <title>TechGuru - Demo</title>
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
