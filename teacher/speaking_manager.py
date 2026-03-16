# teacher/speaking_manager.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
import os
from utils.database import load_db, save_db

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class SpeakingManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = os.path.join(DATA_DIR, "speaking_db.json")
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Danh sách bài nói
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(240)
        self.list_widget.itemClicked.connect(self.load_selected_speaking)
        layout.addWidget(self.list_widget)

        # Form chỉnh sửa
        form = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Tiêu đề bài nói...")

        self.hint_input = QLineEdit()
        self.hint_input.setPlaceholderText("Gợi ý/đề bài nói...")

        self.script_edit = QTextEdit()
        self.script_edit.setPlaceholderText("Script mẫu để học viên nghe và luyện nói...")

        form.addWidget(QLabel("🎙️ Tiêu đề:"))
        form.addWidget(self.title_input)
        form.addWidget(QLabel("💡 Gợi ý/đề bài:"))
        form.addWidget(self.hint_input)
        form.addWidget(QLabel("📜 Script mẫu:"))
        form.addWidget(self.script_edit)

        # Buttons
        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("💾 Lưu")
        self.add_btn = QPushButton("➕ Thêm mới")
        self.delete_btn = QPushButton("🗑️ Xóa")

        self.save_btn.clicked.connect(self.save_speaking)
        self.add_btn.clicked.connect(self.add_new_speaking)
        self.delete_btn.clicked.connect(self.delete_selected_speaking)

        for btn in [self.save_btn, self.add_btn, self.delete_btn]:
            btn.setStyleSheet("padding: 6px; font-weight: bold;")
            btn_row.addWidget(btn)

        form.addLayout(btn_row)
        layout.addLayout(form)
        self.setLayout(layout)

        self.load_speaking_list()

    def load_speaking_list(self):
        try:
            self.speaking_data = load_db(self.db_path)
        except:
            self.speaking_data = []

        self.list_widget.clear()
        for idx, sp in enumerate(self.speaking_data):
            self.list_widget.addItem(f"{idx+1}. {sp.get('title', 'Không tiêu đề')}")
        self.list_widget.addItem("➕ Thêm bài nói mới")

    def load_selected_speaking(self):
        index = self.list_widget.currentRow()
        if index == len(self.speaking_data):
            self.add_new_speaking()
            return

        sp = self.speaking_data[index]
        self.title_input.setText(sp.get("title", ""))
        self.hint_input.setText(sp.get("hint", ""))
        self.script_edit.setPlainText(sp.get("script", ""))

    def save_speaking(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.speaking_data):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn bài nói để lưu.")
            return

        self.speaking_data[index] = {
            "title": self.title_input.text().strip(),
            "hint": self.hint_input.text().strip(),
            "script": self.script_edit.toPlainText().strip()
        }
        save_db(self.db_path, self.speaking_data)
        self.load_speaking_list()
        self.list_widget.setCurrentRow(index)
        QMessageBox.information(self, "Đã lưu", "✅ Bài nói đã được cập nhật.")

    def add_new_speaking(self):
        new = {"title": "New Speaking", "hint": "", "script": ""}
        self.speaking_data.append(new)
        save_db(self.db_path, self.speaking_data)
        self.load_speaking_list()
        self.list_widget.setCurrentRow(len(self.speaking_data) - 1)
        QMessageBox.information(self, "Đã thêm", "🎉 Đã thêm bài nói mới.")

    def delete_selected_speaking(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.speaking_data):
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn muốn xóa bài nói này?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.speaking_data[index]
            save_db(self.db_path, self.speaking_data)
            self.load_speaking_list()
            self.title_input.clear()
            self.hint_input.clear()
            self.script_edit.clear()
