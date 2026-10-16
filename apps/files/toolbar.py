from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit
)


class ExplorerToolbar(QWidget):
    back_clicked = pyqtSignal()
    forward_clicked = pyqtSignal()
    up_clicked = pyqtSignal()
    refresh_clicked = pyqtSignal()
    path_entered = pyqtSignal(str)

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.build_ui()
        self.connect_signals()

    def build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.up_btn = QPushButton("↑")
        self.refresh_btn = QPushButton("⟳")
        self.path_bar = QLineEdit()
        self.path_bar.setPlaceholderText("Enter folder path...")
        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.up_btn)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.path_bar)

    def connect_signals(self):
        self.back_btn.clicked.connect(
            self.back_clicked.emit
        )
        self.forward_btn.clicked.connect(
            self.forward_clicked.emit
        )
        self.up_btn.clicked.connect(
            self.up_clicked.emit
        )
        self.refresh_btn.clicked.connect(
            self.refresh_clicked.emit
        )
        self.path_bar.returnPressed.connect(
            self.emit_path
        )

    def emit_path(self):
        self.path_entered.emit(
            self.path_bar.text()
        )

    def set_path(self, path):
        self.path_bar.setText(path)