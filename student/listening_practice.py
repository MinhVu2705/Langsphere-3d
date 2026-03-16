from utils.database import load_db, save_db
from utils.tts import speak_current
from direct.interval.IntervalGlobal import Sequence, Func
from direct.gui.DirectGui import DirectButton

def run_listening_practice(scene, username="anonymous"):
    user_db = load_db("user_db.json")
    user = next((u for u in user_db if u["username"] == username), None)
    if not user:
        scene.board_writer.write_on_board("Không tìm thấy tài khoản!", speak=False)
        return

    if "listening_index" not in user:
        user["listening_index"] = 0

    listening_data = load_db('listening_db.json')

    def save_user_index(idx):
        user["listening_index"] = idx
        save_db("user_db.json", user_db)

    def set_btn_scale(btn, val):
        btn.setScale(val)

    def animate_next_btn(btn):
        seq = Sequence(Func(set_btn_scale, btn, 0.055))
        for i in range(5):
            seq.append(Func(set_btn_scale, btn, 0.072 + 0.005 * ((-1) ** i)))
        seq.append(Func(set_btn_scale, btn, 0.07))
        seq.start()

    def show_listening(index):
        if hasattr(scene, "next_listen_btn") and scene.next_listen_btn:
            scene.next_listen_btn.destroy()
        if index >= len(listening_data):
            scene.board_writer.write_on_board("🎉 Chúc mừng! Bạn đã hoàn thành tất cả bài luyện nghe.", speak=False)
            return
        entry = listening_data[index]
        title = entry.get("title", "Listening Practice")
        script = entry.get("script", "")
        board_text = f"Listening Practice\n{title}\n\n(Script sẽ đọc lên, bạn nghe kỹ!)"
        def after_zoom():
            scene.board_writer.write_on_board(board_text, speak=False)
            speak_current(script)
            if entry.get("quiz"):
                scene.taskMgr.doMethodLater(6, lambda t: show_quiz(entry["quiz"], index), "show_quiz")
            else:
                scene.taskMgr.doMethodLater(2, lambda t: show_next_btn(index+1), "show_next_btn")
        if hasattr(scene, "zoom_to_board"):
            scene.zoom_to_board(after_zoom)
        else:
            scene.camera.setPos(0, 2, 5)
            scene.camera.lookAt(0, 7.8, 3.2)
            after_zoom()

    def show_quiz(quiz_list, listening_index):
        if not quiz_list:
            show_next_btn(listening_index+1)
            return
        quiz = quiz_list[0]
        question = quiz.get("question", "")
        options = quiz.get("options", [])
        answer = quiz.get("answer", "")
        board_text = f"Quiz:\n{question}\n"
        for i, opt in enumerate(options):
            board_text += f"{i+1}. {opt}\n"
        scene.board_writer.write_on_board(board_text, speak=False)
        btns = []
        base_x = 0.8
        base_y = -0.5
        spacing = 0.14
        def make_callback(opt):
            return lambda: on_select(opt, answer, listening_index, btns)
        for i, opt in enumerate(options):
            btn = DirectButton(
                text=opt,
                scale=0.07,
                pos=(base_x, 0, base_y - i*spacing),
                frameColor=(0.15,0.26,0.25,1),
                text_fg=(1,1,1,1),
                relief=1,
                command=make_callback(opt),
            )
            btns.append(btn)

    def on_select(selected, answer, listening_index, btns):
        for b in btns:
            b.destroy()
        if selected == answer:
            scene.board_writer.write_on_board("Chính xác! Tiếp tục bài tiếp theo...", speak=False)
            scene.taskMgr.doMethodLater(2, lambda t: show_next_btn(listening_index+1), "next_after_quiz")
        else:
            scene.board_writer.write_on_board("Sai rồi! Thử lại bài quiz này.", speak=False)
            scene.taskMgr.doMethodLater(2, lambda t: show_listening(listening_index), "retry_quiz")

    def show_next_btn(next_index):
        if hasattr(scene, "next_listen_btn") and scene.next_listen_btn:
            scene.next_listen_btn.destroy()
        btn = DirectButton(
            text="Next Listening",
            scale=0.07,
            pos=(1.1, 0, -0.8),
            frameColor=(0.13,0.18,0.13,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: (btn.destroy(), unlock_next(next_index)),
        )
        btn.setTransparency(True)
        animate_next_btn(btn)
        scene.next_listen_btn = btn

    def unlock_next(next_index):
        save_user_index(next_index)
        show_listening(next_index)

    idx = user.get("listening_index", 0)
    show_listening(idx)
    scene.board_writer.write_on_board("🎧 Bắt đầu luyện nghe!", speak=True
                                    )
    