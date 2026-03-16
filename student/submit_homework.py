from utils.database import load_db, save_db
from utils.file_utils import pick_file, save_uploaded_file
import datetime
import os

def run_submit_homework(scene, username="anonymous"):
    scene.board_writer.write_on_board("Submit Homework\nChọn loại bài tập và nộp bài!", speak=False)
    from direct.gui.DirectGui import DirectEntry, DirectButton, DirectLabel

    # Label hướng dẫn
    DirectLabel(
        text="Loại bài:",
        scale=0.055,
        pos=(0.66, 0, -0.47),
        frameColor=(0,0,0,0),
        text_fg=(1,1,1,1)
    )

    # Loại bài (writing/file/audio/image)
    hw_types = ["Writing", "File Upload", "Speaking (Record)", "Image Upload"]
    current_type = {"value": hw_types[0]}

    def set_type(i):
        current_type["value"] = hw_types[i]
        update_ui()

    # Tạo nút chọn loại bài
    btns_type = []
    for idx, name in enumerate(hw_types):
        btn = DirectButton(
            text=name,
            scale=0.054,
            pos=(0.95 + idx*0.19, 0, -0.47),
            frameColor=(0.12,0.14,0.18,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda i=idx: set_type(i)
        )
        btns_type.append(btn)

    # Dynamic: ô nhập bài, nút upload, nút ghi âm...
    widgets = []

    def clear_widgets():
        for w in widgets:
            try: w.destroy()
            except: pass
        widgets.clear()

    def update_ui():
        clear_widgets()
        t = current_type["value"]
        if t == "Writing":
            entry = DirectEntry(
                scale=0.065,
                pos=(0.7, 0, -0.6),
                width=35,
                numLines=4,
                focus=1,
                frameColor=(0.22,0.28,0.23,1),
                initialText='Nhập bài viết ở đây...',
                text_fg=(1,1,1,1)
            )
            widgets.append(entry)
            widgets.append(make_submit_btn(lambda: submit_text(entry.get())))
        elif t == "File Upload":
            lbl = DirectLabel(
                text="Chọn file bất kỳ để upload (PDF, Word, ảnh, ...)",
                scale=0.054,
                pos=(0.85, 0, -0.62),
                frameColor=(0,0,0,0),
                text_fg=(1,1,1,1)
            )
            widgets.append(lbl)
            widgets.append(make_submit_btn(submit_file))
        elif t == "Speaking (Record)":
            widgets.append(make_record_btn(submit_audio))
        elif t == "Image Upload":
            lbl = DirectLabel(
                text="Chọn ảnh để upload (JPG, PNG, ...)",
                scale=0.054,
                pos=(0.8, 0, -0.62),
                frameColor=(0,0,0,0),
                text_fg=(1,1,1,1)
            )
            widgets.append(lbl)
            widgets.append(make_submit_btn(submit_image))

    def make_submit_btn(submit_func):
        return DirectButton(
            text="Nộp bài",
            scale=0.07,
            pos=(1.18, 0, -0.85),
            frameColor=(0.18,0.25,0.14,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=submit_func,
        )

    def make_record_btn(callback):
        return DirectButton(
            text="Ghi âm & Nộp bài nói",
            scale=0.07,
            pos=(1.18, 0, -0.85),
            frameColor=(0.18,0.10,0.25,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=callback,
        )

    def submit_text(content):
        content = content.strip()
        if not content:
            scene.board_writer.write_on_board("Bạn chưa nhập nội dung!", speak=False)
            return
        append_homework({
            "type": "writing",
            "content": content
        })
        update_ui()
        show_history()

    def submit_file():
        file_path = pick_file()
        if not file_path:
            scene.board_writer.write_on_board("Bạn chưa chọn file nào!", speak=False)
            return
        saved_path = save_uploaded_file(file_path)
        append_homework({
            "type": "file",
            "content": f"File: {os.path.basename(saved_path)}",
            "file_path": saved_path
        })
        update_ui()
        show_history()

    def submit_image():
        file_path = pick_file()
        if not file_path:
            scene.board_writer.write_on_board("Bạn chưa chọn ảnh nào!", speak=False)
            return
        saved_path = save_uploaded_file(file_path)
        append_homework({
            "type": "image",
            "content": f"Image: {os.path.basename(saved_path)}",
            "file_path": saved_path
        })
        update_ui()
        show_history()

    def submit_audio():
        # Ghi âm audio, lưu file, upload như file thường
        import sounddevice as sd
        import scipy.io.wavfile as wav
        import tempfile
        samplerate = 16000
        duration = 6
        scene.board_writer.write_on_board("Đang ghi âm... Hãy nói vào micro!", speak=False)
        try:
            recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()
            temp_path = tempfile.mktemp(suffix='.wav')
            wav.write(temp_path, samplerate, recording)
            saved_path = save_uploaded_file(temp_path)
            append_homework({
                "type": "audio",
                "content": f"Audio: {os.path.basename(saved_path)}",
                "file_path": saved_path
            })
            update_ui()
            show_history()
        except Exception as e:
            scene.board_writer.write_on_board(f"Lỗi ghi âm: {e}", speak=False)

    def append_homework(entry_data):
        hw_data = load_db("homework_db.json")
        new_hw = {
            "username": username,
            "homework_id": f"hw_{len(hw_data)+1:03d}",
            "status": "submitted",
            "submit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **entry_data
        }
        hw_data.append(new_hw)
        save_db("homework_db.json", hw_data)
        scene.board_writer.write_on_board("Nộp bài thành công! 🎉", speak=False)

    def show_history():
        hw_data = [h for h in load_db("homework_db.json") if h["username"] == username]
        if not hw_data:
            scene.board_writer.write_on_board("Chưa có bài nào đã nộp.", speak=False)
            return
        last = hw_data[-1]
        text = f"Lần nộp gần nhất:\n- {last['type'].capitalize()} | {last['status']} | {last['submit_time']}\n{last['content']}"
        scene.board_writer.write_on_board(text, speak=False)

    update_ui()
