from gtts import gTTS
from playsound import playsound
import tempfile
import os
import threading

def speak(text, lang='en', async_play=True):
    """Phát âm text bằng Google TTS. Có thể chạy async."""
    def _play():
        if not text:
            return
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts = gTTS(text=text, lang=lang)
                tts.save(fp.name)
                playsound(fp.name)
            os.remove(fp.name)
        except Exception as e:
            print(f"Lỗi phát âm: {e}")

    if async_play:
        threading.Thread(target=_play, daemon=True).start()
    else:
        _play()

def speak_current(text, lang='en', async_play=True):
    """Alias cho speak, không kiểm tra scene. Giữ lại cho code cũ."""
    speak(text, lang=lang, async_play=async_play)
