from cmu_graphics import *
from rail import *
import math


class Car:
    carSpeed = {
        "red": 0.5,
        "green": 1,
        "blue": 1.5,
        "purple": 2,
        "yellow": 2.5,
        "orange": 3,
    }

    def __init__(self, app, spawnType, spawnRail):
        self.type = spawnType
        self.speed = Car.carSpeed[self.type]
        # change size according to type later
        self.size = app.unitSize / 4  # * (6 - self.speed / 2 + 1) / 6
        self.animationCount = 0

        self.rail = None

        # pretend there is a straight rail connect to the spawn rail
        self.movingFrom = spawnRail.spawnCarDirection
        self.movingTo = Rail.directionComplement[self.movingFrom]
        self.nextRail = spawnRail
        self.changeRail(app.map)

    def display(self):
        drawCircle(self.pos[0], self.pos[1], self.size, fill=self.type)

    def move(self, app):
        # region change pos base on animation count
        ratio = self.animationCount / (app.stepsPerSecond / app.speedFactor)
        railPos = self.rail.toWorldPos(app)
        # region straight cases
        if self.movingFrom == "left" and self.movingTo == "right":
            self.pos = (
                railPos[0] - app.unitSize / 2 + app.unitSize * ratio,
                railPos[1],
            )
        elif self.movingFrom == "right" and self.movingTo == "left":
            self.pos = (
                railPos[0] + app.unitSize / 2 - app.unitSize * ratio,
                railPos[1],
            )
        elif self.movingFrom == "top" and self.movingTo == "bottom":
            self.pos = (
                railPos[0],
                railPos[1] - app.unitSize / 2 + app.unitSize * ratio,
            )
        elif self.movingFrom == "bottom" and self.movingTo == "top":
            self.pos = (
                railPos[0],
                railPos[1] + app.unitSize / 2 - app.unitSize * ratio,
            )
        # endregion
        # region turn cases
        else:
            if self.movingFrom == "left" or self.movingTo == "right":
                xDir = 1
            elif self.movingFrom == "right" or self.movingTo == "left":
                xDir = -1

            if self.movingFrom == "top" or self.movingTo == "bottom":
                yDir = -1
            elif self.movingFrom == "bottom" or self.movingTo == "top":
                yDir = 1

            self.pos = (
                railPos[0] + math.cos(ratio * math.pi / 2) * xDir * app.unitSize / 2,
                railPos[1] + math.sin(ratio * math.pi / 2) * yDir * app.unitSize / 2,
            )
        # endregion
        # endregion

        # animate time between tracks
        if self.animationCount < app.stepsPerSecond / app.speedFactor:
            self.animationCount += self.speed
        else:
            # possibly can't change rail when not connected
            if self.changeRail(app.map):
                self.animationCount = 0

    def changeRail(self, map):
        # only can change when next rail is connected to current rail
        if Rail.directionComplement[self.movingTo] not in self.nextRail.directions:
            return False

        # moving from is the opposite of moving to
        self.movingFrom = Rail.directionComplement[self.movingTo]
        # change rail to the next rail
        if self.rail != None:
            self.rail.car = None
        self.rail = self.nextRail
        # moving to is the other direction of this rail
        self.movingTo = (self.rail.directions - {self.movingFrom}).pop()
        # calculate next rail
        self.nextRail = self.calculateNextRail(map)
        self.nextRail.car = self
        return True

    def calculateNextRail(self, map):
        # using moving to to calculate rail
        dif = Rail.directionToDif[self.movingTo]
        curIndices = self.rail.indices
        return map.rails[curIndices[0] + dif[0]][curIndices[1] + dif[1]]
