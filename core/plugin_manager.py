import json

from pathlib import Path

from core.config import PLUGINS_DIR


class PluginManager:
    def __init__(self, logger):
        self.logger = logger
        self.plugins = {}

    def discover_plugins(self):
        self.plugins.clear()
        if not PLUGINS_DIR.exists():
            self.logger.warning("Plugin directory not found")
            return
        for folder in PLUGINS_DIR.iterdir():
            if not folder.is_dir():
                continue
            manifest = folder / "manifest.json"
            if not manifest.exists():
                self.logger.warning(
                    f"Skipping {folder.name}: manifest.json missing"
                )
                continue
            try:
                with open(manifest, "r", encoding="utf-8") as file:
                    info = json.load(file)
                self.plugins[info["name"]] = {
                    "path": folder,
                    "info": info
                }
                self.logger.info(
                    f"Loaded plugin: {info['name']}"
                )
            except Exception as e:
                self.logger.error(
                    f"Failed loading plugin '{folder.name}': {e}"
                )

    def get_plugins(self):
        return self.plugins

    def get_plugin(self, name):
        return self.plugins.get(name)