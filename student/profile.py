from utils.database import load_db
from direct.gui.DirectGui import DirectFrame, DirectButton
from direct.gui.OnscreenText import OnscreenText

def show_profile(scene, username="anonymous"):
    user_db = load_db("user_db.json")
    user = next((u for u in user_db if u["username"] == username), None)
    if not user:
        scene.board_writer.write_on_board("Không tìm thấy tài khoản!", speak=False)
        return

    fullname = user.get("fullname", username)
    email = user.get("email", "-")
    role = user.get("role", "-").capitalize()
    badges = user.get("badges", [])
    total_badges = len(badges)
    grammar_idx = user.get("grammar_index", 0)
    listening_idx = user.get("listening_index", 0)
    vocab_idx = user.get("vocab_index", 0)

    homeworks = [h for h in load_db("homework_db.json") if h["username"] == username]
    if homeworks:
        last_hw = homeworks[-1]
        last_hw_line = f"Bài tập gần nhất: {last_hw['type']} | {last_hw['status']} | {last_hw['submit_time']}"
    else:
        last_hw_line = "Chưa có bài tập đã nộp."

    # Tạo frame popup – tờ giấy trắng
    frame = DirectFrame(
        frameColor=(1,1,1,0.96),
        frameSize=(-0.8, 0.8, -0.7, 0.7),
        pos=(0,0,0),
        relief=1
    )

    # Hiện thông tin từng dòng (OnscreenText parent=frame)
    y = 0.55
    spacing = 0.13
    texts = []
    info_lines = [
        f"👤 {fullname}",
        f"Email: {email}",
        f"Username: {user.get('username', '-')}",
        f"Role: {role}",
        f"Huy hiệu đã đạt: {total_badges}" if total_badges else "Chưa có huy hiệu nào.",
        f"Tiến độ Grammar: {grammar_idx}",
        f"Tiến độ Vocabulary: {vocab_idx}",
        f"Tiến độ Listening: {listening_idx}",
        last_hw_line
    ]
    for line in info_lines:
        txt = OnscreenText(
            text=line,
            pos=(0, y),
            scale=0.07,
            fg=(0.18,0.18,0.22,1),
            mayChange=False,
            align=0,
            parent=frame
        )
        texts.append(txt)
        y -= spacing

    # Nút Đóng (Close)
    btn = DirectButton(
        text="Đóng",
        scale=0.07,
        pos=(0,0,-0.6),
        frameColor=(0.5,0.2,0.2,1),
        text_fg=(1,1,1,1),
        relief=1,
        parent=frame,
        command=lambda: close_popup()
    )

    def close_popup():
        frame.destroy()
        for t in texts:
            t.destroy()
        btn.destroy()

    # Lưu reference nếu muốn kiểm soát ngoài hàm này
    scene.profile_popup = frame

