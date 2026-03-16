# langsphere3d/utils/database.py

import json
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'user_db.json')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def check_login(username, password):
    """Trả về user dict nếu login thành công, None nếu fail."""
    users = load_users()
    password_hashed = hash_password(password)
    for user in users:
        if user['username'] == username and user['password'] == password_hashed:
            return user  # trả nguyên user dict
    return None

def username_exists(username):
    users = load_users()
    return any(u['username'] == username for u in users)

def email_exists(email):
    users = load_users()
    return any(u['email'] == email for u in users)

def add_user(user_data):
    users = load_users()
    users.append(user_data)
    save_users(users)
import json
def load_db(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
def save_db(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)