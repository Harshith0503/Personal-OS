from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtCore import Qt

from desktop.desktop_canvas import DesktopCanvas
from desktop.taskbar import Taskbar


class DesktopWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.logger = app.logger
        self.settings = app.settings
        self.theme = app.theme
        self.logger.info("Creating Desktop Window")
        self.build_ui()

    def build_ui(self):
        colors = self.theme.theme["colors"]
        self.setWindowTitle("HarshOS")
        self.resize(1400, 850)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.desktop_canvas = DesktopCanvas(self.app)
        self.taskbar = Taskbar(self.app)
        main_layout.addWidget(self.desktop_canvas)
        main_layout.addWidget(self.taskbar)
        self.logger.info("Desktop Window Ready")