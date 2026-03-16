# teacher/assign_homework.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox,
    QTextEdit, QPushButton, QDateEdit, QMessageBox
)
from PyQt5.QtCore import QDate
from utils.database import load_db, save_db
import os
import datetime

# Đảm bảo đường dẫn tương đối đến thư mục database
DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class AssignHomeworkWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📤 Giao bài tập cho học sinh")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Chọn học sinh
        try:
            user_data = load_db(os.path.join(DATA_DIR, "user_db.json"))
        except:
            user_data = []

        self.student_list = [u for u in user_data if u.get("role") == "student"]
        self.student_combo = QComboBox()
        self.student_combo.addItems([f"{u.get('fullname', u['username'])} ({u['username']})" for u in self.student_list])
        layout.addWidget(QLabel("👤 Chọn học sinh:"))
        layout.addWidget(self.student_combo)

        # Loại bài tập
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Writing", "File", "Speaking", "Image"])
        layout.addWidget(QLabel("📂 Loại bài tập:"))
        layout.addWidget(self.type_combo)

        # Nội dung bài
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Nhập hướng dẫn hoặc nội dung bài tập...")
        layout.addWidget(QLabel("📝 Nội dung bài:"))
        layout.addWidget(self.content_edit)

        # Hạn nộp
        self.deadline_picker = QDateEdit()
        self.deadline_picker.setCalendarPopup(True)
        self.deadline_picker.setDate(QDate.currentDate().addDays(3))
        layout.addWidget(QLabel("📅 Hạn nộp bài:"))
        layout.addWidget(self.deadline_picker)

        # Nút giao bài
        submit_btn = QPushButton("Giao bài")
        submit_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-size: 16px;")
        submit_btn.clicked.connect(self.assign_homework)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def assign_homework(self):
        student_index = self.student_combo.currentIndex()
        if student_index < 0 or student_index >= len(self.student_list):
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy học sinh được chọn.")
            return

        student = self.student_list[student_index]
        username = student["username"]
        hw_type = self.type_combo.currentText()
        content = self.content_edit.toPlainText().strip()
        deadline = self.deadline_picker.date().toString("yyyy-MM-dd")

        if not content:
            QMessageBox.warning(self, "Thiếu nội dung", "Bạn chưa nhập nội dung bài tập!")
            return

        try:
            data = load_db(os.path.join(DATA_DIR, "homework_db.json"))
        except:
            data = []

        new_entry = {
            "homework_id": f"hw_{len(data)+1:03}",
            "username": username,
            "type": hw_type.lower(),
            "content": content,
            "deadline": deadline,
            "status": "assigned",
            "assign_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(new_entry)
        save_db(os.path.join(DATA_DIR, "homework_db.json"), data)

        QMessageBox.information(self, "Thành công", "🎉 Bài tập đã được giao!")
        self.content_edit.clear()

