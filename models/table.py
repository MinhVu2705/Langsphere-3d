# models/table.py
from panda3d.core import CardMaker

class Table3D:
    def __init__(self, render, x, y, w, d, h, color=(1,1,1,1), with_legs=True):
        self.render = render
        self.table = self._create_table(x, y, w, d, h, color, with_legs)

    def _create_table(self, x, y, w, d, h, color, with_legs):
        top = CardMaker("table_top")
        top.setFrame(-w/2, w/2, -d/2, d/2)
        table = self.render.attachNewNode(top.generate())
        table.setPos(x, y, h)
        table.setHpr(0, -90, 0)
        table.setColor(*color)
        if with_legs:
            for dx, dy in [(-w/2+0.1, -d/2+0.1), (w/2-0.1, -d/2+0.1), (-w/2+0.1, d/2-0.1), (w/2-0.1, d/2-0.1)]:
                leg = CardMaker("leg")
                leg.setFrame(-0.07, 0.07, 0, h)
                leg_np = self.render.attachNewNode(leg.generate())
                leg_np.setPos(x + dx, y + dy, 0)
                leg_np.setHpr(0,0,0)
                leg_np.setColor(color[0]*0.7, color[1]*0.7, color[2]*0.7, 1)
        return table
