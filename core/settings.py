import json

from pathlib import Path

from core.config import ROOT_DIR


class Settings:
    SETTINGS_FILE = ROOT_DIR / "settings.json"
    DEFAULTS = {
        "theme": "dark",
        "accent_color": "#4F8EF7",
        "font": "Segoe UI",
        "font_size": 10,
        "wallpaper": "",
        "window_width": 1400,
        "window_height": 850,
        "volume": 70,
        "ai_model": "llama3",
        "ai_enabled": True,
        "animations": True,
        "check_updates": True
    }

    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if not self.SETTINGS_FILE.exists():
            self.data = self.DEFAULTS.copy()
            self.save()
            return
        with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        for key, value in self.DEFAULTS.items():
            self.data.setdefault(key, value)

    def save(self):
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4
            )

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def reset(self):
        self.data = self.DEFAULTS.copy()
        self.save()