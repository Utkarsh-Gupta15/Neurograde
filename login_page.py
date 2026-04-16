# login_page.py
import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QFrame, QCheckBox, QApplication, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QPixmap
from PyQt5.QtCore import Qt
import pymysql
import os


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


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFont(QFont("Segoe UI", 13))

        # -------- Background --------
        palette = QPalette()
        grad = QLinearGradient(0, 0, 0, 900)
        grad.setColorAt(0.0, QColor("#020617"))
        grad.setColorAt(0.4, QColor("#071126"))
        grad.setColorAt(1.0, QColor("#081423"))
        palette.setBrush(QPalette.Window, QBrush(grad))
        self.setPalette(palette)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, "assets", "background.jpg")

        self.bg_image = QLabel(self)
        self.bg_image.setPixmap(QPixmap(image_path))
        self.bg_image.setScaledContents(True)
        self.bg_image.setGeometry(self.rect())
        self.bg_image.lower()

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # -------- Header --------
        from UI.public_header import PublicHeader
        header = PublicHeader(self)
        mainLayout.addWidget(header)

        # -------- Login Form --------
        container = QFrame()
        container.setFixedWidth(500)
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(8,14,28,150);
                border: 1px solid rgba(120,200,255,0.10);
                border-radius: 14px;
            }
        """)

        containerLayout = QVBoxLayout(container)
        containerLayout.setContentsMargins(40, 40, 40, 40)
        containerLayout.setSpacing(22)

        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #9EE9FF;")
        containerLayout.addWidget(title)

        subtitle = QLabel("Welcome back. Please sign in to continue.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #BFE9FF; font-size: 14px;")
        containerLayout.addWidget(subtitle)

        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        for fld in (self.emailInput, self.passwordInput):
            fld.setFixedHeight(48)
            fld.setFont(QFont("Segoe UI", 14))
            fld.setStyleSheet("""
                QLineEdit {
                    background-color: #061224;
                    color: white;
                    border: 2px solid rgba(120,200,255,0.25);
                    border-radius: 8px;
                    padding-left: 12px;
                }
                QLineEdit:focus {
                    border: 2px solid #00D1FF;
                }
            """)

        self.emailInput.setPlaceholderText("Email")
        self.passwordInput.setPlaceholderText("Password")

        containerLayout.addWidget(self.emailInput)
        containerLayout.addWidget(self.passwordInput)

        showPass = QCheckBox("Show Password")
        showPass.setStyleSheet("color: #BFE9FF; font-size: 14px;")
        showPass.stateChanged.connect(
            lambda s: self.passwordInput.setEchoMode(
                QLineEdit.Normal if s else QLineEdit.Password
            )
        )
        containerLayout.addWidget(showPass)

        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setStyleSheet("color: #FF7A7A; font-size: 14px;")
        self.message.setVisible(False)
        containerLayout.addWidget(self.message)

        loginBtn = QPushButton("Login")
        loginBtn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        loginBtn.setFixedHeight(52)
        loginBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00AEEF, stop:1 #00D7FF);
                color: #02101A;
                border-radius: 10px;
            }
        """)
        containerLayout.addWidget(loginBtn)

        # ===== ONLY NEW ADDITION (SAFE) =====
        createAccount = LinkLabel("New user? Create Account", font_size=15)
        createAccount.setAlignment(Qt.AlignCenter)
        createAccount.onClick = self.goRegister
        containerLayout.addWidget(createAccount)
        # ===================================

        mainLayout.addStretch()
        mainLayout.addWidget(container, alignment=Qt.AlignCenter)
        mainLayout.addStretch()

        # -------- Footer --------
        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet("background-color: #152D45; color: #9EE9FF; font-size: 14px;")
        mainLayout.addWidget(footer)

        loginBtn.clicked.connect(self.validateLogin)

    # -------- Logic --------
    def validateLogin(self):
        email = self.emailInput.text().strip()
        pwd = self.passwordInput.text().strip()

        if not email or not pwd:
            self.message.setText("Enter both email and password.")
            self.message.setVisible(True)
            return

        try:
            conn = pymysql.connect(
                host="localhost",
                user="",
                password="",
                database=""
            )
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, pwd)
            )
            result = cursor.fetchone()

            if result:
                from UI.home import MainWindow
                self.home = MainWindow()
                self.home.showMaximized()
                self.close()
            else:
                self.message.setText("Invalid email or password.")
                self.message.setVisible(True)

            cursor.close()
            conn.close()

        except pymysql.MySQLError as err:
            QMessageBox.critical(self, "Database Error", str(err))

    def goRegister(self):
        from UI.registeration_page import RegisterPage
        self.register = RegisterPage()
        self.register.showMaximized()
        self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_image.setGeometry(self.rect())

    def goLogin(self):
        pass  # already on login page

    def goAbout(self):
        from UI.about import AboutPage
        self.about = AboutPage()
        self.about.showMaximized()
        self.hide()

    def goHelp(self):
        from UI.help import HelpPage
        self.help = HelpPage()
        self.help.showMaximized()
        self.hide()

    def goContact(self):
        from UI.contactUs import ContactPage
        self.contact = ContactPage()
        self.contact.showMaximized()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.showMaximized()
    sys.exit(app.exec_())
