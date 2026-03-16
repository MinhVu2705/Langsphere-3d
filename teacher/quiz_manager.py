# teacher/quiz_manager.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QTextEdit, QLineEdit, QPushButton,
    QMessageBox, QComboBox
)
import os
from utils.database import load_db, save_db

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class QuizManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 14px;")
        self.db_path = os.path.join(DATA_DIR, "quiz_db.json")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # ==== LEFT: Danh sách câu hỏi ====
        self.quiz_list = QListWidget()
        self.quiz_list.setMinimumWidth(250)
        self.quiz_list.itemClicked.connect(self.load_selected_question)
        layout.addWidget(self.quiz_list)

        # ==== RIGHT: Biểu mẫu chỉnh sửa ====
        form = QVBoxLayout()

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Chủ đề (Topic)...")

        self.level_input = QComboBox()
        self.level_input.addItems(["A1", "A2", "B1", "B2", "C1"])

        self.question_edit = QTextEdit()
        self.question_edit.setPlaceholderText("Nhập câu hỏi...")

        self.options_inputs = [QLineEdit() for _ in range(4)]
        for i, opt in enumerate(self.options_inputs):
            opt.setPlaceholderText(f"Đáp án {i+1}")

        self.answer_combo = QComboBox()
        self.answer_combo.addItems(["Đáp án 1", "Đáp án 2", "Đáp án 3", "Đáp án 4"])

        form.addWidget(QLabel("📌 Chủ đề:"))
        form.addWidget(self.topic_input)
        form.addWidget(QLabel("🎯 Trình độ:"))
        form.addWidget(self.level_input)
        form.addWidget(QLabel("❓ Câu hỏi:"))
        form.addWidget(self.question_edit)
        form.addWidget(QLabel("💡 Đáp án:"))
        for opt in self.options_inputs:
            form.addWidget(opt)
        form.addWidget(QLabel("✅ Đáp án đúng:"))
        form.addWidget(self.answer_combo)

        # ==== Buttons ====
        btn_row = QHBoxLayout()
        self.btn_save = QPushButton("💾 Lưu")
        self.btn_add = QPushButton("➕ Thêm mới")
        self.btn_delete = QPushButton("🗑️ Xóa")

        self.btn_save.clicked.connect(self.save_question)
        self.btn_add.clicked.connect(self.add_new_question)
        self.btn_delete.clicked.connect(self.delete_selected_question)

        for btn in [self.btn_save, self.btn_add, self.btn_delete]:
            btn.setStyleSheet("padding: 6px; font-weight: bold;")
            btn_row.addWidget(btn)

        form.addLayout(btn_row)
        layout.addLayout(form)

        self.setLayout(layout)
        self.load_quiz_list()

    def load_quiz_list(self):
        try:
            self.quiz_data = load_db(self.db_path)
        except:
            self.quiz_data = []

        self.quiz_list.clear()
        for idx, quiz in enumerate(self.quiz_data):
            topic = quiz.get("topic", "No topic")
            q = quiz.get("question", "Câu hỏi...")
            self.quiz_list.addItem(f"{idx+1}. [{topic}] {q[:40]}...")
        self.quiz_list.addItem("➕ Thêm câu hỏi mới")

    def load_selected_question(self):
        index = self.quiz_list.currentRow()
        if index == len(self.quiz_data):
            self.add_new_question()
            return
        quiz = self.quiz_data[index]
        self.topic_input.setText(quiz.get("topic", ""))
        self.level_input.setCurrentText(quiz.get("level", "A1"))
        self.question_edit.setText(quiz.get("question", ""))
        for i in range(4):
            self.options_inputs[i].setText(quiz.get("options", [""]*4)[i])
        self.answer_combo.setCurrentIndex(quiz.get("answer", 0))

    def save_question(self):
        index = self.quiz_list.currentRow()
        if index < 0 or index >= len(self.quiz_data):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một câu hỏi để lưu.")
            return
        new_data = {
            "type": "grammar",
            "topic": self.topic_input.text().strip(),
            "level": self.level_input.currentText(),
            "question": self.question_edit.toPlainText().strip(),
            "options": [opt.text().strip() for opt in self.options_inputs],
            "answer": self.answer_combo.currentIndex()
        }
        self.quiz_data[index] = new_data
        save_db(self.db_path, self.quiz_data)
        self.load_quiz_list()
        self.quiz_list.setCurrentRow(index)
        QMessageBox.information(self, "Đã lưu", "✅ Câu hỏi đã được cập nhật!")

    def add_new_question(self):
        new = {
            "type": "grammar",
            "topic": "New Topic",
            "level": "A1",
            "question": "",
            "options": ["", "", "", ""],
            "answer": 0
        }
        self.quiz_data.append(new)
        save_db(self.db_path, self.quiz_data)
        self.load_quiz_list()
        self.quiz_list.setCurrentRow(len(self.quiz_data) - 1)
        QMessageBox.information(self, "Thành công", "🎉 Đã thêm câu hỏi mới.")

    def delete_selected_question(self):
        index = self.quiz_list.currentRow()
        if index < 0 or index >= len(self.quiz_data):
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn muốn xóa câu hỏi này?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.quiz_data[index]
            save_db(self.db_path, self.quiz_data)
            self.load_quiz_list()
            for field in [self.topic_input, self.question_edit] + self.options_inputs:
                field.clear()
    