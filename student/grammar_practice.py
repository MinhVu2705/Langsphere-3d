from utils.database import load_db, save_db
from direct.interval.IntervalGlobal import Sequence, Func
from direct.gui.DirectGui import DirectButton
import random

def run_grammar_practice(scene, username="anonymous"):
    grammar_order = ["Present Simple", "Present Continuous", "Past Simple"]

    user_db = load_db("user_db.json")
    user = next((u for u in user_db if u["username"] == username), None)
    if not user:
        scene.board_writer.write_on_board("Không tìm thấy tài khoản!", speak=False)
        return

    if "grammar_index" not in user:
        user["grammar_index"] = 0

    def save_user_index(idx):
        user["grammar_index"] = idx
        save_db("user_db.json", user_db)

    def set_btn_scale(btn, val):
        btn.setScale(val)

    def animate_congrats():
        msg = random.choice(["🎉 GIỎI QUÁ! 🎉", "✨Bạn đã hoàn thành!✨", "🏆 Congratulations! 🏆"])
        scene.board_writer.write_on_board(msg, color=(1, 0.87, 0.22, 1), scale=0.09, speed=0.025, speak=False)
        btn = DirectButton(
            text="Học lại từ đầu",
            scale=0.058,
            pos=(1.08,0,-0.88),
            frameColor=(0.98,0.64,0.13,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=lambda: restart()
        )
        btn.setTransparency(True)
        seq = Sequence(Func(set_btn_scale, btn, 0.04))
        for i in range(6):
            seq.append(Func(set_btn_scale, btn, 0.065 + 0.005 * ((-1) ** i)))
        seq.append(Func(set_btn_scale, btn, 0.058))
        seq.start()
        scene.next_tense_btn = btn

    def animate_next_btn(btn):
        seq = Sequence(Func(set_btn_scale, btn, 0.055))
        for i in range(5):
            seq.append(Func(set_btn_scale, btn, 0.072 + 0.005 * ((-1) ** i)))
        seq.append(Func(set_btn_scale, btn, 0.069))
        seq.start()

    def show_tense(index):
        try:
            grammar_data = load_db('grammar_db.json')
        except Exception:
            scene.board_writer.write_on_board("Không load được dữ liệu ngữ pháp.", speak=False)
            return
        if index >= len(grammar_order):
            animate_congrats()
            return
        tense = grammar_order[index]
        lesson = next((g for g in grammar_data if g.get("tense") == tense), None)
        if not lesson:
            scene.board_writer.write_on_board(f"Không có dữ liệu cho thì: {tense}", speak=False)
            return
        title = lesson.get("title", tense)
        theory = lesson.get("theory", "")
        example = lesson.get("example", "")
        content = f"{title}\n{theory}\n\nEg: {example}"

        def after_zoom():
            scene.board_writer.write_on_board(content, color=(1,1,1,1), scale=0.07, speed=0.027, speak=True)
            if index < len(grammar_order) - 1:
                if hasattr(scene, "next_tense_btn") and scene.next_tense_btn:
                    scene.next_tense_btn.destroy()
                btn = DirectButton(
                    text="Next Tense",
                    scale=0.069,
                    pos=(1.1, 0, -0.8),
                    frameColor=(0.13,0.18,0.33,1),
                    text_fg=(1,1,1,1),
                    relief=1,
                    command=lambda: unlock_next(index + 1),
                )
                btn.setTransparency(True)
                animate_next_btn(btn)
                scene.next_tense_btn = btn
            else:
                animate_congrats()

        if hasattr(scene, "zoom_to_board"):
            scene.zoom_to_board(after_zoom)
        else:
            scene.camera.setPos(0, 2, 5)
            scene.camera.lookAt(0, 7.8, 3.2)
            after_zoom()

    def unlock_next(next_index):
        if hasattr(scene, "next_tense_btn") and scene.next_tense_btn:
            scene.next_tense_btn.destroy()
        save_user_index(next_index)
        show_tense(next_index)

    def restart():
        if hasattr(scene, "next_tense_btn") and scene.next_tense_btn:
            scene.next_tense_btn.destroy()
        save_user_index(0)
        show_tense(0)

    if hasattr(scene, "next_tense_btn") and scene.next_tense_btn:
        scene.next_tense_btn.destroy()

    idx = user.get("grammar_index", 0)
    show_tense(idx)
