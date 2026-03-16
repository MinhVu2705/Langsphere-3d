from utils.database import load_db
from utils.tts import speak_current

import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import whisper

def run_speaking_practice(scene):
    if not hasattr(scene, "current_speaking_index"):
        scene.current_speaking_index = 0

    speaking_data = load_db('speaking_db.json')

    def show_speaking(index):
        if index >= len(speaking_data):
            scene.board_writer.write_on_board("Chúc mừng! Bạn đã hoàn thành tất cả bài Speaking.", speak=False)
            return
        entry = speaking_data[index]
        title = entry.get("title", "Speaking Practice")
        script = entry.get("script", "")
        hint = entry.get("hint", "")
        board_text = f"Speaking Practice\n{title}\n\nHint: {hint}\n\nẤn 'Nghe mẫu' để nghe AI đọc, rồi nhấn 'Ghi âm & Chấm điểm' để nói lại."
        def after_zoom():
            scene.board_writer.write_on_board(board_text, speak=False)
            make_sample_btn(script)
            make_record_btn(script, index)
        if hasattr(scene, "zoom_to_board"):
            scene.zoom_to_board(after_zoom)
        else:
            scene.camera.setPos(0, 2, 5)
            scene.camera.lookAt(0, 7.8, 3.2)
            after_zoom()

    def make_sample_btn(text):
        from direct.gui.DirectGui import DirectButton
        btn = DirectButton(
            text="Nghe mẫu",
            scale=0.07,
            pos=(0.9, 0, -0.7),
            frameColor=(0.1,0.32,0.12,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: speak_current(text),
        )
        if hasattr(scene, "sample_btn") and scene.sample_btn:
            scene.sample_btn.destroy()
        scene.sample_btn = btn

    def make_record_btn(ref_text, speaking_index):
        from direct.gui.DirectGui import DirectButton
        btn = DirectButton(
            text="Ghi âm & Chấm điểm (AI)",
            scale=0.07,
            pos=(1.1, 0, -0.85),
            frameColor=(0.28,0.12,0.22,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: record_and_check_ai(ref_text, speaking_index, btn),
        )
        if hasattr(scene, "record_btn") and scene.record_btn:
            scene.record_btn.destroy()
        scene.record_btn = btn

    def record_and_check_ai(ref_text, speaking_index, btn):
        scene.board_writer.write_on_board("Đang ghi âm... Hãy nói vào micro!", speak=False)
        samplerate = 16000
        duration = 5
        try:
            recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()
            temp_path = tempfile.mktemp(suffix='.wav')
            wav.write(temp_path, samplerate, recording)
            # --- Nhận diện bằng Whisper ---
            scene.board_writer.write_on_board("Đang nhận diện phát âm bằng AI...", speak=False)
            model = whisper.load_model("base")  # base/tiny/small/medium/large (base là đủ nhanh)
            result = model.transcribe(temp_path, language='en')
            user_text = result['text'].strip().lower()
            ref_text_clean = ref_text.strip().lower()
            os.remove(temp_path)
            # So sánh:
            score, wrong_words = check_pronunciation(ref_text_clean, user_text)
            feedback = f"Bạn nói: {user_text}\n"
            feedback += f"Điểm phát âm: {score:.1f}/10\n"
            if wrong_words:
                feedback += f"Từ cần chú ý: {', '.join(wrong_words)}"
            else:
                feedback += "Rất tốt! Không có từ nào sai."
            scene.board_writer.write_on_board(feedback, speak=False)
            btn.destroy()
            make_next_btn(speaking_index+1)
        except Exception as e:
            scene.board_writer.write_on_board(f"Lỗi ghi âm hoặc AI: {e}", speak=False)

    def check_pronunciation(ref, user):
        ref_words = ref.replace('.', '').replace(',', '').split()
        user_words = user.replace('.', '').replace(',', '').split()
        correct = sum(1 for w, u in zip(ref_words, user_words) if w == u)
        score = 10 * correct / max(1, len(ref_words))
        wrong = [w for w, u in zip(ref_words, user_words) if w != u]
        return score, wrong

    def make_next_btn(next_index):
        from direct.gui.DirectGui import DirectButton
        btn = DirectButton(
            text="Next Speaking",
            scale=0.07,
            pos=(1.1, 0, -0.7),
            frameColor=(0.13,0.18,0.13,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: (btn.destroy(), unlock_next(next_index)),
        )

    def unlock_next(next_index):
        if hasattr(scene, "sample_btn") and scene.sample_btn:
            scene.sample_btn.destroy()
        if hasattr(scene, "record_btn") and scene.record_btn:
            scene.record_btn.destroy()
        scene.current_speaking_index = next_index
        show_speaking(next_index)

    show_speaking(scene.current_speaking_index)
