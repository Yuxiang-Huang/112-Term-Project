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

    def display(self, app):
        if len(self.directions) == 1:
            return

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

        if len(self.directions) > 2:
            type = "Multi"
            angle = 0

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

    def floodFill(self, app, prevDirection):
        choices = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        random.shuffle(choices)

        if random.random() < map.Map.probOfStraight:
            dif = Rail.directionToDif[prevDirection]
            self.connect(app, dif)

        for dif in choices:
            self.connect(app, dif)

    def connect(self, app, dif):
        row = self.indices[0] + dif[0]
        col = self.indices[1] + dif[1]

        # out of bound cases
        if row < 0:
            self.directions.add("left")
            return
        elif row >= len(app.map.rails):
            self.directions.add("right")
            return
        if col < 0:
            self.directions.add("top")
            return
        elif col >= len(app.map.rails[0]):
            self.directions.add("bottom")
            return

        # inbound case
        neverVisited = app.map.rails[row][col] == None

        # create new rail if not created
        if neverVisited:
            app.map.rails[row][col] = Rail(app, (row, col), set())

        # determine if need to connect to this rail
        # (always connect to newly created one to ensure all rails are connected
        # otherwise determine using probability of connection in app)
        if neverVisited or random.random() < map.Map.probOfConnect:
            self.connectToRail(app.map.rails[row][col], dif)

        # only flood fill if never visited
        if neverVisited:
            app.map.rails[row][col].floodFill(app, Rail.difToDirection[dif])

    def connectToRail(self, other, dif):
        # connect the two rails together using dif
        self.directions.add(Rail.difToDirection[dif])
        other.directions.add(Rail.directionComplement[Rail.difToDirection[dif]])

    def optimize(self, app):
        # connect to complement if only has one direction
        if len(self.directions) == 1:
            dif = Rail.directionToDif[Rail.directionComplement[min(self.directions)]]
            other = app.map.rails[self.indices[0] + dif[0]][self.indices[1] + dif[1]]
            self.connectToRail(other, dif)

    def toWorldPos(self, app):
        return (
            app.unitX * (self.indices[1] + 0.5),
            app.unitY * (self.indices[0] + 0.5),
        )

    # @staticmethod
    # def inBound(app, indices):
    #     return (
    #         indices[0] >= 0
    #         and indices[0] < len(app.map.rails)
    #         and indices[1] >= 0
    #         and indices[1] < len(app.map.rails[0])
    #     )
