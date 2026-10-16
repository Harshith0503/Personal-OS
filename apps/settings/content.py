from PyQt6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout
)

from apps.settings.pages.appearance import AppearancePage
from apps.settings.pages.wallpaper import WallpaperPage
from apps.settings.pages.themes import ThemesPage
from apps.settings.pages.system import SystemPage
from apps.settings.pages.about import AboutPage


class SettingsContent(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.stack = QStackedWidget()
        self.pages = {
            "appearance": AppearancePage(self.app),
            "wallpaper": WallpaperPage(self.app),
            "themes": ThemesPage(self.app),
            "system": SystemPage(self.app),
            "about": AboutPage(self.app)
        }
        for page in self.pages.values():
            self.stack.addWidget(page)
        layout.addWidget(self.stack)

    def set_page(self, page_name):
        if page_name in self.pages:
            self.stack.setCurrentWidget(
                self.pages[page_name]
            )