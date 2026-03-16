# models/board.py
from panda3d.core import CardMaker

class Board3D:
    def __init__(self, render, x, y, z, width=10, height=4.8, frame=0.28, frame_color=(0.13, 0.08, 0.03, 1)):
        self.render = render
        self.board = self._create_framed_board(x, y, z, width, height, frame, frame_color)

    def _create_framed_board(self, x, y, z, width, height, frame, frame_color):
        board_cm = CardMaker("board")
        board_cm.setFrame(-width/2+frame, width/2-frame, frame, height-frame)
        board = self.render.attachNewNode(board_cm.generate())
        board.setPos(x, y, z)
        board.setHpr(0, 0, 0)
        board.setColor(0.11, 0.28, 0.13, 1)
        # Khung viền dọc
        for dx in [-width/2, width/2-frame*2]:
            edge = CardMaker("frame_vert")
            edge.setFrame(0, frame, 0, height)
            edge_np = self.render.attachNewNode(edge.generate())
            edge_np.setPos(x + dx + frame/2, y + 0.01, z)
            edge_np.setColor(*frame_color)
        # Khung viền ngang
        for dy in [0, height-frame]:
            edge = CardMaker("frame_hori")
            edge.setFrame(-width/2, width/2, 0, frame)
            edge_np = self.render.attachNewNode(edge.generate())
            edge_np.setPos(x, y + 0.01, z + dy)
            edge_np.setColor(*frame_color)
        return board
