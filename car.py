from cmu_graphics import *
from rail import *


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
        # change size according to type later
        self.size = app.unitX / 4  # * (6 - self.speed / 2 + 1) / 6
        self.animationCount = 0

        # pretend there is a straight rail connect to the spawn rail
        self.movingFrom = spawnRail.spawnCarDirection
        self.movingTo = Rail.directionComplement[self.movingFrom]
        self.nextRail = spawnRail
        self.changeRail(app.map)

    def display(self):
        drawCircle(self.pos[0], self.pos[1], self.size, fill=self.type)

    def move(self, map):
        # animate time between tracks
        self.animationCount += 1
        if self.animationCount >= self.speed:
            self.changeRail(map)
            self.animationCount = 0

    def changeRail(self, map):
        # moving from is the opposite of moving to
        self.movingFrom = Rail.directionComplement[self.movingTo]
        # change rail to the next rail
        self.rail = self.nextRail
        # change position accordingly (FOR NOW)
        self.pos = self.rail.toWorldPos(app)
        # moving to is the other direction of this rail
        self.movingTo = (self.rail.directions - {self.movingFrom}).pop()
        # calculate next rail
        self.nextRail = self.calculateNextRail(map)

    def calculateNextRail(self, map):
        # using moving to to calculate rail
        dif = Rail.directionToDif[self.movingTo]
        curIndices = self.rail.indices
        return map.rails[curIndices[0] + dif[0]][curIndices[1] + dif[1]]
