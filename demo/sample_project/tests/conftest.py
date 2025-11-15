import os
import sys

# Insert the project root (the parent of 'src') into sys.path so tests can import 'src'
HERE = os.path.dirname(__file__)               # tests/
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))  # sample_project/
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
