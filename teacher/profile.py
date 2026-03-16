# teacher/profile.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from utils.database import load_db
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class TeacherProfileWidget(QWidget):
    def __init__(self, username="anonymous"):
        super().__init__()
        self.username = username
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        try:
            users = load_db(os.path.join(DATA_DIR, "user_db.json"))
            user = next((u for u in users if u["username"] == self.username), None)
        except:
            user = None

        if not user:
            label = QLabel("Không tìm thấy thông tin giáo viên.")
            label.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(label)
            self.setLayout(layout)
            return

        fullname = user.get("fullname", self.username)
        email = user.get("email", "-")
        role = user.get("role", "teacher").capitalize()

        # Hiển thị thông tin cơ bản
        layout.addWidget(self.make_line(f"👩‍🏫 Họ tên: {fullname}"))
        layout.addWidget(self.make_line(f"📧 Email: {email}"))
        layout.addWidget(self.make_line(f"👤 Username: {self.username}"))
        layout.addWidget(self.make_line(f"🔐 Vai trò: {role}"))

        # Thống kê bài tập đã giao (nếu có homework_db)
        try:
            homeworks = load_db(os.path.join(DATA_DIR, "homework_db.json"))
            assigned_count = sum(1 for h in homeworks if h["status"] == "assigned")
        except:
            assigned_count = 0

        layout.addSpacing(20)
        layout.addWidget(QLabel("📊 Thống kê:"))
        layout.addWidget(self.make_line(f"📎 Bài tập đã giao: {assigned_count}"))

        layout.addStretch()
        self.setLayout(layout)

    def make_line(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-size: 15px; padding: 6px;")
        return label
