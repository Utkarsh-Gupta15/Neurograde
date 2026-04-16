import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QTextEdit, QMainWindow,
    QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #0F1E33;
                border-radius: 15px;
            }
        """)
        self.setContentsMargins(20, 20, 20, 20)


class ModelDetailsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Dashboard - NeuroGrade")
        self.showMaximized()

        wrapper = QWidget()
        outer_layout = QVBoxLayout(wrapper)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # ================= HEADER =================
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("background-color: #152D45;")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        project_title = QLabel("NeuroGrade")
        project_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        project_title.setStyleSheet("color: #9EE9FF;")

        home_btn = QPushButton("Home")
        home_btn.setFixedHeight(35)
        home_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E3A5F;
                color: #8FD3FF;
                border-radius: 8px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #254D78;
                color: #00D1FF;
            }
        """)
        home_btn.clicked.connect(self.goHome)

        header_layout.addWidget(project_title)
        header_layout.addStretch()
        header_layout.addWidget(home_btn)

        outer_layout.addWidget(header)

        # ================= CONTENT =================
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)

        # -------- TITLE --------
        title = QLabel("📊 Model Performance Dashboard")
        title.setFont(QFont("Segoe UI", 34, QFont.Bold))
        title.setStyleSheet("color: #E6FBFF;")
        main_layout.addWidget(title)

        # -------- KPI CARDS --------
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(20)

        kpi_layout.addWidget(self.create_kpi("Validation Accuracy", "99.62%"))
        kpi_layout.addWidget(self.create_kpi("Test Accuracy", "99.50%"))
        kpi_layout.addWidget(self.create_kpi("Epochs", "50"))

        main_layout.addLayout(kpi_layout)

        # -------- GRAPHS --------
        graph_layout = QGridLayout()
        graph_layout.setSpacing(20)

        self.acc_canvas = self.create_dark_graph()
        self.loss_canvas = self.create_dark_graph()

        self.plot_accuracy()
        self.plot_loss()

        graph_layout.addWidget(self.wrap_card("Accuracy Curve", self.acc_canvas), 0, 0)
        graph_layout.addWidget(self.wrap_card("Loss Curve", self.loss_canvas), 0, 1)

        main_layout.addLayout(graph_layout)

        # -------- REPORT --------
        report_card = Card()
        report_layout = QVBoxLayout(report_card)

        report_title = QLabel("Classification Report")
        report_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        report_title.setStyleSheet("color: #9EE9FF;")

        report_text = QTextEdit()
        report_text.setReadOnly(True)
        report_text.setFont(QFont("Consolas", 13))
        report_text.setStyleSheet("""
            QTextEdit {
                background-color: #081423;
                border-radius: 10px;
                padding: 15px;
                color: #A8D9FF;
            }
        """)
        report_text.setText(
            "Class A → Precision: 1.00 | Recall: 1.00 | F1: 1.00\n"
            "Class B → Precision: 1.00 | Recall: 1.00 | F1: 1.00\n"
            "Class C → Precision: 0.98 | Recall: 1.00 | F1: 0.99\n"
            "Class D → Precision: 1.00 | Recall: 0.99 | F1: 0.99\n\n"
            "Overall Accuracy: 99%"
        )

        export_btn = QPushButton("Export Report to PDF")
        export_btn.setFixedHeight(45)
        export_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        export_btn.clicked.connect(self.export_pdf)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E3A5F;
                border-radius: 10px;
                color: #8FD3FF;
            }
            QPushButton:hover {
                background-color: #254D78;
                color: #00D1FF;
            }
        """)

        report_layout.addWidget(report_title)
        report_layout.addWidget(report_text)
        report_layout.addWidget(export_btn)

        main_layout.addWidget(report_card)

        outer_layout.addWidget(content_widget, 1)

        # ================= FOOTER =================
        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet(
            "background-color: #152D45; color: #9EE9FF; font-size: 14px;"
        )

        outer_layout.addWidget(footer)

        self.setCentralWidget(wrapper)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #020617,
                    stop:1 #071126
                );
            }
        """)

    # ================= NAVIGATION =================
    def goHome(self):
        from UI.home import MainWindow
        self.home = MainWindow()
        self.home.showMaximized()
        self.close()

    # ================= KPI CARD =================
    def create_kpi(self, label, value):
        card = Card()
        layout = QVBoxLayout(card)

        lbl = QLabel(label)
        lbl.setFont(QFont("Segoe UI", 14))
        lbl.setStyleSheet("color: #9EE9FF;")

        val = QLabel(value)
        val.setFont(QFont("Segoe UI", 28, QFont.Bold))
        val.setStyleSheet("color: #E6FBFF;")

        layout.addWidget(lbl)
        layout.addWidget(val)
        return card

    # ================= GRAPH =================
    def create_dark_graph(self):
        fig = Figure(facecolor="#0F1E33")
        canvas = FigureCanvas(fig)
        return canvas

    def wrap_card(self, title_text, widget):
        card = Card()
        layout = QVBoxLayout(card)

        title = QLabel(title_text)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #9EE9FF;")

        layout.addWidget(title)
        layout.addWidget(widget)
        return card

    def plot_accuracy(self):
        epochs = list(range(1, 51))
        train_acc = [0.54,0.94,0.96,0.97,0.98] + [0.99]*45
        val_acc = [0.94,0.95,0.96,0.97,0.98] + [0.99]*45

        ax = self.acc_canvas.figure.add_subplot(111)
        ax.set_facecolor("#0F1E33")
        ax.plot(epochs, train_acc)
        ax.plot(epochs, val_acc)
        ax.set_title("Accuracy", color="white")
        ax.tick_params(colors='white')
        ax.spines[:].set_color("white")
        self.acc_canvas.draw()

    def plot_loss(self):
        epochs = list(range(1, 51))
        train_loss = [1.0,0.17,0.10,0.08,0.07] + [0.02]*45
        val_loss = [0.20,0.11,0.09,0.08,0.06] + [0.02]*45

        ax = self.loss_canvas.figure.add_subplot(111)
        ax.set_facecolor("#0F1E33")
        ax.plot(epochs, train_loss)
        ax.plot(epochs, val_loss)
        ax.set_title("Loss", color="white")
        ax.tick_params(colors='white')
        ax.spines[:].set_color("white")
        self.loss_canvas.draw()

    # ================= PDF EXPORT =================
    def export_pdf(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "NeuroGrade_Model_Report.pdf")

        doc = SimpleDocTemplate(file_path)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("NeuroGrade Model Report", styles["Heading1"]))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph("Validation Accuracy: 99.62%", styles["Normal"]))
        elements.append(Paragraph("Test Accuracy: 99.50%", styles["Normal"]))
        doc.build(elements)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ModelDetailsPage()
    window.show()
    sys.exit(app.exec_())
