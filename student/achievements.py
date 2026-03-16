from utils.database import load_db, save_db
from datetime import datetime, timedelta
from collections import defaultdict


def run_view_achievements(scene, username="anonymous"):
    """
    Hiển thị achievements đã và chưa đạt, chi tiết, kèm icon.
    """
    all_badges = load_db("database/achievements_db.json")
    user_db = load_db("user_db.json")
    user = next((u for u in user_db if u["username"] == username), None)
    if not user:
        scene.board_writer.write_on_board("Không tìm thấy tài khoản!", speak=False)
        return

    # Cập nhật badges nếu có badge mới unlock
    new_badges = check_and_unlock_badges(user)
    if new_badges:
        scene.board_writer.write_on_board(f"🎉 Bạn vừa mở khóa {len(new_badges)} huy hiệu mới!", speak=True)
    save_db("user_db.json", user_db)

    user_badges = set(b["id"] for b in user.get("badge_history", []))

    # Tổng hợp bảng theo mode
    mode_summary = defaultdict(int)
    for b in user.get("badge_history", []):
        matched = next((a for a in all_badges if a["id"] == b["id"]), None)
        if matched and "mode" in matched["condition"]:
            mode_summary[matched["condition"]["mode"]] += 1

    summary_lines = ["📊 THỐNG KÊ HUY HIỆU THEO KỸ NĂNG"]
    for mode, count in mode_summary.items():
        summary_lines.append(f"{mode.capitalize()}: {count} badge(s)")

    # Thống kê theo ngày (7 ngày gần nhất)
    date_summary = defaultdict(int)
    now = datetime.now()
    for b in user.get("badge_history", []):
        try:
            date = datetime.fromisoformat(b["unlocked_at"]).date()
            if now.date() - date <= timedelta(days=6):
                date_summary[str(date)] += 1
        except:
            continue

    summary_lines.append("\n📅 HUY HIỆU ĐẠT TRONG 7 NGÀY QUA")
    for i in range(6, -1, -1):
        d = now.date() - timedelta(days=i)
        summary_lines.append(f"{d}: {date_summary.get(str(d), 0)} badge(s)")

    # Hiển thị chính
    lines = []
    for badge in all_badges:
        unlocked = badge["id"] in user_badges or badge["name"] in user_badges
        status = "✅" if unlocked else "🔒"
        lines.append(f"{status} {badge['name']}: {badge['description']}")
    text = "🏅 ACHIEVEMENTS 🏅\n" + "\n".join(lines)
    scene.board_writer.write_on_board(text + "\n\n" + "\n".join(summary_lines), speak=False)

    show_badge_detail_btn(scene, all_badges, user_badges)


def get_progress(username):
    return {
        "grammar": 7,
        "vocab": 8,
        "login_streak": 5,
        "listening": 4,
        "reading": 2,
        "speaking": 3,
        "quiz": 20
    }


def check_and_unlock_badges(user):
    all_badges = load_db("achievements_db.json")
    progress = get_progress(user["username"])
    badge_history = user.setdefault("badge_history", [])
    unlocked_ids = set(b["id"] for b in badge_history)
    newly_unlocked = []

    for badge in all_badges:
        cond = badge["condition"]
        mode = cond.get("mode")
        completed = cond.get("completed")
        streak = cond.get("login_streak")
        badge_id = badge["id"]

        should_unlock = False
        if mode and progress.get(mode, 0) >= completed:
            should_unlock = True
        if streak and progress.get("login_streak", 0) >= streak:
            should_unlock = True

        if should_unlock and badge_id not in unlocked_ids:
            badge_history.append({
                "id": badge_id,
                "unlocked_at": datetime.now().isoformat()
            })
            newly_unlocked.append(badge_id)

    return newly_unlocked


def show_badge_detail_btn(scene, all_badges, user_badges):
    from direct.gui.DirectGui import DirectButton
    from direct.gui.OnscreenImage import OnscreenImage

    if not hasattr(scene, "badge_images"):
        scene.badge_images = []

    def show_detail():
        for img in scene.badge_images:
            img.destroy()
        scene.badge_images = []

        y_start = -0.3
        delta = 0.19
        for idx, badge in enumerate(all_badges):
            pos_y = y_start - idx * delta
            icon_path = badge["icon"]
            img = OnscreenImage(image=icon_path, pos=(0.95, 0, pos_y), scale=0.09)
            img.setTransparency(True)
            scene.badge_images.append(img)

            status = "Đã đạt" if badge["id"] in user_badges else "Chưa đạt"
            scene.board_writer.write_on_board(
                f"{badge['name']} ({status})\n{badge['description']}", speak=False
            )

    btn = DirectButton(
        text="Xem chi tiết badges", scale=0.048, pos=(1.12, 0, -0.18),
        frameColor=(0.22, 0.18, 0.22, 1), text_fg=(1, 1, 1, 1),
        command=show_detail
    )
