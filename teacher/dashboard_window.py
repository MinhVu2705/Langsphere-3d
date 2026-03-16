# teacher/dashboard_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QApplication, QStackedLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class TeacherDashboardWindow(QWidget):
    def __init__(self, fullname="Teacher"):
        super().__init__()
        self.fullname = fullname
        self.setWindowTitle("👩‍🏫 LangSphere 3D - Teacher Dashboard")
        self.showMaximized()
        self.setStyleSheet("background-color: #f0f4f8;")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== SIDEBAR MENU =====
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #2c3e50;")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        user_label = QLabel(f"👩‍🏫 {self.fullname}")
        user_label.setStyleSheet("font-size: 20px; color: white; font-weight: bold;")
        sidebar_layout.addWidget(user_label)

        self.menu_buttons = {}
        menu_items = {
            "Giao bài tập": self.open_assign_homework,
            "Chấm điểm": self.open_score_review,
            "Ngữ pháp": self.open_grammar_manager,
            "Từ vựng": self.open_vocab_manager,
            "Speaking": self.open_speaking_manager,
            "Reading": self.open_reading_manager,
            "Quiz": self.open_quiz_manager,
            "Hồ sơ": self.open_profile,
            "Đăng xuất": self.logout
        }

        for label, func in menu_items.items():
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: white;
                    font-size: 15px;
                    padding: 10px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #3d5a73;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(func)
            sidebar_layout.addWidget(btn)
            self.menu_buttons[label] = btn

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # ===== MAIN CONTENT =====
        self.content_area = QStackedLayout()
        self.placeholder = QLabel("📊 Chào mừng bạn đến với hệ thống quản lý giáo viên LangSphere 3D.\nChọn một mục bên trái để bắt đầu.")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setFont(QFont("Segoe UI", 20))
        self.content_area.addWidget(self.placeholder)

        content_frame = QFrame()
        content_frame.setLayout(self.content_area)
        main_layout.addWidget(content_frame)

    # ===== MENU FUNCTION PLACEHOLDERS =====
    def open_assign_homework(self):
        from teacher.assign_homework import AssignHomeworkWidget
        widget = AssignHomeworkWidget()
        self.show_widget(widget)
        self.show_message("📤 Module: Giao bài tập (assign_homework.py)")

    def open_grammar_manager(self):
        from teacher.grammar_manager import GrammarManagerWidget
        widget = GrammarManagerWidget()
        self.show_widget(widget)
        self.show_message("📘 Module: Ngữ pháp")

    def open_vocab_manager(self):
        from teacher.vocab_manager import VocabManagerWidget
        widget = VocabManagerWidget()
        self.show_widget(widget)
        self.show_message("🧠 Module: Từ vựng")

    def open_speaking_manager(self):
        from teacher.speaking_manager import SpeakingManagerWidget
        widget = SpeakingManagerWidget()
        self.show_widget(widget)
        self.show_message("🎤 Module: Speaking")

    def open_reading_manager(self):
        from teacher.reading_manager import ReadingManagerWidget
        widget = ReadingManagerWidget()
        self.show_widget(widget)
        self.show_message("📚 Module: Reading")

    def open_quiz_manager(self):
        from teacher.quiz_manager import QuizManagerWidget
        widget = QuizManagerWidget()
        self.show_widget(widget)
        self.show_message("📝 Module: Quiz")

    def open_profile(self):
       from teacher.profile import TeacherProfileWidget
       self.show_widget(TeacherProfileWidget(self.fullname))
       self.show_message("👤 Hồ sơ cá nhân")

    def logout(self):
        print("👋 Đăng xuất giáo viên")
        self.close()

    def show_message(self, text):
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 18))
        lbl.setAlignment(Qt.AlignCenter)
        # Xóa tất cả widgets cũ và thêm mới
        while self.content_area.count():
            widget = self.content_area.widget(0)
            self.content_area.removeWidget(widget)
            widget.deleteLater()
        self.content_area.addWidget(lbl)
        self.content_area.setCurrentWidget(lbl)

    def show_widget(self, widget):
        while self.content_area.count():
            old = self.content_area.widget(0)
            self.content_area.removeWidget(old)
            old.deleteLater()
        self.content_area.addWidget(widget)
        self.content_area.setCurrentWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TeacherDashboardWindow("Cô Mai Hương")
    win.show()
    sys.exit(app.exec_())
