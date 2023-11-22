from cmu_graphics import *
import random


class Rail:
    def __init__(self, app, indices, directions):
        self.width = app.unitX
        self.height = app.unitY
        self.indices = indices
        self.directions = directions

        if random.randrange(2) == 0:
            self.directions.add("top")
            self.directions.add("bottom")
        else:
            self.directions.add("left")
            self.directions.add("right")

    def display(self, app):
        worldPos = self.toWorldPos(app)

        # determine type
        if "top" in self.directions and "bottom" in self.directions:
            type = "Straight"
            angle = 0
        elif "left" in self.directions and "right" in self.directions:
            type = "Straight"
            angle = 90

        drawImage(
            app.imageDict[type],
            worldPos[0],
            worldPos[1],
            width=self.width,
            height=self.height,
            align="center",
            rotateAngle=angle,
        )
        # drawLabel(self.indices,    worldPos[0], worldPos[1])

        # for direction in self.directions:
        #     drawLine(
        #         worldPos[0],
        #         worldPos[1],
        #         worldPos[0] + app.unitX * direction[0],
        #         worldPos[1] + app.unitY * direction[1],
        #     )

    # def createEdge(self):
    #     choices = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    #     choice = choices[random.randrange(len(choices))]

    def toWorldPos(self, app):
        return (
            app.unitX * (self.indices[1] + 0.5),
            app.unitY * (self.indices[0] + 0.5),
        )

    def inBound(indices):
        return (
            indices[0] >= 0
            and indices[0] < len(app.grids)
            and indices[1] >= 0
            and indices[1] < len(app.grids[0])
        )
