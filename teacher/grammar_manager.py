# teacher/grammar_manager.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QListWidget, QPushButton, QTextEdit, QLineEdit, QMessageBox
)
import os
from utils.database import load_db, save_db

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class GrammarManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 15px;")
        self.db_path = os.path.join(DATA_DIR, "grammar_db.json")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # ===== LEFT: List of lessons =====
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(240)
        self.list_widget.itemClicked.connect(self.load_selected_lesson)
        layout.addWidget(self.list_widget)

        # ===== RIGHT: Editor =====
        right_panel = QVBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Tên bài học (thì)...")

        self.theory_edit = QTextEdit()
        self.theory_edit.setPlaceholderText("Lý thuyết chi tiết...")

        self.structure_edit = QLineEdit()
        self.structure_edit.setPlaceholderText("Ví dụ: S + Vs/es + O")

        self.example_edit = QTextEdit()
        self.example_edit.setPlaceholderText("Ví dụ minh họa...")

        right_panel.addWidget(QLabel("🧠 Tên bài học (thì):"))
        right_panel.addWidget(self.title_input)

        right_panel.addWidget(QLabel("📘 Lý thuyết:"))
        right_panel.addWidget(self.theory_edit)

        right_panel.addWidget(QLabel("📐 Cấu trúc:"))
        right_panel.addWidget(self.structure_edit)

        right_panel.addWidget(QLabel("✏️ Ví dụ:"))
        right_panel.addWidget(self.example_edit)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("💾 Lưu")
        self.add_btn = QPushButton("➕ Thêm mới")
        self.delete_btn = QPushButton("🗑️ Xóa")

        self.save_btn.clicked.connect(self.save_current_lesson)
        self.add_btn.clicked.connect(self.add_new_lesson)
        self.delete_btn.clicked.connect(self.delete_selected_lesson)

        for btn in [self.save_btn, self.add_btn, self.delete_btn]:
            btn.setStyleSheet("padding: 6px; font-weight: bold;")
            btn_row.addWidget(btn)

        right_panel.addLayout(btn_row)
        layout.addLayout(right_panel)

        self.setLayout(layout)
        self.load_grammar_list()

    def load_grammar_list(self):
        try:
            self.grammar_data = load_db(self.db_path)
        except:
            self.grammar_data = []

        self.list_widget.clear()
        for entry in self.grammar_data:
            self.list_widget.addItem(entry.get("tense", "Chưa đặt tên"))
        self.list_widget.addItem("➕ Thêm bài học mới")

    def load_selected_lesson(self):
        index = self.list_widget.currentRow()

        if self.list_widget.currentItem().text().startswith("➕"):
            self.add_new_lesson()
            return

        if 0 <= index < len(self.grammar_data):
            lesson = self.grammar_data[index]
            self.title_input.setText(lesson.get("tense", ""))
            self.theory_edit.setPlainText(lesson.get("theory", ""))
            self.structure_edit.setText(lesson.get("structure", ""))
            self.example_edit.setPlainText(lesson.get("example", ""))

    def save_current_lesson(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.grammar_data):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một bài học để lưu.")
            return
        self.grammar_data[index] = {
            "tense": self.title_input.text().strip(),
            "title": self.title_input.text().strip(),
            "theory": self.theory_edit.toPlainText().strip(),
            "structure": self.structure_edit.text().strip(),
            "example": self.example_edit.toPlainText().strip(),
        }
        save_db(self.db_path, self.grammar_data)
        self.load_grammar_list()
        self.list_widget.setCurrentRow(index)
        QMessageBox.information(self, "Đã lưu", "✅ Bài học đã được cập nhật!")

    def add_new_lesson(self):
        new_entry = {
            "tense": "New Tense",
            "title": "New Tense",
            "theory": "",
            "structure": "",
            "example": ""
        }
        self.grammar_data.append(new_entry)
        save_db(self.db_path, self.grammar_data)
        self.load_grammar_list()
        self.list_widget.setCurrentRow(len(self.grammar_data) - 1)
        QMessageBox.information(self, "Thành công", "🎉 Đã thêm bài học mới.")

    def delete_selected_lesson(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.grammar_data):
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn chắc chắn muốn xóa bài học này?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.grammar_data[index]
            save_db(self.db_path, self.grammar_data)
            self.load_grammar_list()
            self.title_input.clear()
            self.theory_edit.clear()
            self.structure_edit.clear()
            self.example_edit.clear()
