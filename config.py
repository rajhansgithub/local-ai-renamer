import json
import os
import sys

DEFAULT_CONFIG = {
    "engine": "local_florence2",
    "local_model_id": "microsoft/Florence-2-base",
    "gemini_api_key": "",
    "min_words": 1,
    "max_words": 5,
    "word_separator": "_",
    "lowercase": True,
    "recursive": True,
    "device": "cuda",
    "supported_extensions": [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
        ".tiff",
        ".tif"
    ],
    "auto_close_on_complete": False,
    "auto_close_delay_seconds": 3
}

def get_app_dir() -> str:
    """Returns the base directory of the application (works both in script and bundled .exe)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_config_path() -> str:
    return os.path.join(get_app_dir(), "config.json")

def load_config() -> dict:
    config_path = get_config_path()
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception as e:
            print(f"[Warning] Failed to read config.json, using defaults: {e}")
    else:
        save_config(config)
    return config

def save_config(config: dict) -> None:
    config_path = get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[Warning] Failed to save config.json: {e}")
