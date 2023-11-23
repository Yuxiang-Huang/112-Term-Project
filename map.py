import rail as railFile
import math
import random


class Map:
    probOfStraight = 0.1
    probOfConnect = 0  # 0.05

    allTypes = ["red", "green", "blue", "purple", "yellow", "orange"]

    def __init__(self, allTypes):
        self.allTypes = allTypes
        self.allCars = []

    def createMap(self, app, mapSize):
        # initlizations
        self.rails = [[None] * mapSize for _ in range(mapSize)]
        app.unitSize = app.width / mapSize

        spawnableRails = []

        # start with the most left center rail
        self.rails[mapSize // 2][0] = railFile.Rail(app, (mapSize // 2, 0), set())

        # flood fill to create map
        self.rails[mapSize // 2][0].floodFill(app, "right")

        # make sure this each side has a spawnable rail
        self.rails[mapSize // 2][0].outOfBoundConnection(
            mapSize // 2, -1, spawnableRails
        )

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[randomIndex][-1].outOfBoundConnection(
            randomIndex, mapSize, spawnableRails
        )

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[0][randomIndex].outOfBoundConnection(-1, randomIndex, spawnableRails)

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[-1][randomIndex].outOfBoundConnection(
            mapSize, randomIndex, spawnableRails
        )

        # finalize
        for rowList in self.rails:
            for rail in rowList:
                rail.fixOneDirectionRail(app, spawnableRails)
        for rowList in self.rails:
            for rail in rowList:
                rail.createAllDirections()

        return spawnableRails

    def display(self, app):
        for rowList in self.rails:
            for curRail in rowList:
                curRail.display(app)
        for car in self.allCars:
            car.move(app)
            car.display()

    def findRail(self, app, mouseX, mouseY):
        return self.rails[math.floor(mouseY / app.unitSize)][
            math.floor(mouseX / app.unitSize)
        ]
