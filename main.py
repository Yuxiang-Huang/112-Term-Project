from cmu_graphics import *
import imageManager
from rail import *


def onAppStart(app):
    imageManager.loadImages(app)

    mapSize = 15
    app.grids = [[0] * mapSize for _ in range(mapSize)]
    app.unitX = app.width / mapSize
    app.unitY = app.height / mapSize

    # app.pSplit = 0.5

    for i in range(len(app.grids)):
        for j in range(len(app.grids[0])):
            app.grids[i][j] = Rail(app, (i, j), [])

    # app.grids[0][0].createEdge(app)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightgreen")
    for i in range(len(app.grids)):
        for j in range(len(app.grids[0])):
            app.grids[i][j].display(app)


def main():
    runApp(800, 800)


main()
