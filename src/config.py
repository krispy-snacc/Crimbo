from dataclasses import dataclass
import json
import discord
import toml
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()


@dataclass
class AppConfig:
    VERSION: str
    DEBUG: bool
    TOKEN: str
    PRIMARY_COLOR: discord.Color

def load_config(path: str) -> AppConfig:
    with open(path) as f:
        raw = json.load(f)

    pyproject_path = Path("pyproject.toml")
    pyproject = toml.loads(pyproject_path.read_text())

    try:
        __version__ = pyproject["project"]["version"]
    except KeyError:
        __version__ = raw.get("VERSION", None)


    return AppConfig(
        VERSION       = __version__,
        DEBUG         = os.getenv("CRIMBO_DEBUG", "1") == "1",
        TOKEN         = os.getenv("TOKEN", None),
        PRIMARY_COLOR = discord.Color.from_str(raw.get("PRIMARY_COLOR", "#f5ad42")),
    )

CONFIG = load_config("data/config.json")
