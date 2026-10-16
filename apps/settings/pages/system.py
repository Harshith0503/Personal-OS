from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SystemPage(QWidget):
    def __init__(self, app):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("System")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        layout.addWidget(title)
        layout.addStretch()