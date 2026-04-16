# prediction_page.py

import pymysql
import matplotlib
matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QSizePolicy,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# ------------------ THEME (EYE FRIENDLY) ------------------
DARK_BG = "#0B1220"
CARD_BG = "#111B2E"
TEXT_COLOR = "#E6F1FF"
ACCENT = "#38BDF8"
BAR_COLOR = "#60A5FA"


class PredictionWindow(QWidget):
    def __init__(self, predicted_grade, student_data):
        super().__init__()
        self.predicted_grade = predicted_grade
        self.student_data = student_data

        self.setWindowTitle("Predicted Final Grade & Insights")
        self.setMinimumSize(1200, 800)
        self.initUI()

    # ------------------ UI ------------------
    def initUI(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 900)
        gradient.setColorAt(0, QColor("#020617"))
        gradient.setColorAt(1, QColor(DARK_BG))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- HEADER ----------------
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #152D45;")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        title_label = QLabel("NeuroGrade")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #9EE9FF;")

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(140)
        home_btn.setFixedHeight(42)
        home_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        home_btn.setCursor(Qt.PointingHandCursor)
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E3A5F;
                color: #8FD3FF;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #254D78;
                color: #00D1FF;
            }
        """)

        home_btn.clicked.connect(self.goHome)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(home_btn)

        main_layout.addWidget(header)

        # ---------------- CONTENT ----------------
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)

        # Title
        title = QLabel(f"Predicted Final Grade: {self.predicted_grade}")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet(f"color:{ACCENT};")
        content_layout.addWidget(title)

        header_lbl = QLabel("Personalized Insights")
        header_lbl.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_lbl.setStyleSheet(f"color:{TEXT_COLOR};")
        content_layout.addWidget(header_lbl)

        suggestions = QLabel(self.generate_suggestions())
        suggestions.setFont(QFont("Segoe UI", 14))
        suggestions.setWordWrap(True)
        suggestions.setStyleSheet(f"""
            QLabel {{
                background-color: {CARD_BG};
                color: {TEXT_COLOR};
                padding: 18px;
                border-radius: 12px;
                line-height: 1.6;
            }}
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(suggestions)
        scroll.setFixedHeight(180)
        scroll.setStyleSheet("border:none;")
        content_layout.addWidget(scroll)

        # ------------------ GRAPHS ------------------
        graph_layout = QHBoxLayout()
        graph_layout.setSpacing(25)

        self.figures = [
            self.plot_metric("attendance", "Attendance (%)"),
            self.plot_metric("exam_score", "Exam Score"),
            self.plot_metric("study_hours", "Study Hours"),
        ]

        for fig in self.figures:
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            graph_layout.addWidget(canvas)

        content_layout.addLayout(graph_layout)

        btn = QPushButton("Download Charts")
        btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: #020617;
                padding: 10px 24px;
                border-radius: 8px;
            }}
        """)
        btn.clicked.connect(self.download_charts)
        content_layout.addWidget(btn, alignment=Qt.AlignRight)

        main_layout.addWidget(content_widget)

        # ---------------- FOOTER ----------------
        footer = QLabel("© 2026 NeuroGrade. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFixedHeight(40)
        footer.setStyleSheet(
            "background-color: #152D45; color: #9EE9FF; font-size: 14px;"
        )

        main_layout.addWidget(footer)

        self.showMaximized()

    # ---------------- HOME NAVIGATION ----------------
    def goHome(self):
        from UI.home import MainWindow
        self.home = MainWindow()
        self.home.showMaximized()
        self.close()

    # ------------------ DATABASE ------------------
    def connect_db(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="studentdetails"
        )

    def fetch_all_students(self):
        conn = self.connect_db()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM student_performance")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    # ------------------ SUGGESTIONS ------------------
    def generate_suggestions(self):
        data = self.fetch_all_students()

        same_grade = [
            d for d in data
            if d["Predicted_Grade"] == self.predicted_grade
        ] or data

        metrics = [
            ("attendance", "Attendance (%)"),
            ("exam_score", "Exam Score"),
            ("study_hours", "Study Hours"),
        ]

        lines = []
        for key, label in metrics:
            avg = sum(d[key] for d in same_grade) / len(same_grade)
            current = self.student_data.get(key, 0)

            if current < avg:
                lines.append(f"• {label}: Needs improvement (Avg: {avg:.1f})")
            else:
                lines.append(f"• {label}: Performing well (Avg: {avg:.1f})")

        return "\n".join(lines)

    # ------------------ GRAPH STYLING ------------------
    def style_ax(self, fig, ax, title, ylabel):
        fig.patch.set_facecolor(DARK_BG)
        ax.set_facecolor(DARK_BG)
        ax.set_title(title, color=TEXT_COLOR, fontsize=14, pad=10)
        ax.set_ylabel(ylabel, color=TEXT_COLOR)
        ax.tick_params(colors=TEXT_COLOR, labelsize=11)
        ax.grid(axis="y", alpha=0.25)
        for spine in ax.spines.values():
            spine.set_visible(False)

    # ------------------ VISUALIZATION ------------------
    def plot_metric(self, metric, label):
        data = self.fetch_all_students()
        grades = sorted(set(d["Predicted_Grade"] for d in data))

        averages = []
        for g in grades:
            vals = [d[metric] for d in data if d["Predicted_Grade"] == g]
            averages.append(sum(vals) / len(vals))

        fig, ax = plt.subplots(figsize=(4.5, 6))
        self.style_ax(fig, ax, f"{label} by Grade", label)

        ax.bar(grades, averages, color=BAR_COLOR, width=0.6)

        ax.scatter(
            [self.predicted_grade],
            [self.student_data.get(metric, 0)],
            color="red",
            s=140,
            zorder=5,
            label="You"
        )

        ax.legend(facecolor=DARK_BG, edgecolor="none", labelcolor=TEXT_COLOR)
        fig.tight_layout()
        return fig

    # ------------------ DOWNLOAD ------------------
    def download_charts(self):
        for i, fig in enumerate(self.figures):
            fig.savefig(f"chart_{i+1}.png", dpi=300, bbox_inches="tight")
        QMessageBox.information(self, "Saved", "Charts downloaded successfully.")
