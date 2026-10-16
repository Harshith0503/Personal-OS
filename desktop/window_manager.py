from PyQt6.QtCore import QObject, pyqtSignal, QRect
from PyQt6.QtWidgets import QWidget


class WindowManager(QWidget):
    active_window_changed = pyqtSignal(object)
    windows_changed = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.windows = []
        self.active_window = None

    def register(self, window):
        if window not in self.windows:
            self.windows.append(window)
            self.windows_changed.emit()

    def unregister(self, window):
        if window in self.windows:
            self.windows.remove(window)
            self.windows_changed.emit()
        if self.active_window == window:
            self.active_window = None
            self.active_window_changed.emit(None)

    def bring_to_front(self, window):
        if window not in self.windows:
            return
        self.windows.remove(window)
        self.windows.append(window)
        self.active_window = window
        window.raise_()
        window.activateWindow()
        self.active_window_changed.emit(window)

    def open_window(self, window):
        window.setParent(self)
        self.register(window)
        window.show()
        self.bring_to_front(window)

    def snap_window(self, window, mode):
        rect = self.rect()
        if mode == "maximize":
            window.normal_geometry = window.geometry()
            window.setGeometry(rect)
            window.is_maximized = True
        elif mode == "left":
            window.normal_geometry = window.geometry()
            window.setGeometry(
                QRect(
                    0,
                    0,
                    rect.width() // 2,
                    rect.height()
                )
            )
            window.is_maximized = False
        elif mode == "right":
            window.normal_geometry = window.geometry()
            window.setGeometry(
                QRect(
                    rect.width() // 2,
                    0,
                    rect.width() // 2,
                    rect.height()
                )
            )
            window.is_maximized = False

    def restore_window(self, window):
        if window.normal_geometry is not None:
            window.setGeometry(window.normal_geometry)
            window.is_maximized = False