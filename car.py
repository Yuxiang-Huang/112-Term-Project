from cmu_graphics import *


class Car:
    carSpeed = {
        "red": 1,
        "green": 2,
        "blue": 3,
        "purple": 4,
        "yellow": 5,
        "orange": 6,
    }

    def __init__(self, app, spawnType, spawnRail):
        self.type = spawnType
        self.speed = Car.carSpeed[self.type]

        # fix size later
        self.size = app.unitX * (6 - self.speed + 1) / 6 / 3

        self.rail = spawnRail
        self.pos = spawnRail.toWorldPos(app)

    def display(self):
        drawCircle(self.pos[0], self.pos[1], self.size, fill=self.type)
