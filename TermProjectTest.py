from cmu_graphics import *
import random


class Node:
    def __init__(self, indices, directions):
        self.indices = indices
        self.directions = directions

    def display(self, app):
        worldPos = self.toWorldPos(app)
        drawLabel(self.indices, worldPos[0], worldPos[1])
        for direction in self.directions:
            drawLine(
                worldPos[0],
                worldPos[1],
                worldPos[0] + app.unitX * direction[0],
                worldPos[1] + app.unitY * direction[1],
            )

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


def onAppStart(app):
    app.grids = [[0] * 10 for _ in range(10)]
    app.unitX = app.width / 10
    app.unitY = app.height / 10

    # app.pSplit = 0.5

    for i in range(len(app.grids)):
        for j in range(len(app.grids[0])):
            app.grids[i][j] = Node((i, j), [])

    # app.grids[0][0].createEdge(app)


def redrawAll(app):
    for i in range(len(app.grids)):
        for j in range(len(app.grids[0])):
            app.grids[i][j].display(app)


def main():
    runApp(800, 800)


main()
