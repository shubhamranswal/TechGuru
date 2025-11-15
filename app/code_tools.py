"""
Utilities to run pytest on generated test files, apply simple patches (unified diff), and capture results.
"""

import os
import subprocess
import tempfile
from typing import Tuple

def run_pytest(project_root: str) -> Tuple[int, str]:
    """
    Run pytest in project_root. Returns (exit_code, output).
    """
    if not os.path.isdir(project_root):
        return 1, f"Project root not found: {project_root}"
    try:
        proc = subprocess.run(
            ["pytest", "-q"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120
        )
        out = proc.stdout + "\n" + proc.stderr
        return proc.returncode, out
    except Exception as e:
        return 2, f"Error running pytest: {e}"

def apply_unified_diff(project_root: str, diff_text: str) -> bool:
    """
    Apply a very small unified diff to files in project_root.
    WARNING: This is minimal and intended for simple patches only.
    """
    try:
        lines = diff_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("--- "):
                a_path = line[4:].strip()
                b_line = lines[i+1] if i+1 < len(lines) else ""
                if b_line.startswith("+++ "):
                    b_path = b_line[4:].strip()
                    # unified diffs often include a/ or b/ paths; try both
                    target = b_path
                    if target.startswith("a/") or target.startswith("b/"):
                        target = target[2:]
                    # collect hunk
                    i += 2
                    new_content = []
                    while i < len(lines) and not lines[i].startswith("--- "):
                        # naive: skip @@ hunk markers and +/- lines; keep context and '+' adds
                        ln = lines[i]
                        if ln.startswith("+") and not ln.startswith("+++"):
                            new_content.append(ln[1:])
                        elif ln.startswith(" "):
                            new_content.append(ln[1:])
                        i += 1
                    # write new content
                    target_path = os.path.join(project_root, target)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(new_content))
                else:
                    i += 1
            else:
                i += 1
        return True
    except Exception:
        return False
