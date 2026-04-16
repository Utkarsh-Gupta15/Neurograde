# main.py
import sys
from PyQt5.QtWidgets import QApplication
from UI.login_page import LoginPage

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Launch login page
    login_window = LoginPage()
    login_window.showMaximized()  # opens full screen

    sys.exit(app.exec_())
