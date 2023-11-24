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
        self.movingTo = Rail.directionComplement[spawnRail.spawnCarDirection]
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
        # turn cases
        else:
            # hard coded conditions for circular motion...
            if self.movingFrom == "left" and self.movingTo == "top":
                dx = -app.unitSize / 2
                dy = -app.unitSize / 2
                theta = math.pi * 3 / 2
            elif self.movingFrom == "top" and self.movingTo == "left":
                dx = -app.unitSize / 2
                dy = -app.unitSize / 2
                theta = 0
                ratio *= -1

            elif self.movingFrom == "right" and self.movingTo == "top":
                dx = app.unitSize / 2
                dy = -app.unitSize / 2
                theta = math.pi * 3 / 2
                ratio *= -1
            elif self.movingFrom == "top" and self.movingTo == "right":
                dx = app.unitSize / 2
                dy = -app.unitSize / 2
                theta = math.pi

            elif self.movingFrom == "left" and self.movingTo == "bottom":
                dx = -app.unitSize / 2
                dy = app.unitSize / 2
                theta = math.pi / 2
                ratio *= -1
            elif self.movingFrom == "bottom" and self.movingTo == "left":
                dx = -app.unitSize / 2
                dy = app.unitSize / 2
                theta = 0

            elif self.movingFrom == "right" and self.movingTo == "bottom":
                dx = app.unitSize / 2
                dy = app.unitSize / 2
                theta = math.pi / 2
            elif self.movingFrom == "bottom" and self.movingTo == "right":
                dx = app.unitSize / 2
                dy = app.unitSize / 2
                theta = math.pi
                ratio *= -1

            self.pos = (
                railPos[0]
                + dx
                + math.cos(theta + ratio * math.pi / 2) * app.unitSize / 2,
                railPos[1]
                + dy
                - math.sin(theta + ratio * math.pi / 2) * app.unitSize / 2,
            )
        # endregion

        # animate time between tracks
        self.animationCount += self.speed
        if self.animationCount > app.stepsPerSecond / app.speedFactor:
            # possibly can't change rail when not connected
            if self.changeRail(app.map):
                self.animationCount -= app.stepsPerSecond / app.speedFactor
            else:
                self.animationCount = app.stepsPerSecond / app.speedFactor

    def changeRail(self, map):
        # if out of bound then teleport this car to a random spawnable rail
        if self.nextRail == None:
            self.nextRail = random.choice(map.spawnableRails)
            self.movingTo = Rail.directionComplement[self.nextRail.spawnCarDirection]
        else:
            # only can change when next rail is connected to current rail
            if Rail.directionComplement[self.movingTo] not in self.nextRail.directions:
                return False

        # moving from is the opposite of moving to
        self.movingFrom = Rail.directionComplement[self.movingTo]
        # change rail to the next rail
        if self.rail != None:
            self.rail.car = None
        self.rail = self.nextRail
        self.rail.car = self
        # moving to is the other direction of this rail
        self.movingTo = (self.rail.directions - {self.movingFrom}).pop()
        # calculate next rail
        self.nextRail = self.calculateNextRail(map)
        return True

    def calculateNextRail(self, map):
        # using moving to to calculate rail
        dif = Rail.directionToDif[self.movingTo]
        curIndices = self.rail.indices
        curIndices = (curIndices[0] + dif[0], curIndices[1] + dif[1])

        # check for out of bound
        if Rail.inBound(map, curIndices):
            return map.rails[curIndices[0]][curIndices[1]]
        else:
            return None
