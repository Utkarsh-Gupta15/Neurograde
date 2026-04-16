#data_entry_page.py

# data_entry_page.py
import sys
import pymysql
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator, QColor, QPalette, QLinearGradient, QBrush

from ml.predictor import predict_final_grade
from UI.prediction_page import PredictionWindow

# ------------------ MYSQL SAVE FUNCTION ------------------
def save_to_database(data, predicted_grade):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="",
            password="",
            database=""
        )
        cursor = conn.cursor()
        # Insert student details including predicted grade
        query = """
            INSERT INTO student_performance 
            (student_id, age, gender, study_hours, participation, exam_score, attendance,
             social_media_hours, sleep_hours, predicted_grade)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                age=%s, gender=%s, study_hours=%s, participation=%s,
                exam_score=%s, attendance=%s, social_media_hours=%s, sleep_hours=%s,
                predicted_grade=%s
        """
        values = (
            data.get("Student_ID"), data["Age"], data["Gender"], data["Study_Hours_per_Week"],
            data["Participation_in_Discussions"], data["Exam_Score (%)"], data["Attendance_Rate (%)"],
            data["Time_Spent_on_Social_Media (hours/week)"], data["Sleep_Hours_per_Night"], predicted_grade,
            # For update on duplicate
            data["Age"], data["Gender"], data["Study_Hours_per_Week"], data["Participation_in_Discussions"],
            data["Exam_Score (%)"], data["Attendance_Rate (%)"], data["Time_Spent_on_Social_Media (hours/week)"],
            data["Sleep_Hours_per_Night"], predicted_grade
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
    except pymysql.MySQLError as e:
        raise Exception(f"MySQL Error: {e}")

# ------------------ GUI ------------------
class StudentPerformanceUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Student Performance Prediction System")
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(1200, 800)

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0,0,0,900)
        gradient.setColorAt(0.0, QColor("#020617"))
        gradient.setColorAt(0.4, QColor("#071126"))
        gradient.setColorAt(1.0, QColor("#081423"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40,40,40,40)
        main_layout.setSpacing(30)

        header = QLabel("Student Performance Prediction")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(92)
        header.setFont(QFont("Segoe UI",26,QFont.Bold))
        header.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #071232, stop:0.5 #003B5C, stop:1 #001529);
                color: #9EE9FF;
                border-radius: 14px;
                padding: 8px;
            }
        """)
        main_layout.addWidget(header)

        self.card = QWidget()
        layout = QGridLayout(self.card)
        layout.setSpacing(28)
        layout.setContentsMargins(48,48,48,48)
        self.card.setStyleSheet("""
            QWidget {
                background-color: rgba(8,14,28,220);
                border: 1px solid rgba(120,200,255,0.10);
                border-radius: 14px;
            }
        """)
        main_layout.addWidget(self.card)

        # Input fields
        self.inputs = {}
        fields = [
            ('Student ID', 'Student_ID', QIntValidator(1,999999999),'Enter student ID'),
            ('Age', 'Age', QIntValidator(3,100),'Enter age'),
            ('Gender','Gender', None,None,['Select','Male','Female','Other']),
            ('Study Hours Per Week','Study_Hours_per_Week', QDoubleValidator(0.0,168.0,2),'Enter hours'),
            ('Participation in Discussions','Participation_in_Discussions', None,None,['Select','Yes','No']),
            ('Exam Score (%)','Exam_Score (%)', QDoubleValidator(0.0,100.0,2),'Enter score'),
            ('Attendance Rate (%)','Attendance_Rate (%)', QDoubleValidator(0.0,100.0,2),'Enter attendance'),
            ('Time on Social Media (hours/week)','Time_Spent_on_Social_Media (hours/week)', QDoubleValidator(0.0,168.0,2),'Enter hours'),
            ('Sleep Hours Per Night','Sleep_Hours_per_Night', QDoubleValidator(0.0,12.0,2),'Enter hours'),
        ]

        combo_style = """
            QComboBox {
                background-color: #061224;
                color: white;
                border: 2px solid rgba(120,200,255,0.25);
                border-radius: 8px;
                padding-left: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #081423;
                color: white;
                selection-background-color: #00AEEF;
                selection-color: black;
                border: 1px solid #00AEEF;
            }
            QComboBox::drop-down {
                width: 28px;
                border-left: 1px solid rgba(120,200,255,0.25);
            }
        """

        for row,f in enumerate(fields):
            label = QLabel(f[0])
            label.setFont(QFont("Segoe UI",16))
            label.setStyleSheet("color: #CFEFFF; font-weight: 600;")
            layout.addWidget(label,row,0)
            if f[1] in ['Gender','Participation_in_Discussions']:
                combo = QComboBox()
                combo.addItems(f[4])
                combo.setFont(QFont("Segoe UI",14))
                combo.setMinimumHeight(54)
                combo.setStyleSheet(combo_style)
                self.inputs[f[1]] = combo
                layout.addWidget(combo,row,1)
            else:
                line = QLineEdit()
                line.setValidator(f[2])
                line.setPlaceholderText(f[3])
                line.setFont(QFont("Segoe UI",14))
                line.setMinimumHeight(54)
                line.setStyleSheet("""
                    QLineEdit {
                        background-color: #061224;
                        color: white;
                        border: 2px solid rgba(120,200,255,0.25);
                        border-radius: 8px;
                        padding-left: 12px;
                    }
                """)
                self.inputs[f[1]] = line
                layout.addWidget(line,row,1)

        # Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(18)
        predict_btn = QPushButton("Predict Performance")
        predict_btn.setFont(QFont("Segoe UI",15,QFont.Bold))
        predict_btn.setMinimumHeight(56)
        predict_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #00AEEF, stop:1 #00D7FF);
                color: #02101A;
                border-radius: 10px;
            }
        """)
        predict_btn.clicked.connect(self.predict)

        clear_btn = QPushButton("Clear")
        clear_btn.setFont(QFont("Segoe UI",15))
        clear_btn.setMinimumHeight(56)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.06);
                color: #DCEFFF;
                border-radius: 10px;
            }
        """)
        clear_btn.clicked.connect(self.clear_fields)

        button_row.addWidget(predict_btn)
        button_row.addWidget(clear_btn)
        main_layout.addLayout(button_row)

    # ------------------ Prediction ------------------
    def predict(self):
        # Validate dropdowns
        for key in ['Gender', 'Participation_in_Discussions']:
            if self.inputs[key].currentText() == "Select":
                QMessageBox.warning(self, "Error", f"Select {key}")
                return

        # Validate text fields
        for key, widget in self.inputs.items():
            if key not in ['Gender', 'Participation_in_Discussions', 'Student_ID'] and not widget.text().strip():
                QMessageBox.warning(self, "Error", f"Enter {key}")
                return

        # Build dictionary FIRST
        db_data = {}
        for k, v in self.inputs.items():
            if isinstance(v, QComboBox):
                db_data[k] = v.currentText()
            else:
                text = v.text().strip()
                db_data[k] = int(text) if k in ["Age", "Student_ID"] else float(text)

        # ✅ Negative value validation (NOW it works)
        for key in [
            "Study_Hours_per_Week",
            "Exam_Score (%)",
            "Attendance_Rate (%)",
            "Time_Spent_on_Social_Media (hours/week)",
            "Sleep_Hours_per_Night"
        ]:
            if db_data[key] < 0:
                QMessageBox.warning(self, "Error", f"{key} cannot be negative.")
                return

        # Weekly hours validation
        study_hours = db_data["Study_Hours_per_Week"]
        social_hours = db_data["Time_Spent_on_Social_Media (hours/week)"]
        sleep_hours_week = db_data["Sleep_Hours_per_Night"] * 7

        if study_hours + social_hours + sleep_hours_week > 168:
            QMessageBox.warning(
                self,
                "Error",
                "Total weekly hours (study + social media + sleep) "
                "cannot exceed 168 hours."
            )
            return

        pred_data = {k: db_data[k] for k in db_data if k != "Student_ID"}

        try:
            grade = predict_final_grade(pred_data)
            if hasattr(grade, "item"):
                grade = grade.item()
            save_to_database(db_data, grade)
            self.win = PredictionWindow(grade, student_data=pred_data)
            self.win.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ------------------ Clear ------------------
    def clear_fields(self):
        for k,v in self.inputs.items():
            if isinstance(v,QComboBox):
                v.setCurrentIndex(0)
            else:
                v.clear()

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = StudentPerformanceUI()
    win.show()
    sys.exit(app.exec_())
