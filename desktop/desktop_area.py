from PyQt6.QtWidgets import QWidget

from desktop.wallpaper import Wallpaper
from desktop.window_manager import WindowManager


class DesktopArea(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.wallpaper = Wallpaper(app)
        self.wallpaper.setParent(self)
        self.window_manager = WindowManager(self)
        self.window_manager.setParent(self)
        self.wallpaper.lower()
        self.window_manager.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.wallpaper.setGeometry(self.rect())
        self.window_manager.setGeometry(self.rect())