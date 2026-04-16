from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QScrollArea, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PyQt5.QtCore import Qt


class ContactPage(QWidget):
    def __init__(self, mode="public"):
        super().__init__()
        self.setWindowTitle("Contact Us - NeuroGrade")
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
        title = QLabel("Contact Us")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
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
            "General Inquiries",
            "For general questions about NeuroGrade, features, or system usage:\n\n"
            "📧 Email: support@neurograde.ai\n"
            "📞 Phone: +91 98765 43210\n"
            "🕒 Working Hours: Monday – Friday (9:00 AM – 6:00 PM)"
        ))

        container_layout.addWidget(create_section(
            "Technical Support",
            "Facing technical issues or bugs?\n\n"
            "• Provide detailed description of the issue.\n"
            "• Include screenshots if possible.\n"
            "• Mention your system configuration.\n\n"
            "📧 techsupport@neurograde.ai"
        ))

        container_layout.addWidget(create_section(
            "Academic Collaboration",
            "Interested in integrating NeuroGrade into your institution?\n\n"
            "• Contact us for partnership opportunities.\n"
            "• Request institutional demo.\n"
            "• Discuss data-driven academic solutions.\n\n"
            "📧 partnerships@neurograde.ai"
        ))

        container_layout.addWidget(create_section(
            "Feedback & Suggestions",
            "We value your feedback.\n\n"
            "• Suggest improvements.\n"
            "• Report usability issues.\n"
            "• Share feature ideas.\n\n"
            "📧 feedback@neurograde.ai"
        ))

        container_layout.addStretch()

        scroll.setWidget(container)

        # stretch keeps footer at bottom
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
        from UI.help import HelpPage
        self.help = HelpPage(mode="private")
        self.help.showMaximized()
        self.close()

    def goContact(self):
        pass

    def goLogout(self):
        self.goLogin()
