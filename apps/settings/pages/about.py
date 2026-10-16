from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class AboutPage(QWidget):
    def __init__(self, app):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("About HarshOS")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        layout.addWidget(title)
        info = QLabel(
            "HarshOS\n\n"
            "Version 0.1 Alpha\n\n"
            "Built with Python & PyQt6"
        )
        layout.addWidget(info)
        layout.addStretch()