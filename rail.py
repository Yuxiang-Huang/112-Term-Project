from cmu_graphics import *
import random


class Rail:
    def __init__(self, app, indices, directions):
        self.indices = indices
        self.directions = directions
        if randrange(2) == 1:
            self.type = "Straight"
        else:
            self.type = "Turn"
        self.width = app.unitX
        self.height = app.unitY

    def display(self, app):
        worldPos = self.toWorldPos(app)
        drawImage(
            app.imageDict[self.type],
            worldPos[0],
            worldPos[1],
            width=self.width,
            height=self.height,
            align="center",
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
