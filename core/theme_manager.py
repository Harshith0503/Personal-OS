import json

from PyQt6.QtCore import QObject, pyqtSignal

from core.config import THEMES_DIR


class ThemeManager(QObject):
    theme_changed = pyqtSignal()

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.theme = {}
        self.load_theme(
            self.settings.get("theme", "dark")
        )

    def load_theme(self, name):
        theme_file = THEMES_DIR / f"{name}.json"
        with open(theme_file, "r", encoding="utf-8") as file:
            self.theme = json.load(file)
        self.settings.set("theme", name)
        self.theme_changed.emit()

    def color(self, key):
        return self.theme["colors"].get(key)

    def current_theme(self):
        return self.theme["name"]