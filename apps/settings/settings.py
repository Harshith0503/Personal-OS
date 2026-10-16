from PyQt6.QtWidgets import (
    QHBoxLayout
)

from apps.base.app_window import AppWindow
from apps.settings.sidebar import SettingsSidebar
from apps.settings.content import SettingsContent


class SettingsApp(AppWindow):
    def __init__(self, app):
        super().__init__(
            app,
            "Settings",
            app_id="settings"
        )
        self.build_content()

    def build_content(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.sidebar = SettingsSidebar(self.app)
        self.sidebar.setFixedWidth(230)
        self.content = SettingsContent(self.app)
        self.sidebar.page_changed.connect(
            self.content.set_page
        )
        layout.addWidget(self.sidebar)
        layout.addWidget(self.content)
        self.content_layout.addLayout(layout)