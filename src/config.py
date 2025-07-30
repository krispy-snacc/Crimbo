import json
import toml
from pathlib import Path
from box import Box


pyproject_path = Path("pyproject.toml")
pyproject = toml.loads(pyproject_path.read_text())

try:
    __version__ = pyproject["project"]["version"]
except KeyError:
    __version__ = None

CONFIG = Box()

with open("data/config.json") as f:
    CONFIG = Box(json.load(f))

CONFIG["version"] = __version__