from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout
)
from PyQt6.QtCore import Qt


class Dock(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.theme = app.theme
        self.build_ui()

    def build_ui(self):
        colors = self.theme.theme["colors"]
        self.setFixedHeight(80)
        self.setStyleSheet(f"""
            QWidget {{
                background: rgba(40,40,40,180);
                border: 1px solid {colors["border"]};
                border-radius:20px;
            }}
            QPushButton {{
                background: transparent;
                border:none;
                font-size:30px;
                padding:10px;
            }}
            QPushButton:hover {{
                background:{colors["surface_alt"]};
                border-radius:15px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        for app_info in self.app.registry.all():
            btn = QPushButton(app_info["icon"])
            btn.setToolTip(app_info["name"])
            btn.clicked.connect(
                lambda checked=False, app_id=app_info["id"]:
                    self.launch_app(app_id)
            )
            layout.addWidget(btn)

    def launch_app(self, app_id):
        app_info = self.app.registry.get(app_id)
        if app_info is None:
            return
        if (
            app_info["single_instance"]
            and self.app.process_manager.is_running(app_id)
        ):
            window = self.app.process_manager.get(app_id)
            if window.isHidden():
                window.show()
            self.app.window.desktop_canvas.desktop_area.window_manager.bring_to_front(window)
            return
        window = app_info["window"](self.app)
        window.move(150, 120)
        self.app.process_manager.start(
            app_id,
            window
        )
        self.app.window.desktop_canvas.desktop_area.window_manager.open_window(window)