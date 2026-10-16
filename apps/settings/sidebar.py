from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem
)


class SettingsSidebar(QWidget):
    page_changed = pyqtSignal(str)

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        self.menu = QListWidget()
        pages = [
            ("appearance", "🎨 Appearance"),
            ("wallpaper", "🖼 Wallpaper"),
            ("themes", "🌙 Themes"),
            ("system", "⚙ System"),
            ("about", "ℹ About"),
        ]
        for page_id, title in pages:
            item = QListWidgetItem(title)
            item.setData(1, page_id)
            self.menu.addItem(item)
        self.menu.setCurrentRow(0)
        self.menu.currentItemChanged.connect(
            self.on_page_changed
        )
        layout.addWidget(self.menu)

    def on_page_changed(self, current, previous):
        if current is None:
            return
        page_id = current.data(1)
        self.page_changed.emit(page_id)