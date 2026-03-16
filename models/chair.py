# models/chair.py
from panda3d.core import CardMaker

class Chair3D:
    def __init__(self, render, x, y, w, d, h, seat_h, color=(1,1,1,1), backrest=True, backrest_height=0.3, face_angle=0):
        self.render = render
        self.chair = self._create_chair(x, y, w, d, h, seat_h, color, backrest, backrest_height, face_angle)

    def _create_chair(self, x, y, w, d, h, seat_h, color, backrest, backrest_height, face_angle):
        seat = CardMaker("chair_seat")
        seat.setFrame(-w/2, w/2, -d/2, d/2)
        seat_np = self.render.attachNewNode(seat.generate())
        seat_np.setPos(x, y, seat_h)
        seat_np.setHpr(face_angle, -90, 0)
        seat_np.setColor(*color)
        for dx, dy in [(-w/2+0.07, -d/2+0.07), (w/2-0.07, -d/2+0.07), (-w/2+0.07, d/2-0.07), (w/2-0.07, d/2-0.07)]:
            leg = CardMaker("chair_leg")
            leg.setFrame(-0.04, 0.04, 0, seat_h)
            leg_np = self.render.attachNewNode(leg.generate())
            leg_np.setPos(x + dx, y + dy, 0)
            leg_np.setHpr(face_angle, 0, 0)
            leg_np.setColor(color[0]*0.6, color[1]*0.6, color[2]*0.6, 1)
        if backrest:
            back_cm = CardMaker("chair_backrest")
            back_cm.setFrame(-w/2+0.05, w/2-0.05, 0, backrest_height)
            back_np = self.render.attachNewNode(back_cm.generate())
            back_np.setPos(x, y - d/2 + 0.05, seat_h + 0.01)
            back_np.setHpr(face_angle, 0, 0)
            back_np.setColor(color[0]*0.85, color[1]*0.85+0.05, color[2]*0.85+0.1, 1)
        return seat_np
