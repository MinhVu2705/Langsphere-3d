# utils/file_utils.py
import shutil
import os
from tkinter import Tk, filedialog

def pick_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def save_uploaded_file(src_path, dest_dir="uploads"):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, filename)
    shutil.copy(src_path, dest_path)
    return dest_path
