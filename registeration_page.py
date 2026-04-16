# registeration_page.py
import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QPixmap
from PyQt5.QtCore import Qt
import pymysql
import os


class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFont(QFont("Segoe UI", 13))

        # --- Background gradient ---
        palette = QPalette()
        grad = QLinearGradient(0, 0, 0, 900)
        grad.setColorAt(0.0, QColor("#020617"))
        grad.setColorAt(0.4, QColor("#071126"))
        grad.setColorAt(1.0, QColor("#081423"))
        palette.setBrush(QPalette.Window, QBrush(grad))
        self.setPalette(palette)

        # --- Background image ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(base_dir, "assets", "background.jpg")

        self.bg_image = QLabel(self)
        self.bg_image.setPixmap(QPixmap(image_path))
        self.bg_image.setScaledContents(True)
        self.bg_image.setGeometry(self.rect())
        self.bg_image.lower()

        # --- Main layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- HEADER ---
        header = QFrame()
        header.setFixedHeight(78)
        header.setStyleSheet("background-color: #152D45;")
        headerLayout = QHBoxLayout(header)
        headerLayout.setContentsMargins(20, 0, 20, 0)
        headerLayout.setSpacing(36)

        titleLabel = QLabel("NeuroGrade")
        titleLabel.setFont(QFont("Segoe UI", 24, QFont.Bold))
        titleLabel.setStyleSheet("color: #9EE9FF;")
        headerLayout.addWidget(titleLabel)
        headerLayout.addStretch()
        main_layout.addWidget(header)

        # --- STAGE FRAME (central form container) ---
        stage = QFrame()
        stage.setStyleSheet("""
            QFrame {
                background-color: rgba(120,200,255,0.05);
                border-radius: 26px;
            }
        """)
        stageLayout = QVBoxLayout(stage)
        stageLayout.setContentsMargins(36, 36, 36, 36)

        # Inner container
        container = QFrame()
        container.setFixedWidth(540)
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(8,14,28,150);
                border: 1px solid rgba(120,200,255,0.10);
                border-radius: 14px;
            }
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(22)

        # --- Form Title ---
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #9EE9FF;")
        layout.addWidget(title)

        # --- Input fields ---
        self.username = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.confirm_password = QLineEdit()
        for f in [self.username, self.email, self.password, self.confirm_password]:
            f.setFixedHeight(48)
            f.setFont(QFont("Segoe UI", 14))
            f.setStyleSheet("""
                QLineEdit {
                    background-color: #061224;
                    color: white;
                    border: 2px solid rgba(120,200,255,0.25);
                    border-radius: 8px;
                    padding-left: 12px;
                }
                QLineEdit:focus {
                    border: 2px solid #00D7FF;
                }
            """)
        self.username.setPlaceholderText("Username")
        self.email.setPlaceholderText("Email")
        self.password.setPlaceholderText("Password")
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)

        # --- Show password checkbox ---
        show_pass = QCheckBox("Show Passwords")
        show_pass.setStyleSheet("color: #CFF5FF; font-size: 14px;")
        show_pass.stateChanged.connect(
            lambda s: [
                self.password.setEchoMode(QLineEdit.Normal if s else QLineEdit.Password),
                self.confirm_password.setEchoMode(QLineEdit.Normal if s else QLineEdit.Password)
            ]
        )
        layout.addWidget(show_pass)

        # --- Register button ---
        register_btn = QPushButton("Register")
        register_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        register_btn.setFixedHeight(52)
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #00AEEF, stop:1 #00D7FF);
                color: #02101A;
                border-radius: 10px;
            }
        """)
        layout.addWidget(register_btn)

        # --- Login link ---
        login_link = QLabel("Already have an account? <a href='#'>Login</a>")
        login_link.setAlignment(Qt.AlignCenter)
        login_link.setStyleSheet("color: #8FD3FF; font-size: 16px;")
        login_link.setOpenExternalLinks(False)
        layout.addWidget(login_link)

        login_link.mousePressEvent = self.goToLogin
        register_btn.clicked.connect(self.register_user)

        stageLayout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.addWidget(stage, alignment=Qt.AlignCenter)

        # --- FOOTER ---
        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet("background-color: #152D45; color: #9EE9FF; font-size: 14px;")
        main_layout.addWidget(footer)

    # --- Resize background properly ---
    def resizeEvent(self, event):
        self.bg_image.setGeometry(self.rect())
        super().resizeEvent(event)

    # --- Registration logic ---
    def register_user(self):
        u, e, p, c = self.username.text().strip(), self.email.text().strip(), self.password.text().strip(), self.confirm_password.text().strip()
        if not u or not e or not p or not c:
            QMessageBox.warning(self, "Input Error", "Fill all fields.")
            return
        if p != c:
            QMessageBox.warning(self, "Password Error", "Passwords do not match.")
            return
        try:
            conn = pymysql.connect(host="localhost", user="root", password="root", database="userdb")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)", (u,e,p))
            conn.commit()
            QMessageBox.information(self,"Success","Registration complete!")
            cursor.close()
            conn.close()
        except pymysql.MySQLError as ex:
            QMessageBox.critical(self,"Database Error",str(ex))

    def goToLogin(self,_):
        from UI.login_page import LoginPage
        self.login = LoginPage()
        self.login.showMaximized()
        self.close()
