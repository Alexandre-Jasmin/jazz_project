import json
from functools import lru_cache
from pathlib import Path

from config import DevelopmentConfig

def _get_latest_patch_dir():
    p = Path(DevelopmentConfig.DDRAGON_DIR)
    dirs = [d.name for d in p.iterdir() if d.is_dir()]
    # Sort patches numerically instead of string order
    dirs.sort(key=lambda v: [int(x) for x in v.split('.')])
    return dirs[-1]

@lru_cache
def get_current_patch():
    return _get_latest_patch_dir()

@lru_cache
def get_current_champion_data():
    current_patch = _get_latest_patch_dir()
    with open(DevelopmentConfig.DDRAGON_DIR / current_patch / current_patch / "data" / "en_US" / "champion.json", "r", encoding="utf-8") as f:
        return json.load(f)