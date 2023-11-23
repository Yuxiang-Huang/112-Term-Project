from cmu_graphics import *
import random
import map


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
        self.width = app.unitX
        self.height = app.unitY
        self.indices = indices
        self.directions = directions
        self.spawnCarDirection = None

    def __repr__(self):
        return f"Pos: {self.indices}, Dir: {self.allDirections}"

    def display(self, app):
        # if len(self.directions) == 1:
        #     return

        worldPos = self.toWorldPos(app)

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
                self.width,
                self.height,
                fill="lightyellow",
            )

        drawImage(
            app.imageDict[type],
            worldPos[0],
            worldPos[1],
            width=self.width,
            height=self.height,
            align="center",
            rotateAngle=angle,
        )
        # drawLabel(self.indices, worldPos[0], worldPos[1])

    def onPress(self):
        if len(self.allDirections) > 1:
            self.dirIndex = (self.dirIndex + 1) % len(self.allDirections)
            self.directions = self.allDirections[self.dirIndex]

    # region map generation
    def floodFill(self, app, prevDirection):
        # bias to move straight
        if random.random() < map.Map.probOfStraight:
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
        if not Rail.inBound(app, (row, col)):
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
        if random.random() < map.Map.probOfConnect:
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
            if Rail.inBound(app, otherIndices):
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

    # region helper functions
    def toWorldPos(self, app):
        return (
            app.unitX * (self.indices[1] + 0.5),
            app.unitY * (self.indices[0] + 0.5),
        )

    @staticmethod
    def inBound(app, indices):
        return (
            indices[0] >= 0
            and indices[0] < len(app.map.rails)
            and indices[1] >= 0
            and indices[1] < len(app.map.rails[0])
        )

    # endregion
