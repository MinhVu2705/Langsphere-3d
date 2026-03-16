from utils.database import load_db
from utils.tts import speak_current

def run_reading_practice(scene):
    if not hasattr(scene, "current_reading_index"):
        scene.current_reading_index = 0

    reading_data = load_db('reading_db.json')

    def show_reading(index):
        if index >= len(reading_data):
            scene.board_writer.write_on_board("Bạn đã hoàn thành tất cả bài Reading!", speak=False)
            return
        entry = reading_data[index]
        title = entry.get("title", "Reading Practice")
        content = entry.get("content", "")
        board_text = f"{title}\n\n{content}\n\n(Ấn 'Nghe mẫu' để nghe AI đọc đoạn này)"
        def after_zoom():
            scene.board_writer.write_on_board(board_text, speak=False)
            make_tts_btn(content)
            if entry.get("quiz"):
                scene.taskMgr.doMethodLater(2.2, lambda t: run_quiz(entry["quiz"], index), "show_reading_quiz")
            else:
                scene.taskMgr.doMethodLater(2, lambda t: show_next_btn(index+1), "reading_next_btn")
        if hasattr(scene, "zoom_to_board"):
            scene.zoom_to_board(after_zoom)
        else:
            scene.camera.setPos(0, 2, 5)
            scene.camera.lookAt(0, 7.8, 3.2)
            after_zoom()

    def make_tts_btn(text):
        from direct.gui.DirectGui import DirectButton
        btn = DirectButton(
            text="Nghe mẫu",
            scale=0.07,
            pos=(0.85, 0, -0.7),
            frameColor=(0.14,0.23,0.32,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: speak_current(text),
        )
        if hasattr(scene, "tts_btn") and scene.tts_btn:
            scene.tts_btn.destroy()
        scene.tts_btn = btn

    def run_quiz(quiz_list, reading_index):
        # Sử dụng biến session lưu trạng thái đúng/sai
        if not hasattr(scene, "quiz_result"):
            scene.quiz_result = []
        scene.quiz_result = []
        show_next_quiz(0, quiz_list, reading_index)

    def show_next_quiz(qi, quiz_list, reading_index):
        if qi >= len(quiz_list):
            # Nếu đúng hết thì unlock, sai thì báo lại
            n_correct = sum(scene.quiz_result)
            if n_correct == len(quiz_list):
                scene.board_writer.write_on_board("Bạn đã trả lời đúng tất cả! Tiếp tục bài tiếp theo...", speak=False)
                scene.taskMgr.doMethodLater(2, lambda t: show_next_btn(reading_index+1), "reading_next_after_all_quiz")
            else:
                scene.board_writer.write_on_board(f"Bạn đúng {n_correct}/{len(quiz_list)}. Thử lại toàn bộ quiz.", speak=False)
                scene.taskMgr.doMethodLater(2, lambda t: run_quiz(quiz_list, reading_index), "reading_retry_all_quiz")
            return
        quiz = quiz_list[qi]
        q_type = quiz.get("type", "mcq")
        if q_type == "mcq":
            show_mcq(quiz, lambda correct: after_quiz(qi, quiz_list, reading_index, correct, quiz))
        elif q_type == "blank":
            show_blank(quiz, lambda correct: after_quiz(qi, quiz_list, reading_index, correct, quiz))
        else:
            scene.board_writer.write_on_board("Unsupported quiz type!", speak=False)
            show_next_quiz(qi+1, quiz_list, reading_index)

    def after_quiz(qi, quiz_list, reading_index, correct, quiz):
        scene.quiz_result.append(correct)
        explanation = quiz.get("explanation", "")
        if correct:
            scene.board_writer.write_on_board(f"Đúng rồi!\n{explanation}", speak=False)
            scene.taskMgr.doMethodLater(1.2, lambda t: show_next_quiz(qi+1, quiz_list, reading_index), "reading_next_quiz")
        else:
            scene.board_writer.write_on_board(f"Sai nhé!\n{explanation}", speak=False)
            scene.taskMgr.doMethodLater(1.5, lambda t: show_next_quiz(qi+1, quiz_list, reading_index), "reading_next_quiz_wrong")

    def show_mcq(quiz, callback):
        from direct.gui.DirectGui import DirectButton
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
            return lambda: (destroy_btns(), callback(opt == answer))
        def destroy_btns():
            for b in btns:
                b.destroy()
        for i, opt in enumerate(options):
            btn = DirectButton(
                text=opt,
                scale=0.07,
                pos=(base_x, 0, base_y - i*spacing),
                frameColor=(0.16,0.22,0.22,1),
                text_fg=(1,1,1,1),
                relief=1,
                command=make_callback(opt),
            )
            btns.append(btn)

    def show_blank(quiz, callback):
        from direct.gui.DirectGui import DirectEntry, DirectButton
        question = quiz.get("question", "")
        answer = quiz.get("answer", "")
        scene.board_writer.write_on_board(f"Quiz: {question}\n(Điền từ vào chỗ trống)", speak=False)
        # Tạo ô nhập:
        entry = DirectEntry(
            scale=0.065,
            pos=(0.85, 0, -0.75),
            width=15,
            numLines=1,
            focus=1,
            frameColor=(0.22,0.28,0.23,1),
            initialText='',
            text_fg=(1,1,1,1)
        )
        btn = DirectButton(
            text="Kiểm tra",
            scale=0.055,
            pos=(1.1, 0, -0.75),
            frameColor=(0.15,0.22,0.18,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: (entry.destroy(), btn.destroy(), callback(entry.get().strip().lower() == answer.lower()))
        )

    def show_next_btn(next_index):
        from direct.gui.DirectGui import DirectButton
        btn = DirectButton(
            text="Next Reading",
            scale=0.07,
            pos=(1.1, 0, -0.7),
            frameColor=(0.13,0.18,0.13,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: (btn.destroy(), unlock_next(next_index)),
        )

    def unlock_next(next_index):
        if hasattr(scene, "tts_btn") and scene.tts_btn:
            scene.tts_btn.destroy()
        scene.current_reading_index = next_index
        show_reading(next_index)

    show_reading(scene.current_reading_index)
