# models/wall.py
from panda3d.core import CardMaker

class Wall3D:
    def __init__(self, render, x, y, z=3, width=24, height=6, hpr=(0,0,0), color=(0.78, 0.81, 0.87, 1)):
        cm = CardMaker("wall")
        cm.setFrame(-width/2, width/2, 0, height)
        wall = render.attachNewNode(cm.generate())
        wall.setPos(x, y, z)
        wall.setHpr(*hpr)
        wall.setColor(*color)
        self.node = wall
