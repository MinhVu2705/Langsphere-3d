from utils.database import load_db

def run_vocab_practice(scene):
    """
    Khi được gọi, sẽ cho học vocab theo thứ tự level (A1 → A2 → ...)
    - Khi học xong 1 level (bấm 'Next' hoặc học hết), mới unlock level tiếp theo.
    """
    # Lưu trạng thái level đang học vào scene (hoặc có thể dùng user profile/score)
    if not hasattr(scene, "current_vocab_level"):
        scene.current_vocab_level = "A1"

    def show_level(level):
        vocab_data = load_db('vocab_db.json')
        vocab_this_level = [entry for entry in vocab_data if entry.get("level") == level]
        if not vocab_this_level:
            scene.board_writer.write_on_board(f"Đã hết từ vựng cho level {level}.", speak=False)
            return
        topic = vocab_this_level[0].get("topic", "No topic")
        lines = [f"Vocabulary Practice\nLevel: {level}", f"Topic: {topic}"]
        for entry in vocab_this_level:
            word = entry.get("word", "")
            meaning = entry.get("meaning", "")
            example = entry.get("example", "")
            lines.append(f"{word} ({meaning})\nEg: {example}")
        board_text = "\n\n".join(lines)
        def after_zoom():
            scene.board_writer.write_on_board(board_text, speak=True)
            # Thêm nút "Next Level" nếu còn level sau
            if level == "A1":
                scene.next_level_btn = make_next_btn(lambda: unlock_next("A2"))
            elif level == "A2":
                scene.next_level_btn = make_next_btn(lambda: unlock_next("B1"))
            # ... có thể mở rộng thêm các level khác
        if hasattr(scene, "zoom_to_board"):
            scene.zoom_to_board(after_zoom)
        else:
            scene.camera.setPos(0, 2, 5)
            scene.camera.lookAt(0, 7.8, 3.2)
            after_zoom()

    def unlock_next(next_level):
        # Xóa nút Next cũ nếu có
        if hasattr(scene, "next_level_btn") and scene.next_level_btn:
            scene.next_level_btn.destroy()
        scene.current_vocab_level = next_level
        show_level(next_level)

    def make_next_btn(callback):
        from direct.gui.DirectGui import DirectButton
        return DirectButton(
            text="Next Level",
            scale=0.07,
            pos=(1.1, 0, -0.8),
            frameColor=(0.13,0.18,0.13,1),
            text_fg=(1,1,1,1),
            relief=1,
            command=callback,
        )

    show_level(scene.current_vocab_level)
