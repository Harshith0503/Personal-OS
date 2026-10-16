from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout
)

from apps.settings.widgets.setting_card import SettingCard


class AppearancePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Appearance")
        title.setStyleSheet("""
        font-size:28px;
        font-weight:bold;
        """)
        self.current_theme = QLabel(
            f"Current Theme: {self.app.theme.current_theme()}"
        )
        self.current_theme.setStyleSheet("""
        font-size:16px;
        color:gray;
        """)
        layout.addWidget(self.current_theme)
        layout.addWidget(title)
        theme_card = SettingCard(
            "Theme",
            "Choose the appearance of HarshOS."
        )
        row = QHBoxLayout()
        self.dark_btn = QPushButton("🌙 Dark")
        self.light_btn = QPushButton("☀ Light")
        self.dark_btn.clicked.connect(
            lambda: self.change_theme("dark")
        )
        self.light_btn.clicked.connect(
            lambda: self.change_theme("light")
        )
        row.addWidget(self.dark_btn)
        row.addWidget(self.light_btn)
        theme_card.body.addLayout(row)
        layout.addWidget(theme_card)
        layout.addStretch()

    def change_theme(self, theme_name):
        self.app.theme.load_theme(theme_name)
        self.current_theme.setText(
            f"Current Theme: {theme_name}"
        )
        self.refresh_ui()

    def refresh_ui(self):
        self.app.window.repaint()
        for _, window in self.app.process_manager.all():
            window.repaint()