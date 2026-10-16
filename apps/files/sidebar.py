from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QListWidget,
    QVBoxLayout
)


class ExplorerSidebar(QWidget):
    location_selected = pyqtSignal(str)
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout(self)
        self.list = QListWidget()
        self.locations = {
            "🏠 Home": Path.home(),
            "🖥 Desktop": Path.home() / "Desktop",
            "📄 Documents": Path.home() / "Documents",
            "⬇ Downloads": Path.home() / "Downloads",
            "🖼 Pictures": Path.home() / "Pictures",
            "🎵 Music": Path.home() / "Music",
            "🎬 Videos": Path.home() / "Videos",
            "💻 This PC": Path.home()
        }
        self.list.addItems(self.locations.keys())
        self.list.itemClicked.connect(
            self.item_clicked
        )
        layout.addWidget(self.list)

    def item_clicked(self, item):
        path = self.locations[item.text()]
        if path.exists():
            self.location_selected.emit(str(path))