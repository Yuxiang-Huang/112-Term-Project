from cmu_graphics import *


class Destination:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def display(self):
        drawRect(self.pos[0], self.pos[1], self.size, self.size, align="center")
