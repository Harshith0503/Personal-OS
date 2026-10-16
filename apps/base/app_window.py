from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import (
    Qt, 
    QPoint,
    QRect
)
from PyQt6.QtGui import QColor, QGuiApplication


class AppWindow(QFrame):
    def __init__(self, app, title="Application", app_id=None):
        super().__init__()
        self.app = app
        self.window_manager = (
            self.app.window
            .desktop_canvas
            .desktop_area
            .window_manager
        )
        self.theme = app.theme
        self.title = title
        self.app_id = app_id
        self.dragging = False
        self.drag_position = QPoint()
        self.resizing = False
        self.resize_margin = 8
        self.resize_start = QPoint()
        self.start_size = self.size()
        self.is_maximized = False
        self.snap_mode = None
        self.snap_margin = 25
        self.normal_geometry = None
        self.minimum_width = 500
        self.minimum_height = 350
        self.build_ui()
        self.app.theme.theme_changed.connect(
            self.apply_theme
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

    def build_ui(self):
        colors = self.theme.theme["colors"]
        self.setObjectName("AppWindow")
        self.setMinimumSize(600, 400)
        self.setStyleSheet(f"""
        #AppWindow {{
            background: {colors["surface"]};
            border: 2px solid #3B82F6;
            border-radius: 12px;
        }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.titlebar = QWidget()
        self.titlebar.setFixedHeight(42)
        self.titlebar.setStyleSheet(f"""
        QWidget {{
            background: {colors["surface_alt"]};
            border-top-left-radius:12px;
            border-top-right-radius:12px;
        }}
        """)
        tb_layout = QHBoxLayout(self.titlebar)
        tb_layout.setContentsMargins(12, 0, 12, 0)
        title = QLabel(self.title)
        title.setStyleSheet(f"""
        color:{colors["text"]};
        font-size:14px;
        font-weight:bold;
        """)
        tb_layout.addWidget(title)
        tb_layout.addStretch()
        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("□")
        self.close_btn = QPushButton("✕")
        self.min_btn.clicked.connect(self.minimize)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.close_window)
        for btn in (
            self.min_btn,
            self.max_btn,
            self.close_btn
        ):
            btn.setFixedSize(28, 28)
            btn.setStyleSheet(f"""
            QPushButton {{
                border:none;
                background:transparent;
                color:{colors["text"]};
                font-size:14px;
                font-weight:bold;
                border-radius:6px;
            }}
            QPushButton:hover {{
                background:{colors["surface"]};
            }}
            QPushButton:pressed {{
                background:{colors["border"]};
            }}
            """)
        self.close_btn.setStyleSheet("""
        QPushButton{
            border:none;
            background:transparent;
            color:white;
            border-radius:6px;
        }
        QPushButton:hover{
            background:#E81123;
        }
        QPushButton:pressed{
            background:#C50F1F;
        }
        """)
        tb_layout.addWidget(self.min_btn)
        tb_layout.addWidget(self.max_btn)
        tb_layout.addWidget(self.close_btn)
        layout.addWidget(self.titlebar)
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )
        layout.addWidget(self.content)

    def mousePressEvent(self, event):
        self.window_manager.bring_to_front(self)
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.in_resize_zone(event.position().toPoint())
        ):
            self.resizing = True
            self.resize_start = event.globalPosition().toPoint()
            self.start_size = self.size()
            event.accept()
            return
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.titlebar.geometry().contains(
                event.position().toPoint()
            )
        ):
            self.dragging = True
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.in_resize_zone(event.position().toPoint()):
            self.setCursor(
                Qt.CursorShape.SizeFDiagCursor
            )
        else:
            self.setCursor(
                Qt.CursorShape.ArrowCursor
            )
        if self.resizing:
            delta = (
                event.globalPosition().toPoint()
                - self.resize_start
            )
            new_width = max(
                self.minimum_width,
                self.start_size.width() + delta.x()
            )
            new_height = max(
                self.minimum_height,
                self.start_size.height() + delta.y()
            )
            self.resize(
                new_width,
                new_height
            )
            return
        if self.dragging:
            global_pos = event.globalPosition().toPoint()
            self.move(
                global_pos - self.drag_position
            )
            parent_rect = self.window_manager.rect()
            pos = self.pos()
            if pos.y() <= 10:
                self.snap_mode = "maximize"
            elif pos.x() <= 10:
                self.snap_mode = "left"
            elif pos.x() + self.width() >= parent_rect.width() - 10:
                self.snap_mode = "right"
            else:
                self.snap_mode = None
            screen = QGuiApplication.primaryScreen().availableGeometry()
            if global_pos.y() <= screen.top() + self.snap_margin:
                self.snap_mode = "maximize"
            elif global_pos.x() <= screen.left() + self.snap_margin:
                self.snap_mode = "left"
            elif global_pos.x() >= screen.right() - self.snap_margin:
                self.snap_mode = "right"
            else:
                self.snap_mode = None
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.dragging and self.snap_mode is not None:
            self.window_manager.snap_window(
                self,
                self.snap_mode
            )
        self.dragging = False
        self.resizing = False
        self.snap_mode = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.titlebar.geometry().contains(
                event.position().toPoint()
            )
        ):
            self.toggle_maximize()
        super().mouseDoubleClickEvent(event)

    def minimize(self):
        self.hide()

    def toggle_maximize(self):
        if not self.is_maximized:
            self.window_manager.snap_window(
                self,
                "maximize"
            )
        else:
            self.window_manager.restore_window(
                self
            )

    def close_window(self):
        self.window_manager.unregister(self)
        if (
            self.app_id is not None
            and self.app_id in self.app.running_apps
        ):
            self.app.process_manager.stop(
                self.app_id
            )
        self.close()

    def in_resize_zone(self, pos):
        return (
            pos.x() >= self.width() - self.resize_margin
            and
            pos.y() >= self.height() - self.resize_margin
        )

    def apply_theme(self):
        colors = self.app.theme.theme["colors"]
        self.setStyleSheet(f"""
        #AppWindow {{
            background:{colors["surface"]};
            border:2px solid {colors["border"]};
            border-radius:12px;
        }}
        """)
        self.titlebar.setStyleSheet(f"""
        QWidget {{
            background:{colors["surface_alt"]};
            border-top-left-radius:12px;
            border-top-right-radius:12px;
        }}
        """)