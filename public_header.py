from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LinkLabel(QLabel):
    def __init__(self, text, font_size=20, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"color: #8FD3FF; font-size: {font_size}px;")

    def enterEvent(self, e):
        self.setStyleSheet("color: #00D1FF; font-size: 20px;")

    def leaveEvent(self, e):
        self.setStyleSheet("color: #8FD3FF; font-size: 20px;")

    def mousePressEvent(self, event):
        if hasattr(self, "onClick"):
            self.onClick()


class PublicHeader(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(78)
        self.setStyleSheet("background-color: #152D45;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(36)

        title = QLabel("NeuroGrade")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #9EE9FF;")

        layout.addWidget(title)
        layout.addStretch()

        for link in ["Login", "About", "Help", "Contact Us"]:
            lbl = LinkLabel(link)

            if link == "Login":
                lbl.onClick = parent.goLogin
            elif link == "About":
                lbl.onClick = parent.goAbout
            elif link == "Help":
                lbl.onClick = parent.goHelp
            elif link == "Contact Us":
                lbl.onClick = parent.goContact

            layout.addWidget(lbl)
