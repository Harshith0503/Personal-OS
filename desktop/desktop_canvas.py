from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from desktop.desktop_area import DesktopArea
from desktop.dock import Dock


class DesktopCanvas(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.logger = app.logger
        self.settings = app.settings
        self.theme = app.theme
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)
        self.desktop_area = DesktopArea(self.app)
        layout.addWidget(self.desktop_area, 1)
        self.dock = Dock(self.app)
        layout.addWidget(
            self.dock,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )