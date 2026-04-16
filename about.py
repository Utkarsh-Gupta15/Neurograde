from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5.QtCore import Qt


class AboutPage(QWidget):
    def __init__(self, mode="public"):
        super().__init__()
        self.setWindowTitle("About")
        self.showMaximized()

        # ✅ SAME BACKGROUND GRADIENT AS HOME / DATA ENTRY
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 900)
        gradient.setColorAt(0.0, QColor("#020617"))
        gradient.setColorAt(0.4, QColor("#071126"))
        gradient.setColorAt(1.0, QColor("#081423"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        if mode == "public":
            from UI.public_header import PublicHeader
            layout.addWidget(PublicHeader(self))
        else:
            from UI.private_header import PrivateHeader
            layout.addWidget(PrivateHeader(self))

        # Content card (glass look)
        content = QLabel(
            "About NeuroGrade\n\n"
            "NeuroGrade is an AI-based Student Performance Prediction System designed "
            "to analyze academic, behavioral, and lifestyle factors to predict a "
            "student’s future academic performance.\n\n"

            "The system leverages machine learning models trained on historical "
            "student data, including study habits, attendance, exam scores, "
            "participation in discussions, sleep patterns, and social media usage.\n\n"

            "By combining these parameters, NeuroGrade provides accurate performance "
            "predictions that can help educators identify at-risk students early and "
            "enable timely academic interventions.\n\n"

            "The platform features a modern, intuitive interface built using PyQt5, "
            "secure data storage through a MySQL database, and seamless integration "
            "with trained machine learning models for real-time predictions.\n\n"

            "NeuroGrade aims to support data-driven decision-making in education, "
            "improve learning outcomes, and promote personalized academic guidance "
            "through intelligent analytics."
        )

        content.setWordWrap(True)
        content.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        content.setMaximumWidth(1000)

        content.setAlignment(Qt.AlignCenter)
        content.setFont(QFont("Segoe UI", 18))
        content.setStyleSheet("""
            QLabel {
                color: #CFEFFF;
                background-color: rgba(8,14,28,220);
                border: 1px solid rgba(120,200,255,0.15);
                border-radius: 14px;
                padding: 40px;
            }
        """)

        layout.addStretch()
        layout.addWidget(content, alignment=Qt.AlignCenter)
        layout.addStretch()

    # ---------- Navigation ----------
    def goLogin(self):
        from UI.login_page import LoginPage
        self.login = LoginPage()
        self.login.showMaximized()
        self.close()

    def goHome(self):
        from UI.home import MainWindow
        self.home = MainWindow()
        self.home.showMaximized()
        self.close()

    def goAbout(self):
        pass

    def goHelp(self):
        from UI.help import HelpPage
        self.help = HelpPage()
        self.help.showMaximized()
        self.close()

    def goContact(self):
        from UI.contact import ContactPage
        self.contact = ContactPage()
        self.contact.showMaximized()
        self.close()

    def goLogout(self):
        self.goLogin()
