from cmu_graphics import *
import map as mapFile
from destination import *
import random


class Rail:
    difToDirection = {
        (-1, 0): "top",
        (1, 0): "bottom",
        (0, -1): "left",
        (0, 1): "right",
    }
    directionToDif = {
        "top": (-1, 0),
        "bottom": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    directionComplement = {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left",
    }

    def __init__(self, app, indices, directions):
        self.size = app.unitSize
        self.indices = indices
        self.directions = directions
        self.spawnCarDirection = None
        self.car = None
        self.destinationList = []

    def __repr__(self):
        return f"Pos: {self.indices}, Dir: {self.allDirections}"

    def display(self, app):
        # if len(self.directions) == 1:
        #     return

        worldPos = mapFile.Map.toWorldPos(self.indices, app)

        # determine rail display dependo on connections
        if "top" in self.directions and "bottom" in self.directions:
            type = "Straight"
            angle = 0
        elif "left" in self.directions and "right" in self.directions:
            type = "Straight"
            angle = 90
        elif "top" in self.directions and "left" in self.directions:
            type = "Turn"
            angle = 90
        elif "top" in self.directions and "right" in self.directions:
            type = "Turn"
            angle = 180
        elif "bottom" in self.directions and "left" in self.directions:
            type = "Turn"
            angle = 0
        elif "bottom" in self.directions and "right" in self.directions:
            type = "Turn"
            angle = 270

        # special case for clickable rails
        if len(self.allDirections) > 1:
            drawOval(
                worldPos[0],
                worldPos[1],
                self.size,
                self.size,
                fill="lightyellow",
            )

        drawImage(
            app.imageDict[type],
            worldPos[0],
            worldPos[1],
            width=self.size,
            height=self.size,
            align="center",
            rotateAngle=angle,
        )
        # drawLabel(self.indices, worldPos[0], worldPos[1])

    def onPress(self, button):
        if len(self.allDirections) > 1 and self.car == None:
            if button == 0:
                self.dirIndex += 1
            else:
                self.dirIndex -= 1
            self.dirIndex %= len(self.allDirections)
            self.directions = self.allDirections[self.dirIndex]

    # region rail generation
    def floodFill(self, app, prevDirection):
        # bias to move straight
        if random.random() < mapFile.Map.probOfStraight:
            dif = Rail.directionToDif[prevDirection]
            self.connect(app, dif)

        # try all directions in random order
        choices = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(choices)
        for dif in choices:
            self.connect(app, dif)

    def connect(self, app, dif):
        row = self.indices[0] + dif[0]
        col = self.indices[1] + dif[1]

        # out of bound cases
        if not mapFile.Map.inBound(app.map, (row, col)):
            return

        # if never visited
        if app.map.rails[row][col] == None:
            # create new rail
            app.map.rails[row][col] = Rail(app, (row, col), set())
            # connect to this rail to ensure that all rails are connected
            self.connectToRail(app.map.rails[row][col], dif)
            # flood fill the rest of the map
            app.map.rails[row][col].floodFill(app, Rail.difToDirection[dif])

        # determine using probability of connection if to connect to this rail)
        if random.random() < mapFile.Map.probOfConnect:
            self.connectToRail(app.map.rails[row][col], dif)

    def connectToRail(self, other, dif):
        # connect the two rails together using dif
        self.directions.add(Rail.difToDirection[dif])
        other.directions.add(Rail.directionComplement[Rail.difToDirection[dif]])

    def fixOneDirectionRail(self, app, spawnableRails):
        # connect to complement if only has one direction
        if len(self.directions) == 1:
            dif = Rail.directionToDif[Rail.directionComplement[min(self.directions)]]
            otherIndices = (self.indices[0] + dif[0], self.indices[1] + dif[1])
            # in bound and out of bound cases
            if mapFile.Map.inBound(app.map, otherIndices):
                other = app.map.rails[otherIndices[0]][otherIndices[1]]
                self.connectToRail(other, dif)
            else:
                self.outOfBoundConnection(
                    self.indices[0] + dif[0], self.indices[1] + dif[1], spawnableRails
                )

    def createAllDirections(self):
        # create all directions
        if len(self.directions) == 2:
            curDirectionList = list(self.directions)
            self.allDirections = [{curDirectionList[0], curDirectionList[1]}]
        else:
            self.allDirections = []
            # hard coded to be sorted...
            if app.directionSort:
                if "top" in self.directions and "bottom" in self.directions:
                    self.allDirections.append({"top", "bottom"})
                if "left" in self.directions and "right" in self.directions:
                    self.allDirections.append({"left", "right"})
                if "top" in self.directions and "left" in self.directions:
                    self.allDirections.append({"top", "left"})
                if "top" in self.directions and "right" in self.directions:
                    self.allDirections.append({"top", "right"})
                if "bottom" in self.directions and "right" in self.directions:
                    self.allDirections.append({"bottom", "right"})
                if "bottom" in self.directions and "left" in self.directions:
                    self.allDirections.append({"bottom", "left"})
            else:
                # random directions
                for dir1 in self.directions:
                    for dir2 in self.directions:
                        curDir = {dir1, dir2}
                        # check for duplicates
                        if len(curDir) == 2 and curDir not in self.allDirections:
                            self.allDirections.append(curDir)

            # make sure spawnable rails stays spawnable
            if self.spawnCarDirection != None:
                index = len(self.allDirections) - 1
                while index >= 0:
                    curDirection = self.allDirections[index]
                    if self.spawnCarDirection not in curDirection:
                        self.allDirections.remove(curDirection)
                    index -= 1

        # set direction for rail
        self.dirIndex = 0
        self.directions = self.allDirections[self.dirIndex]

    def outOfBoundConnection(self, row, col, spawnableRails):
        if row < 0:
            self.directions.add("top")
            self.spawnCarDirection = "top"
            spawnableRails.append(self)
        elif row >= len(app.map.rails):
            self.directions.add("bottom")
            self.spawnCarDirection = "bottom"
            spawnableRails.append(self)
        if col < 0:
            self.directions.add("left")
            self.spawnCarDirection = "left"
            spawnableRails.append(self)
        elif col >= len(app.map.rails[0]):
            self.directions.add("right")
            self.spawnCarDirection = "right"
            spawnableRails.append(self)

    # endregion

    # region destination generation
    def createDestination(self, map, type, unitSize):
        # can't be switchable
        if len(self.allDirections) > 1:
            return False

        # need to be straight
        directionList = list(self.directions)
        if directionList[0] != Rail.directionComplement[directionList[1]]:
            return False

        # not too close with other destinations
        if self.tooClose(map.allDestinations):
            return False

        # determine relative positive
        if "top" in self.directions:
            relativePositions = ["left", "right"]
        if "right" in self.directions:
            relativePositions = ["top", "bottom"]

        # random relative position
        random.shuffle(relativePositions)

        # try each relative position
        for relativePos in relativePositions:
            neighborRail = self.neighborRail(map, relativePos)
            if self.checkNeighborForDestination(neighborRail, relativePos):
                newDestination = Destination(
                    (self.indices[0], self.indices[1]), unitSize, type, relativePos
                )
                # add to destination list of both rails
                self.destinationList.append(newDestination)
                neighborRail.destinationList.append(newDestination)
                return True

        # return False if both direction doesn't work
        return False

    def checkNeighborForDestination(self, neighborRail, relativePos):
        # edge rails are not valid
        if neighborRail == None:
            return False

        # can't already have a destination in the same way
        if len(neighborRail.destinationList) == 2:
            return False
        elif len(neighborRail.destinationList) == 1:
            if neighborRail.destinationList[0] == Rail.directionComplement[relativePos]:
                return False

        # can't be switchable
        if len(neighborRail.allDirections) > 1:
            return False

        # need to be straight in the same way
        if self.directions != neighborRail.directions:
            return False

        return True

    def tooClose(self, allDestinations):
        # check all destinations
        for destination in allDestinations:
            # check if it is less thatn the minimum difference
            dif = abs(destination.indices[0] - self.indices[0]) + abs(
                destination.indices[1] - self.indices[1]
            )
            if dif < mapFile.Map.minDifBtwDestination:
                return True
        return False

    def neighborRail(self, map, direction):
        dif = Rail.directionToDif[direction]
        newIndices = (self.indices[0] + dif[0], self.indices[1] + dif[1])
        if mapFile.Map.inBound(map, newIndices):
            return map.rails[newIndices[0]][newIndices[1]]

    # endregion
