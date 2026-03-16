# models/classroom.py

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, AmbientLight, DirectionalLight
from models.table import Table3D
from models.chair import Chair3D
from models.board import Board3D
from models.board_writer import BoardWriter
from models.wall import Wall3D
from models.window import Window3D
from models.door import Door3D
from models.laptop import Laptop3D

class ClassroomScene(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.set_background_color(0.28, 0.31, 0.34)
        self.camera.setPos(0, -22, 14)
        self.camera.lookAt(0, 0, 5)

        # ===== ÁNH SÁNG =====
        alight = AmbientLight("ambient")
        alight.setColor((0.48, 0.48, 0.51, 1))
        self.render.setLight(self.render.attachNewNode(alight))
        dlight = DirectionalLight("directional")
        dlight.setColor((0.56, 0.56, 0.60, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(70, -35, 0)
        self.render.setLight(dlnp)

        # ===== SÀN LỚP HỌC =====
        cm = CardMaker("floor")
        cm.setFrame(-12, 12, -8, 8)
        floor = self.render.attachNewNode(cm.generate())
        floor.setPos(0, 0, 0)
        floor.setHpr(0, -90, 0)
        floor.setColor(0.58, 0.49, 0.39, 1)

        # ===== TƯỜNG =====
        Wall3D(self.render, x=0, y=8, hpr=(0,0,0))
        Wall3D(self.render, x=0, y=-8, hpr=(180,0,0))
        Wall3D(self.render, x=-12, y=0, hpr=(90,0,0))
        Wall3D(self.render, x=12, y=0, hpr=(-90,0,0))  # Tường bên phải (có cửa sổ)

        # ===== CỬA SỔ =====
        Window3D(self.render, x=12-0.05, y=0, z=7, width=5, height=2.5)

        # ===== CỬA RA VÀO =====
        Door3D(self.render, x=-10, y=-8, z=1.5)

        # ===== BẢNG XANH 3D =====
        self.board = Board3D(self.render, x=0, y=7.8, z=3.2,
                             width=10, height=4.8, frame=0.28,
                             frame_color=(0.13, 0.08, 0.03, 1))

        # ===== BOARD WRITER (chữ hiện từ từ, phát âm) =====
        self.board_writer = BoardWriter(self, self.aspect2d)   # Sửa ở đây!

        # ===== BÀN GIÁO VIÊN =====
        self.teacher_table = Table3D(self.render, x=-10.0, y=6.5, w=2.4, d=1.2, h=1.1, color=(0.60, 0.35, 0.15, 1))

        # ===== GHẾ GIÁO VIÊN =====
        self.teacher_chair = Chair3D(self.render, x=-10.0, y=5.0, w=1.2, d=1.0, h=1.15, seat_h=0.78,
                                     color=(0.8, 0.1, 0.15, 1), backrest=True, backrest_height=0.6, face_angle=0)

        # ===== LAPTOP BÀN GIÁO VIÊN =====
        Laptop3D(self.render, x=-10.0, y=6.6, z=1.1)

        # ===== BÀN & GHẾ HỌC SINH =====
        student_table_w = 1.7
        student_table_d = 0.7
        student_table_x_spacing = 4.4
        for row in range(3):
            for col in range(4):
                x = (col - 1.5) * student_table_x_spacing
                y = (row - 1) * 3
                Table3D(self.render, x, y, w=student_table_w, d=student_table_d, h=0.8, color=(0.68, 0.51, 0.28, 1))
                Chair3D(self.render, x, y-1.2, w=0.7, d=0.8, h=0.7, seat_h=0.42,
                        color=(0.35+0.1*row, 0.25, 0.12+0.08*col, 1), backrest=True, backrest_height=0.35, face_angle=0)

        # ===== DEMO: VIẾT BẢNG & PHÁT ÂM =====
        self.accept("f1", self.demo_write_on_board)  # Ấn F1 để test hiệu ứng bảng

    def demo_write_on_board(self):
        text = "Hello students!\nToday we learn about insurance.\nAre you ready?"
        self.board_writer.write_on_board(text, speak=True)

if __name__ == "__main__":
    app = ClassroomScene()
    app.demo_write_on_board()  # Auto demo khi chạy
    app.run()
