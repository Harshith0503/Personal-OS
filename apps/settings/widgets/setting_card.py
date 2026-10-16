from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)


class SettingCard(QFrame):
    def __init__(self, title, description=""):
        super().__init__()
        self.setObjectName("SettingCard")
        self.setStyleSheet("""
        #SettingCard{
            border:1px solid #555;
            border-radius:12px;
            padding:10px;
            background:#2D2D30;
        }
        """)
        layout = QVBoxLayout(self)
        title_label = QLabel(title)
        title_label.setStyleSheet("""
        font-size:16px;
        font-weight:bold;
        """)
        layout.addWidget(title_label)
        if description:
            desc = QLabel(description)
            desc.setWordWrap(True)
            desc.setStyleSheet("""
            color:gray;
            """)
            layout.addWidget(desc)
        self.body = QVBoxLayout()
        layout.addLayout(self.body)