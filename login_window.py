from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QStackedLayout, QFrame, QMessageBox, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import json
import os
import hashlib
import re
import sys

# Đường dẫn user database
USERS_PATH = os.path.join(os.path.dirname(__file__), 'database', 'user_db.json')

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email)

def animate_button(btn):
    anim = QPropertyAnimation(btn, b"geometry")
    anim.setDuration(140)
    rect = btn.geometry()
    mid_w, mid_h = int(rect.width() * 1.2), int(rect.height() * 1.2)
    mid_x = rect.center().x() - mid_w // 2
    mid_y = rect.center().y() - mid_h // 2
    anim.setKeyValueAt(0, rect)
    anim.setKeyValueAt(0.5, rect.adjusted(
        -(mid_w-rect.width())//2, -(mid_h-rect.height())//2,
        (mid_w-rect.width())//2, (mid_h-rect.height())//2))
    anim.setKeyValueAt(1, rect)
    anim.setEasingCurve(QEasingCurve.OutBounce)
    btn._anim = anim
    anim.start()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LangSphere 3D - Đăng nhập/Đăng ký")
        self.setFixedSize(480, 520)
        self.setStyleSheet("background-color: #eaf4ff;")
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        logo = QLabel("🌐 LangSphere 3D")
        logo.setFont(QFont("Segoe UI", 24, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("color: #2c3e50;")
        self.main_layout.addWidget(logo)

        tab_layout = QHBoxLayout()
        self.login_tab = QPushButton("Login")
        self.register_tab = QPushButton("Register")
        for btn in (self.login_tab, self.register_tab):
            btn.setCheckable(True)
            btn.setMinimumHeight(36)
            btn.setStyleSheet("QPushButton { font-size: 14px; }")
        self.login_tab.setChecked(True)
        self.login_tab.clicked.connect(lambda: [self.show_login(), animate_button(self.login_tab)])
        self.register_tab.clicked.connect(lambda: [self.show_register(), animate_button(self.register_tab)])
        tab_layout.addWidget(self.login_tab)
        tab_layout.addWidget(self.register_tab)
        self.main_layout.addLayout(tab_layout)

        self.stack = QStackedLayout()
        self.login_frame = self.build_login_form()
        self.register_frame = self.build_register_form()
        self.stack.addWidget(self.login_frame)
        self.stack.addWidget(self.register_frame)
        self.main_layout.addLayout(self.stack)

        self.setLayout(self.main_layout)

    def build_login_form(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.login_role = QComboBox()
        self.login_role.addItems(["Student", "Teacher"])

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username")

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)

        self.login_error = QLabel("")
        self.login_error.setStyleSheet("color: #e74c3c; font-size: 13px;")
        self.login_error.setVisible(False)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("background-color: #1abc9c; color: white; font-size: 16px; padding: 10px; border-radius: 8px;")
        login_btn.clicked.connect(lambda: [self.login_user(), animate_button(login_btn)])

        for widget in [self.login_role, self.login_username, self.login_password, self.login_error, login_btn]:
            if widget not in [self.login_error, login_btn]:
                widget.setMinimumHeight(40)
                widget.setStyleSheet("font-size: 14px; border-radius: 6px;")
            layout.addWidget(widget)

        frame.setLayout(layout)
        return frame

    def build_register_form(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.reg_role = QComboBox()
        self.reg_role.addItems(["Student", "Teacher"])

        self.reg_fullname = QLineEdit()
        self.reg_fullname.setPlaceholderText("Full Name")

        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email")

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Username")

        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Password")
        self.reg_password.setEchoMode(QLineEdit.Password)

        self.reg_confirm = QLineEdit()
        self.reg_confirm.setPlaceholderText("Confirm Password")
        self.reg_confirm.setEchoMode(QLineEdit.Password)

        self.register_error = QLabel("")
        self.register_error.setStyleSheet("color: #e74c3c; font-size: 13px;")
        self.register_error.setVisible(False)

        register_btn = QPushButton("Register")
        register_btn.setStyleSheet("background-color: #3498db; color: white; font-size: 16px; padding: 10px; border-radius: 8px;")
        register_btn.clicked.connect(lambda: [self.register_user(), animate_button(register_btn)])

        for widget in [self.reg_role, self.reg_fullname, self.reg_email, self.reg_username,
                       self.reg_password, self.reg_confirm, self.register_error, register_btn]:
            if widget not in [self.register_error, register_btn]:
                widget.setMinimumHeight(40)
                widget.setStyleSheet("font-size: 14px; border-radius: 6px;")
            layout.addWidget(widget)

        frame.setLayout(layout)
        return frame

    def show_login(self):
        self.login_tab.setChecked(True)
        self.register_tab.setChecked(False)
        self.stack.setCurrentIndex(0)
        self.login_error.setVisible(False)

    def show_register(self):
        self.login_tab.setChecked(False)
        self.register_tab.setChecked(True)
        self.stack.setCurrentIndex(1)
        self.register_error.setVisible(False)

    def login_user(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        role = self.login_role.currentText().lower()
        self.login_error.setVisible(False)

        if not username or not password:
            self.login_error.setText("Vui lòng nhập đầy đủ thông tin!")
            self.login_error.setVisible(True)
            return

        users = load_users()
        password_hashed = hash_password(password)
        for user in users:
            if (
                user["username"] == username
                and user["password"] == password_hashed
                and user["role"].lower() == role
            ):
                print(f"Đăng nhập thành công với vai trò: {role} ({username})")
                self.close()

                if role == "student":
                    try:
                        from student.classroom_scene import StudentScene
                        StudentScene(user["fullname"]).run()
                    except Exception as e:
                        print("Lỗi khi mở Student Scene:", e)

                elif role == "teacher":
                    try:
                        from teacher.dashboard_window import TeacherDashboardWindow
                        self.teacher_win = TeacherDashboardWindow(user["fullname"])
                        self.teacher_win.show()
                    except Exception as e:
                        print("Lỗi khi mở Teacher Dashboard:", e)
                return

        self.login_error.setText("Sai tài khoản, mật khẩu hoặc vai trò!")
        self.login_error.setVisible(True)
        self.login_password.clear()

    def register_user(self):
        fullname = self.reg_fullname.text().strip()
        email = self.reg_email.text().strip()
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm = self.reg_confirm.text()
        role = self.reg_role.currentText().lower()
        self.register_error.setVisible(False)

        if not all([fullname, email, username, password, confirm]):
            self.register_error.setText("Điền đủ thông tin nhé!")
            self.register_error.setVisible(True)
            return

        if not is_valid_email(email):
            self.register_error.setText("Email không hợp lệ!")
            self.register_error.setVisible(True)
            return

        if password != confirm:
            self.register_error.setText("Mật khẩu nhập lại không khớp!")
            self.register_error.setVisible(True)
            self.reg_confirm.clear()
            return

        users = load_users()
        for user in users:
            if user["username"] == username:
                self.register_error.setText("Username đã tồn tại!")
                self.register_error.setVisible(True)
                self.reg_username.clear()
                return
            if user["email"] == email:
                self.register_error.setText("Email đã đăng ký tài khoản khác!")
                self.register_error.setVisible(True)
                self.reg_email.clear()
                return

        user_data = {
            "fullname": fullname,
            "email": email,
            "username": username,
            "password": hash_password(password),
            "role": role
        }
        users.append(user_data)
        save_users(users)

        QMessageBox.information(self, "Đăng ký thành công", "Tài khoản đã được tạo. Mời bạn đăng nhập!")
        self.show_login()

        self.reg_fullname.clear()
        self.reg_email.clear()
        self.reg_username.clear()
        self.reg_password.clear()
        self.reg_confirm.clear()

# Chạy độc lập
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
