# models/laptop.py
from panda3d.core import CardMaker

class Laptop3D:
    def __init__(self, render, x, y, z, body_w=0.6, body_d=0.4, body_h=0.03, screen_h=0.33):
        # Thân
        body_cm = CardMaker("laptop_body")
        body_cm.setFrame(-body_w/2, body_w/2, -body_d/2, body_d/2)
        body = render.attachNewNode(body_cm.generate())
        body.setPos(x, y, z + body_h/2)
        body.setHpr(0, -90, 0)
        body.setColor(0.12, 0.12, 0.12, 1)
        self.body = body
        # Màn hình
        screen_cm = CardMaker("laptop_screen")
        screen_cm.setFrame(-body_w/2, body_w/2, 0, screen_h)
        screen = render.attachNewNode(screen_cm.generate())
        screen.setPos(x, y - body_d/2 + 0.01, z + body_h + 0.01)
        screen.setHpr(-10, 0, 0)
        screen.setColor(0.05, 0.15, 0.19, 1)
        self.screen = screen
