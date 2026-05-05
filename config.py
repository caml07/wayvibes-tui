import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "wayvibes-tui"
CONFIG_FILE = CONFIG_DIR / "config.toml"
DEFAULT_SOUNDPACKS_DIR = Path.home() / "wayvibes" / "soundpacks"

DEFAULT_CONFIG = {
    "general": {
        "soundpacks_dir": str(DEFAULT_SOUNDPACKS_DIR),
    },
    "wayvibes": {
        "volume": 1.0,
        "device": "",
    },
}


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)