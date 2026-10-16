from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class WallpaperPage(QWidget):
    def __init__(self, app):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Wallpaper")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        layout.addWidget(title)
        layout.addStretch()