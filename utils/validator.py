# validator.py
import re

def is_valid_email(email: str) -> bool:
    """Check email hợp lệ (cơ bản)."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    return bool(re.match(pattern, email))

def is_valid_username(username: str) -> bool:
    """
    Chỉ cho phép chữ, số, _ (gạch dưới), dài từ 4-20 ký tự.
    """
    pattern = r"^[A-Za-z0-9_]{4,20}$"
    return bool(re.match(pattern, username))

def is_strong_password(password: str) -> bool:
    """
    Kiểm tra password mạnh: ít nhất 8 ký tự,
    có chữ hoa, chữ thường, số, ký tự đặc biệt.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def is_not_empty(*fields) -> bool:
    """Check tất cả trường đều không rỗng."""
    return all(f and str(f).strip() for f in fields)

def passwords_match(p1: str, p2: str) -> bool:
    """So khớp 2 mật khẩu (case sensitive)."""
    return p1 == p2

def is_valid_fullname(fullname: str) -> bool:
    """Check tên hợp lệ (ít nhất 2 từ, không số, không ký tự lạ)."""
    # Có thể tùy chỉnh theo nhu cầu thực tế
    return bool(re.match(r"^[A-Za-zÀ-ỹà-ỹ\s'-]{4,50}$", fullname.strip()))

def is_valid_class_name(classname: str) -> bool:
    """Tên lớp học: chỉ chữ cái/số, dài hợp lý."""
    return bool(re.match(r"^[A-Za-z0-9\s_-]{3,30}$", classname.strip()))

def is_valid_phone(phone: str) -> bool:
    """Số điện thoại: chỉ số, 9-15 ký tự."""
    return bool(re.match(r"^\d{9,15}$", phone.strip()))

# Có thể bổ sung thêm validator khác tùy app mở rộng:
# - is_valid_date
# - is_valid_role
# - is_valid_badge
# v.v.

# --- Demo test trực tiếp ---
if __name__ == "__main__":
    print("Email:", is_valid_email("abc@xyz.com"))
    print("Username:", is_valid_username("user_name123"))
    print("Strong password:", is_strong_password("Password@1"))
    print("Passwords match:", passwords_match("abc", "abc"))
    print("Not empty:", is_not_empty("hi", "a", "b"))
    print("Full name:", is_valid_fullname("Nguyễn Văn A"))
    print("Class name:", is_valid_class_name("English 101"))
    print("Phone:", is_valid_phone("0987654321"))
