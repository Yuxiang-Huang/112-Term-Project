import rail as railFile
import math
import random


class Map:
    probOfStraight = 0.1
    probOfConnect = 0  # 0.05

    minDifBtwDestination = None

    allTypes = ["red", "green", "blue", "purple", "yellow", "orange"]

    def __init__(self, allTypes):
        self.allTypes = allTypes
        self.allCars = []
        self.allDestinations = []

    def createMap(self, app, mapSize):
        # initlizations
        self.rails = [[None] * mapSize for _ in range(mapSize)]
        app.unitSize = app.width / mapSize

        Map.minDifBtwDestination = mapSize // len(self.allTypes) // app.destinationRatio

        # create rails
        self.spawnableRails = []

        # start with the most left center rail
        self.rails[mapSize // 2][0] = railFile.Rail(app, (mapSize // 2, 0), set())

        # flood fill to create map
        self.rails[mapSize // 2][0].floodFill(app, "right")

        # make sure this each side has a spawnable rail
        self.rails[mapSize // 2][0].outOfBoundConnection(
            mapSize // 2, -1, self.spawnableRails
        )

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[randomIndex][-1].outOfBoundConnection(
            randomIndex, mapSize, self.spawnableRails
        )

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[0][randomIndex].outOfBoundConnection(
            -1, randomIndex, self.spawnableRails
        )

        randomIndex = random.randint(0, mapSize - 1)
        self.rails[-1][randomIndex].outOfBoundConnection(
            mapSize, randomIndex, self.spawnableRails
        )

        # finalize rails
        for rowList in self.rails:
            for rail in rowList:
                rail.fixOneDirectionRail(app, self.spawnableRails)
        for rowList in self.rails:
            for rail in rowList:
                rail.createAllDirections()

        # create destinations
        self.createDestinations(app, mapSize)

    def display(self, app):
        for rowList in self.rails:
            for curRail in rowList:
                curRail.display(app)
        for car in self.allCars:
            car.move(app)
            car.display()
        for destination in self.allDestinations:
            destination.display(app)

    def findRail(self, app, mouseX, mouseY):
        return self.rails[math.floor(mouseY / app.unitSize)][
            math.floor(mouseX / app.unitSize)
        ]

    def createDestinations(self, app, mapSize):
        # for each type
        for type in self.allTypes:
            usedIndices = []
            # create app.destinationRatio many destinations for this type
            for _ in range(app.destinationRatio):
                # keep trying random locations
                randomRow = random.randint(0, mapSize - 1)
                randomCol = random.randint(0, mapSize - 1)
                curRail = self.rails[randomRow][randomCol]
                while not curRail.createDestination(
                    self, type, app.unitSize, usedIndices
                ):
                    randomRow = random.randint(0, mapSize - 1)
                    randomCol = random.randint(0, mapSize - 1)
                    curRail = self.rails[randomRow][randomCol]
                self.allDestinations.extend(curRail.destination)
                usedIndices.append((randomRow, randomCol))

    # region helper functions
    @staticmethod
    def toWorldPos(indices, app):
        return (
            app.unitSize * (indices[1] + 0.5),
            app.unitSize * (indices[0] + 0.5),
        )

    @staticmethod
    def inBound(map, indices):
        return (
            indices[0] >= 0
            and indices[0] < len(map.rails)
            and indices[1] >= 0
            and indices[1] < len(map.rails[0])
        )

    # endregion
