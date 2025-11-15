# app/scaffolder.py
"""
Small project scaffolding helper. Produces a dict of path->content.
"""
from typing import Dict

def default_scaffold(project_name: str = "project") -> Dict[str, str]:
    files = {
        f"{project_name}/README.md": f"# {project_name}\n\nScaffolded by TechGuru.",
        f"{project_name}/requirements.txt": "pytest\n",
        f"{project_name}/src/__init__.py": "",
        f"{project_name}/src/app.py": "def greet(name):\n    return f'Hello, {name}'\n",
        f"{project_name}/tests/test_app.py": (
            "from src.app import greet\n\n"
            "def test_greet():\n"
            "    assert greet('TechGuru') == 'Hello, TechGuru'\n"
        )
    }
    return files
