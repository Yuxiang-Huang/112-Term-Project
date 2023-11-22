from cmu_graphics import *
import imageManager
from rail import *


def onAppStart(app):
    imageManager.loadImages(app)

    mapSize = 15
    app.grids = [[None] * mapSize for _ in range(mapSize)]
    app.unitX = app.width / mapSize
    app.unitY = app.height / mapSize

    app.probOfStraight = 0.5
    app.probOfConnect = 0.0  # 5

    # for i in range(len(app.grids)):
    #     for j in range(len(app.grids[0])):
    #         app.grids[i][j] = Rail(app, (i, j), set())

    app.grids[mapSize // 2][0] = Rail(app, (mapSize // 2, 0), set())

    # make sure this starting rail will have a left direction
    app.grids[mapSize // 2][0].directions.add("left")

    # flood fill to create map
    app.grids[mapSize // 2][0].floodFill(app, "right")


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    for i in range(len(app.grids)):
        for j in range(len(app.grids[0])):
            # if app.grids[i][j] != None:
            print(app.grids[i][j].directions)
            app.grids[i][j].display(app)


def main():
    runApp(800, 800)


main()
