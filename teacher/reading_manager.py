# teacher/reading_manager.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
import os
from utils.database import load_db, save_db

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class ReadingManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = os.path.join(DATA_DIR, "reading_db.json")
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # LEFT: Danh sách bài đọc
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(250)
        self.list_widget.itemClicked.connect(self.load_selected_reading)
        layout.addWidget(self.list_widget)

        # RIGHT: Form chỉnh sửa bài đọc
        form = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Tiêu đề bài đọc...")

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Nhập nội dung bài đọc tại đây...")

        form.addWidget(QLabel("📘 Tiêu đề:"))
        form.addWidget(self.title_input)
        form.addWidget(QLabel("📖 Nội dung:"))
        form.addWidget(self.content_edit)

        # Buttons
        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("💾 Lưu")
        self.add_btn = QPushButton("➕ Thêm mới")
        self.delete_btn = QPushButton("🗑️ Xóa")

        self.save_btn.clicked.connect(self.save_reading)
        self.add_btn.clicked.connect(self.add_new_reading)
        self.delete_btn.clicked.connect(self.delete_selected_reading)

        for btn in [self.save_btn, self.add_btn, self.delete_btn]:
            btn.setStyleSheet("padding: 6px; font-weight: bold;")
            btn_row.addWidget(btn)

        form.addLayout(btn_row)
        layout.addLayout(form)
        self.setLayout(layout)

        self.load_reading_list()

    def load_reading_list(self):
        try:
            self.reading_data = load_db(self.db_path)
        except:
            self.reading_data = []

        self.list_widget.clear()
        for idx, r in enumerate(self.reading_data):
            self.list_widget.addItem(f"{idx+1}. {r.get('title', 'Không tiêu đề')}")
        self.list_widget.addItem("➕ Thêm bài đọc mới")

    def load_selected_reading(self):
        index = self.list_widget.currentRow()
        if index == len(self.reading_data):
            self.add_new_reading()
            return

        reading = self.reading_data[index]
        self.title_input.setText(reading.get("title", ""))
        self.content_edit.setPlainText(reading.get("content", ""))

    def save_reading(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.reading_data):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn bài đọc để lưu.")
            return

        self.reading_data[index] = {
            "title": self.title_input.text().strip(),
            "content": self.content_edit.toPlainText().strip()
        }
        save_db(self.db_path, self.reading_data)
        self.load_reading_list()
        self.list_widget.setCurrentRow(index)
        QMessageBox.information(self, "Đã lưu", "✅ Bài đọc đã được cập nhật.")

    def add_new_reading(self):
        new = {"title": "New Reading", "content": ""}
        self.reading_data.append(new)
        save_db(self.db_path, self.reading_data)
        self.load_reading_list()
        self.list_widget.setCurrentRow(len(self.reading_data) - 1)
        QMessageBox.information(self, "Đã thêm", "🎉 Đã thêm bài đọc mới.")

    def delete_selected_reading(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.reading_data):
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn muốn xóa bài đọc này?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.reading_data[index]
            save_db(self.db_path, self.reading_data)
            self.load_reading_list()
            self.title_input.clear()
            self.content_edit.clear()
