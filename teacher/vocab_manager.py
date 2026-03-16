# teacher/vocab_manager.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
import os
from utils.database import load_db, save_db

DATA_DIR = os.path.join(os.path.dirname(__file__), "../database")

class VocabManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = os.path.join(DATA_DIR, "vocab_db.json")
        self.setStyleSheet("font-size: 15px;")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Danh sách từ
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(240)
        self.list_widget.itemClicked.connect(self.load_selected_vocab)
        layout.addWidget(self.list_widget)

        # Form bên phải
        form = QVBoxLayout()

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Từ vựng...")

        self.meaning_input = QLineEdit()
        self.meaning_input.setPlaceholderText("Nghĩa...")

        self.example_edit = QTextEdit()
        self.example_edit.setPlaceholderText("Ví dụ minh hoạ...")

        form.addWidget(QLabel("🔤 Từ vựng:"))
        form.addWidget(self.word_input)
        form.addWidget(QLabel("💡 Nghĩa:"))
        form.addWidget(self.meaning_input)
        form.addWidget(QLabel("✏️ Ví dụ:"))
        form.addWidget(self.example_edit)

        # Buttons
        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("💾 Lưu")
        self.add_btn = QPushButton("➕ Thêm mới")
        self.delete_btn = QPushButton("🗑️ Xoá")

        self.save_btn.clicked.connect(self.save_vocab)
        self.add_btn.clicked.connect(self.add_new_vocab)
        self.delete_btn.clicked.connect(self.delete_selected_vocab)

        for btn in [self.save_btn, self.add_btn, self.delete_btn]:
            btn.setStyleSheet("padding: 6px; font-weight: bold;")
            btn_row.addWidget(btn)

        form.addLayout(btn_row)
        layout.addLayout(form)
        self.setLayout(layout)

        self.load_vocab_list()

    def load_vocab_list(self):
        try:
            self.vocab_data = load_db(self.db_path)
        except:
            self.vocab_data = []

        self.list_widget.clear()
        for idx, entry in enumerate(self.vocab_data):
            self.list_widget.addItem(f"{idx+1}. {entry.get('word', '???')}")
        self.list_widget.addItem("➕ Thêm từ mới")

    def load_selected_vocab(self):
        index = self.list_widget.currentRow()
        if index == len(self.vocab_data):
            self.add_new_vocab()
            return
        entry = self.vocab_data[index]
        self.word_input.setText(entry.get("word", ""))
        self.meaning_input.setText(entry.get("meaning", ""))
        self.example_edit.setPlainText(entry.get("example", ""))

    def save_vocab(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.vocab_data):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn từ vựng để lưu.")
            return
        self.vocab_data[index] = {
            "word": self.word_input.text().strip(),
            "meaning": self.meaning_input.text().strip(),
            "example": self.example_edit.toPlainText().strip()
        }
        save_db(self.db_path, self.vocab_data)
        self.load_vocab_list()
        self.list_widget.setCurrentRow(index)
        QMessageBox.information(self, "Đã lưu", "✅ Từ vựng đã được cập nhật!")

    def add_new_vocab(self):
        new = {"word": "New word", "meaning": "", "example": ""}
        self.vocab_data.append(new)
        save_db(self.db_path, self.vocab_data)
        self.load_vocab_list()
        self.list_widget.setCurrentRow(len(self.vocab_data) - 1)
        QMessageBox.information(self, "Đã thêm", "🎉 Đã thêm từ mới.")

    def delete_selected_vocab(self):
        index = self.list_widget.currentRow()
        if index < 0 or index >= len(self.vocab_data):
            return
        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xoá từ này?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.vocab_data[index]
            save_db(self.db_path, self.vocab_data)
            self.load_vocab_list()
            self.word_input.clear()
            self.meaning_input.clear()
            self.example_edit.clear()
