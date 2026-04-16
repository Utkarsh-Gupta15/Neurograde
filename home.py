import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QMainWindow, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import os


# -------------------------------
# LinkLabel (SAME AS LOGIN PAGE)
# -------------------------------
class LinkLabel(QLabel):
    def __init__(self, text, font_size=20, parent=None):
        super().__init__(text, parent)
        self.font_size = font_size
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"color: #8FD3FF; font-size: {self.font_size}px;")

    def enterEvent(self, e):
        self.setStyleSheet(f"color: #00D1FF; font-size: {self.font_size}px;")
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setStyleSheet(f"color: #8FD3FF; font-size: {self.font_size}px;")
        super().leaveEvent(e)

    def mousePressEvent(self, event):
        if hasattr(self, "onClick"):
            self.onClick()


# -------------------------------
# Reusable Card Button (UNCHANGED)
# -------------------------------
class CardButton(QPushButton):
    def __init__(self, icon, title, description):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(550)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)
        layout.setContentsMargins(30, 30, 30, 30)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 54))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("color: #D9FAFF;")

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #E6FBFF;")

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #A8D9FF;")

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(12, 20, 40, 0.92);
                border-radius: 20px;
                border: 1px solid rgba(120, 200, 255, 0.25);
            }
            QPushButton:hover {
                background-color: rgba(18, 30, 60, 0.98);
                border: 1px solid rgba(120, 220, 255, 0.55);
            }
        """)


# -------------------------------
# Pages
# -------------------------------
class HomePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setSpacing(40)
        layout.setContentsMargins(40, 40, 40, 40)

        predict = CardButton(
            "📊",
            "Predict Performance",
            "Analyze and predict future performance metrics using AI."
        )

        view = CardButton(
            "📈",
            "View Model Details (NeuroGrade)",
            "View accuracy, precision, recall and F1 score."
        )

        # ✅ NEW CARD ADDED
        retrieve = CardButton(
            "🔎",
            "Retrieve Student Data",
            "Search and retrieve student records from database."
        )

        predict.clicked.connect(self.openDataEntry)
        view.clicked.connect(self.openModelDetails)

        retrieve.clicked.connect(self.openRetrieve)  # ✅ NEW CONNECTION

        layout.addWidget(predict)
        layout.addWidget(view)
        layout.addWidget(retrieve)  # ✅ NEW CARD ADDED TO LAYOUT

    def openDataEntry(self):
        from UI.data_entry_page import StudentPerformanceUI
        self.dataEntry = StudentPerformanceUI()
        self.dataEntry.showMaximized()

    # ✅ NEW METHOD
    def openRetrieve(self):
        from UI.retrieve import RetrievePage
        self.retrieve = RetrievePage()
        self.retrieve.showMaximized()

    def openModelDetails(self):
        from UI.modelDetails import ModelDetailsPage
        self.modelDetails = ModelDetailsPage()
        self.modelDetails.showMaximized()


class PredictPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📊 Predict Performance")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        back = QPushButton("Back to Home")
        back.clicked.connect(lambda: stack.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addWidget(back)


class ViewPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📈 View Prediction Details")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        back = QPushButton("Back to Home")
        back.clicked.connect(lambda: stack.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addWidget(back)


# -------------------------------
# Main Window (UNCHANGED)
# -------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroGrade")
        self.showMaximized()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, "assets", "background.jpg")

        self.bg_image = QLabel(self)
        self.bg_image.setPixmap(QPixmap(image_path))
        self.bg_image.setScaledContents(True)
        self.bg_image.setGeometry(self.rect())
        self.bg_image.lower()

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        from UI.private_header import PrivateHeader
        header = PrivateHeader(self)

        self.stack = QStackedWidget()
        self.stack.addWidget(HomePage(self.stack))
        self.stack.addWidget(PredictPage(self.stack))
        self.stack.addWidget(ViewPage(self.stack))

        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet(
            "background-color: #152D45; color: #9EE9FF; font-size: 14px;"
        )

        wrapper_layout.addWidget(header)
        wrapper_layout.addWidget(self.stack, 1)
        wrapper_layout.addWidget(footer)

        self.setCentralWidget(wrapper)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #020617,
                    stop:0.4 #071126,
                    stop:1 #081423
                );
            }
        """)

    def goHome(self):
        self.stack.setCurrentIndex(0)

    def goLogin(self):
        from UI.login_page import LoginPage
        self.login = LoginPage()
        self.login.showMaximized()
        self.close()

    def goAbout(self):
        from UI.about import AboutPage
        self.about = AboutPage(mode="private")
        self.about.showMaximized()

    def goHelp(self):
        from UI.help import HelpPage
        self.help = HelpPage(mode="private")
        self.help.showMaximized()
        self.close()

    def goLogout(self):
        self.goLogin()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
