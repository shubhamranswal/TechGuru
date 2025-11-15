# tests/test_agent_core.py
import os
import json
from app import agent_core

def test_explain_fallback():
    # Temporarily ensure no GOOGLE_API_KEY so fallback triggers
    prev = os.environ.pop("GOOGLE_API_KEY", None)
    try:
        res = agent_core.explain_code("def add(a,b):\n    return a+b")
        assert isinstance(res, dict)
        assert "summary" in res
    finally:
        if prev is not None:
            os.environ["GOOGLE_API_KEY"] = prev

def test_scaffold_structure():
    files = agent_core.scaffold_project("demo_proj")
    assert isinstance(files, dict)
    assert any(k.endswith("README.md") for k in files.keys())
