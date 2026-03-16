from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from utils.tts import speak_current

class BoardWriter:
    def __init__(self, base, aspect2d):
        self.base = base
        self.aspect2d = aspect2d
        self.board_text = None

    def write_on_board(self, full_text, color=(1,1,1,1), scale=0.07, speed=0.03, speak=True):
        """
        Hiện từng ký tự lên bảng như đang viết tay (speed nhỏ hơn sẽ nhanh hơn)
        Nếu speak=True thì phát âm đoạn text khi viết xong.
        """
        # Xóa text cũ nếu có
        if hasattr(self, "board_text") and self.board_text:
            self.board_text.destroy()

        self._full_text = full_text
        self._displayed = ""
        self._char_idx = 0
        self._board_color = color
        self._board_scale = scale

        def next_char(task):
            if self._char_idx < len(self._full_text):
                self._displayed += self._full_text[self._char_idx]
                if hasattr(self, "board_text") and self.board_text:
                    self.board_text.setText(self._displayed)
                else:
                    self.board_text = OnscreenText(
                        text=self._displayed,
                        pos=(0, 0.43), scale=self._board_scale,
                        fg=self._board_color,
                        align=TextNode.ACenter,
                        parent=self.aspect2d, mayChange=True
                    )
                self._char_idx += 1
                return task.again
            # Phát âm sau khi viết xong
            if speak and self._full_text.strip():
                speak_current(self._full_text)
            return task.done

        # Khởi tạo text rỗng
        self.board_text = OnscreenText(
            text="",
            pos=(0, 0.43), scale=scale,
            fg=color, align=TextNode.ACenter,
            parent=self.aspect2d, mayChange=True
        )
        self.base.taskMgr.doMethodLater(speed, next_char, "write_on_board")
