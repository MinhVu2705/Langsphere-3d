# models/window.py
from panda3d.core import CardMaker

class Window3D:
    def __init__(self, render, x, y, z, width=3, height=2, thickness=0.05):
        # Frame
        frame_cm = CardMaker("window_frame")
        frame_cm.setFrame(-width/2, width/2, 0, height)
        frame = render.attachNewNode(frame_cm.generate())
        frame.setPos(x, y+0.01, z - height/2)
        frame.setHpr(0, 90, 0)
        frame.setColor(0.92, 0.95, 1, 1)
        self.frame = frame
        # Glass
        glass_cm = CardMaker("window_glass")
        glass_cm.setFrame(-width/2+0.12, width/2-0.12, 0.15, height-0.12)
        glass = render.attachNewNode(glass_cm.generate())
        glass.setPos(x, y+0.02, z - height/2)
        glass.setHpr(0, 90, 0)
        glass.setColor(0.62, 0.81, 1, 0.72)
        self.glass = glass
