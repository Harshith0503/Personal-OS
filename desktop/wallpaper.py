from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

from core.config import ASSETS_DIR


class Wallpaper(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.wallpaper_path = (
            ASSETS_DIR /
            "wallpapers" /
            "default.jpg"
        )
        if self.wallpaper_path.exists():
            self.pixmap = QPixmap(str(self.wallpaper_path))
        else:
            self.pixmap = None

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.pixmap is not None:
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.fillRect(self.rect(), Qt.GlobalColor.darkGray)