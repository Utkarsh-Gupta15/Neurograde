from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5.QtCore import Qt


class HelpPage(QWidget):
    def __init__(self, mode="public"):
        super().__init__()
        self.setWindowTitle("Help - NeuroGrade")
        self.showMaximized()

        # ================= BACKGROUND (SAME AS HOME) =================
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 900)
        gradient.setColorAt(0.0, QColor("#020617"))
        gradient.setColorAt(0.4, QColor("#071126"))
        gradient.setColorAt(1.0, QColor("#081423"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # ================= MAIN LAYOUT =================
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= HEADER =================
        if mode == "private":
            from UI.private_header import PrivateHeader
            header = PrivateHeader(self)
        else:
            from UI.public_header import PublicHeader
            header = PublicHeader(self)

        main_layout.addWidget(header)

        # ================= SCROLL AREA =================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(80, 60, 80, 60)
        container_layout.setSpacing(40)

        # ================= PAGE TITLE =================
        title = QLabel("Help & User Guide")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setStyleSheet("color: #38BDF8;")
        title.setAlignment(Qt.AlignLeft)
        container_layout.addWidget(title)

        # ================= SECTION CREATOR =================
        def create_section(heading, text):
            section = QFrame()
            section.setStyleSheet("""
                QFrame {
                    background-color: rgba(8,14,28,220);
                    border: 1px solid rgba(120,200,255,0.15);
                    border-radius: 14px;
                }
            """)

            layout = QVBoxLayout(section)
            layout.setContentsMargins(50, 40, 50, 40)
            layout.setSpacing(20)

            h = QLabel(heading)
            h.setFont(QFont("Segoe UI", 22, QFont.Bold))
            h.setStyleSheet("color: #7DD3FC;")
            h.setAlignment(Qt.AlignLeft)

            body = QLabel(text)
            body.setFont(QFont("Segoe UI", 17))
            body.setStyleSheet("color: #E2E8F0;")
            body.setWordWrap(True)
            body.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            layout.addWidget(h)
            layout.addWidget(body)

            return section

        # ================= SECTIONS =================
        container_layout.addWidget(create_section(
            "1. Registration",
            "• Open the application.\n"
            "• Click 'Create Account' on the login page.\n"
            "• Enter Full Name, Email and Password.\n"
            "• Click Create Account.\n"
            "• Use your credentials to log in."
        ))

        container_layout.addWidget(create_section(
            "2. Login",
            "• Enter your registered Email and Password.\n"
            "• Click Login.\n"
            "• If login fails, verify email spelling and password."
        ))

        container_layout.addWidget(create_section(
            "3. Using the Prediction System",
            "After login you will see:\n\n"
            "• Predict Performance\n"
            "• View Model Details\n"
            "• Retrieve Student Data\n\n"
            "Retrieve Student Data:\n"
            "• Enter Student ID\n"
            "• Click Fetch\n\n"
            "Prediction Page:\n"
            "• Fill all required student details\n"
            "• Click Predict"
        ))

        container_layout.addWidget(create_section(
            "4. Understanding Results",
            "After prediction you will see:\n\n"
            "• Predicted Final Grade\n"
            "• Performance Charts\n"
            "• Personalized Suggestions\n\n"
            "Suggestions are generated using historical student data."
        ))

        container_layout.addWidget(create_section(
            "5. Downloading Charts",
            "• Click 'Download Charts'\n"
            "• Charts are saved in the project directory."
        ))

        container_layout.addWidget(create_section(
            "6. Logout",
            "• Click Logout in the top navigation bar.\n"
            "• You will be redirected to Login page.\n"
            "• Session closes securely."
        ))

        container_layout.addStretch()

        scroll.setWidget(container)

        # IMPORTANT: stretch factor 1 keeps footer at bottom
        main_layout.addWidget(scroll, 1)

        # ================= FOOTER =================
        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet(
            "background-color: #152D45; color: #9EE9FF; font-size: 14px;"
        )

        main_layout.addWidget(footer)

    # ================= NAVIGATION =================
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
        from UI.about import AboutPage
        self.about = AboutPage(mode="private")
        self.about.showMaximized()
        self.close()

    def goHelp(self):
        pass

    def goContact(self):
        from UI.contact import ContactPage
        self.contact = ContactPage()
        self.contact.showMaximized()
        self.close()

    def goLogout(self):
        self.goLogin()
