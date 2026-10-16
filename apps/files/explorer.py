from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from apps.base.app_window import AppWindow
from apps.files.toolbar import ExplorerToolbar
from apps.files.sidebar import ExplorerSidebar
from apps.files.file_view import FileView


class FileExplorer(AppWindow):
    def __init__(self, app):
        super().__init__(
            app,
            "File Explorer",
            app_id="files"
        )
        self.build_content()
        self.connect_signals()

    def build_content(self):
        layout = QVBoxLayout()
        self.toolbar = ExplorerToolbar(self.app)
        layout.addWidget(self.toolbar)
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        self.sidebar = ExplorerSidebar(self.app)
        self.sidebar.setFixedWidth(220)
        self.file_view = FileView(self.app)
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.file_view)
        layout.addWidget(body)
        self.content_layout.addLayout(layout)

    def connect_signals(self):
        self.sidebar.location_selected.connect(
            self.file_view.open_path
        )
        self.toolbar.back_clicked.connect(
            self.file_view.go_back
        )
        self.toolbar.forward_clicked.connect(
            self.file_view.go_forward
        )
        self.toolbar.up_clicked.connect(
            self.file_view.go_up
        )
        self.toolbar.refresh_clicked.connect(
            self.file_view.refresh
        )
        self.toolbar.path_entered.connect(
            self.file_view.open_path
        )
        self.toolbar.set_path(
            self.file_view.current_path()
        )
        self.file_view.path_changed.connect(
            self.toolbar.set_path
        )

    def update_path_bar(self, index):
        self.toolbar.set_path(
            self.file_view.current_path()
        )