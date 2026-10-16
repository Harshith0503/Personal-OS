from PyQt6.QtCore import QObject


class ThemedWidget(QObject):
    def register_theme(self):
        self.app.theme.theme_changed.connect(
            self.apply_theme
        )

    def apply_theme(self):
        pass