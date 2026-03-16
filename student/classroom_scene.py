from models.classroom import ClassroomScene
from direct.gui.DirectGui import DirectButton, DGG
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from direct.interval.IntervalGlobal import LerpPosInterval, LerpHprInterval, Sequence, Func
import sys

BTN_COLORS = [
    (0.12, 0.32, 0.78, 1),
    (0.85, 0.43, 0.13, 1),
    (0.18, 0.59, 0.26, 1),
    (0.42, 0.21, 0.67, 1),
    (0.77, 0.13, 0.29, 1),
    (0.10, 0.46, 0.67, 1),
    (0.96, 0.34, 0.21, 1),
    (0.50, 0.15, 0.55, 1),
    (0.18, 0.18, 0.18, 1)
]

STUDENT_MODULES = [
    {"name": "Achievement", "module": "student.achievements", "group": "Kỹ năng"},
    {"name": "Grammar", "module": "student.grammar_practice", "group": "Kỹ năng"},
    {"name": "Vocabulary", "module": "student.vocab_practice", "group": "Kỹ năng"},
    {"name": "Listening", "module": "student.listening_practice", "group": "Kỹ năng"},
    {"name": "Reading", "module": "student.reading_practice", "group": "Kỹ năng"},
    {"name": "Speaking", "module": "student.speaking_practice", "group": "Kỹ năng"},
    {"name": "Quiz", "module": "student.quiz", "group": "Luyện tập"},
    {"name": "Homework", "module": "student.submit_homework", "group": "Luyện tập"},
    {"name": "Profile", "module": "student.profile", "group": "Hồ sơ"}
]

class StudentScene(ClassroomScene):
    def __init__(self, fullname):
        super().__init__()
        self.fullname = fullname
        self.buttons = []
        self.temp_msg = None
        self.setup_ui()

    def setup_ui(self):
        short_name = self.fullname.split()[0] if " " in self.fullname else self.fullname
        self.user_text = OnscreenText(
            text=f"\U0001F44B Xin chào, {short_name}!",
            pos=(-1.50, 0.92), scale=0.07,
            fg=(0.11, 0.16, 0.22, 1),
            align=TextNode.ALeft, mayChange=True
        )

        y_cursor = 0.85
        current_group = None
        for i, mod in enumerate(STUDENT_MODULES):
            if mod.get("group") != current_group:
                current_group = mod["group"]
                label = OnscreenText(
                    text=f"📂 {current_group}", pos=(1.6, y_cursor), scale=0.05,
                    fg=(0.25, 0.25, 0.25, 1), align=TextNode.ACenter
                )
                y_cursor -= 0.08

            color = BTN_COLORS[i % len(BTN_COLORS)]
            btn = DirectButton(
                text=mod["name"],
                scale=0.07,
                pos=(1.60, 0, y_cursor),
                frameColor=color,
                text_fg=(1, 1, 1, 1),
                borderWidth=(0.12, 0.09),
                frameSize=(-2.8, 2.8, -0.6, 0.6),
                relief=1,
                pad=(0.15, 0.13),
                text_align=TextNode.ACenter,
                command=self.handle_button,
                extraArgs=[mod]
            )
            btn.setTransparency(True)
            btn.bind(DGG.B1PRESS, self.spring_btn, [btn])
            btn.bind(DGG.B1RELEASE, self.unspring_btn, [btn])
            self.buttons.append(btn)
            y_cursor -= 0.13

        self.logout_btn = DirectButton(
            text="Đăng xuất", scale=0.06, pos=(1.60, 0, y_cursor - 0.1),
            frameColor=(0.6, 0.1, 0.1, 1), text_fg=(1, 1, 1, 1),
            command=self.logout
        )

    def spring_btn(self, btn, event):
        btn['scale'] = btn['scale'] * 0.88

    def unspring_btn(self, btn, event):
        btn['scale'] = btn['scale'] / 0.88

    def handle_button(self, mod):
        name = mod["name"]
        try:
            if name == "Achievement":
                import student.achievements as ach
                ach.run_view_achievements(self, self.fullname)
            elif name == "Grammar":
                import student.grammar_practice as grammar
                grammar.run_grammar_practice(self, self.fullname)
            elif name == "Vocabulary":
                import student.vocab_practice as vocab
                vocab.run_vocab_practice(self)
            elif name == "Listening":
                import student.listening_practice as listening
                listening.run_listening_practice(self, self.fullname)
            elif name == "Reading":
                import student.reading_practice as reading
                reading.run_reading_practice(self)
            elif name == "Quiz":
                import student.quiz as quiz
                quiz.show_quiz(self)
            elif name == "Homework":
                import student.submit_homework as hw
                hw.run_submit_homework(self, self.fullname)
            elif name == "Speaking":
                import student.speaking_practice as speaking
                speaking.run_speaking_practice(self)
            elif name == "Profile":
                import student.profile as profile
                profile.show_profile(self, self.fullname)
            else:
                self.show_temp_message("Chức năng chưa hỗ trợ.")
        except Exception as e:
            self.show_temp_message(f"Lỗi {name}: {e}")

    def show_temp_message(self, msg, duration=1.5):
        if self.temp_msg:
            self.temp_msg.destroy()
            self.temp_msg = None

        self.temp_msg = OnscreenText(
            text=msg, pos=(0, 0.75), scale=0.085, fg=(1, 0.24, 0.2, 1), mayChange=True
        )

        def hide_msg(task):
            if self.temp_msg:
                self.temp_msg.destroy()
                self.temp_msg = None
            return task.done

        self.taskMgr.doMethodLater(duration, hide_msg, "hide_temp_msg")

    def logout(self):
        print("Đăng xuất...")
        sys.exit(0)


def zoom_to_board(self, after_func=None):
    cam = self.camera
    seq = Sequence(
        LerpPosInterval(cam, 0.7, (0, 2, 5)),
        LerpHprInterval(cam, 0.6, (0, -15, 0)),
    )
    if after_func:
        seq.append(Func(after_func))
    seq.start()


def zoom_out(self, after_func=None):
    cam = self.camera
    seq = Sequence(
        LerpPosInterval(cam, 0.7, (0, -22, 14)),
        LerpHprInterval(cam, 0.6, (0, -35, 0)),
    )
    if after_func:
        seq.append(Func(after_func))
    seq.start()

ClassroomScene.zoom_to_board = zoom_to_board
ClassroomScene.zoom_out = zoom_out

if __name__ == "__main__":
    scene = StudentScene("Harry Nguyễn")
    scene.run()
