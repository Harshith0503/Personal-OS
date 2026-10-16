from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PyQt6.QtGui import QFont
from datetime import datetime


class Taskbar(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.logger = app.logger
        self.theme = app.theme
        self.build_ui()
        self.app.process_manager.processes_changed.connect(
            self.refresh_running_apps
        )
        self.app.window_manager.active_window_changed.connect(
            self.refresh_running_apps
        )
        self.start_clock()
        self.refresh_running_apps()

    def build_ui(self):
        colors = self.theme.theme["colors"]
        self.setFixedHeight(45)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors["surface"]};
                border-top: 1px solid {colors["border"]};
            }}
            QPushButton {{
                background: transparent;
                color: {colors["text"]};
                border: none;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {colors["surface_alt"]};
            }}
            QLabel {{
                color: {colors["text"]};
                font-size: 13px;
            }}
        """)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(8)
        logo = QLabel("🖥 HarshOS")
        logo.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )
        self.search_btn = QPushButton("🔍 Search")
        self.notify_btn = QPushButton("🔔")
        self.clock = QLabel()
        self.layout.addWidget(logo)
        self.layout.addWidget(self.search_btn)
        self.layout.addStretch()
        self.running_apps_container = QWidget()
        self.running_layout = QHBoxLayout(self.running_apps_container)
        self.running_layout.setContentsMargins(0, 0, 0, 0)
        self.running_layout.setSpacing(4)
        self.layout.addWidget(self.running_apps_container)
        self.layout.addWidget(self.notify_btn)
        self.layout.addWidget(self.clock)

    def start_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        self.clock.setText(
            now.strftime("%d %b %Y   %H:%M:%S")
        )

    def refresh_running_apps(self):
        while self.running_layout.count():
            item = self.running_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for app_id, window in self.app.process_manager.all():
            app_info = self.app.registry.get(app_id)
            if app_info is None:
                continue
            btn = QPushButton(app_info["icon"])
            if window == self.app.window_manager.active_window:
                btn.setStyleSheet("""
                    QPushButton{
                        background:#2563EB;
                        border-radius:8px;
                        color:white;
                        font-size:18px;
                        padding:4px;
                    }
                """)
            btn.setToolTip(app_info["name"])
            btn.clicked.connect(
                lambda checked=False, w=window:
                    self.toggle_window(w)
            )
            self.running_layout.addWidget(btn)

    def toggle_window(self, window):
        if window == self.app.window_manager.active_window:
            window.hide()
            self.app.window_manager.active_window = None
            self.refresh_running_apps()
            return
        if window.isHidden():
            window.show()
        self.app.window_manager.bring_to_front(window)