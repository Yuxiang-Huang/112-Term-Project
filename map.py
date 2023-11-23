import rail as railFile
import math
import random


class Map:
    probOfStraight = 0.1
    probOfConnect = 0  # 0.05

    # def __init__(self):
    #     pass

    def createMap(self, app, mapSize):
        # initlizations
        self.rails = [[None] * mapSize for _ in range(mapSize)]
        app.unitX = app.width / mapSize
        app.unitY = app.height / mapSize

        self.spawnableRails = []

        # start with the  most middle left rail
        self.rails[mapSize // 2][0] = railFile.Rail(app, (mapSize // 2, 0), set())

        # flood fill to create map
        self.rails[mapSize // 2][0].floodFill(app, "right")

        # make sure this each side has a spawnable rail
        self.rails[mapSize // 2][0].outOfBoundConnection(app, mapSize // 2, -1)
        randomIndex = random.randint(0, mapSize - 1)
        self.rails[randomIndex][-1].outOfBoundConnection(app, randomIndex, mapSize)
        randomIndex = random.randint(0, mapSize - 1)
        self.rails[0][randomIndex].outOfBoundConnection(app, -1, randomIndex)
        randomIndex = random.randint(0, mapSize - 1)
        self.rails[-1][randomIndex].outOfBoundConnection(app, mapSize, randomIndex)

        # finalize
        for rowList in self.rails:
            for rail in rowList:
                rail.fixOneDirectionRail(app)

        for rowList in self.rails:
            for rail in rowList:
                rail.createAllDirections()

    def display(self, app):
        for rowList in self.rails:
            for curRail in rowList:
                curRail.display(app)

    def findRail(self, app, mouseX, mouseY):
        return self.rails[math.floor(mouseY / app.unitY)][
            math.floor(mouseX / app.unitX)
        ]
