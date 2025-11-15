# conftest.py - ensures tests can import the project's 'src' package
import os, sys
HERE = os.path.dirname(__file__)            # .../demo/sample_project/tests
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))  # .../demo/sample_project
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
