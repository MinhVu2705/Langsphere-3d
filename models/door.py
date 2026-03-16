# models/door.py
from panda3d.core import CardMaker

class Door3D:
    def __init__(self, render, x, y, z=1.5, width=2, height=3, hpr=(0,0,0), color=(0.36, 0.23, 0.12, 1)):
        door_cm = CardMaker("door")
        door_cm.setFrame(0, width, 0, height)
        door = render.attachNewNode(door_cm.generate())
        door.setPos(x, y, z)
        door.setHpr(*hpr)
        door.setColor(*color)
        self.node = door
