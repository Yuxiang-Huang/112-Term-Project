from cmu_graphics import *
import imageManager
from map import *


def onAppStart(app):
    imageManager.loadImages(app)

    mapSize = 15
    app.map = Map()
    app.map.createMap(app, mapSize)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    for rowList in app.map.rails:
        for rail in rowList:
            # if rail != None:
            # print(rail.directions)
            rail.display(app)


def onMousePress(app, mouseX, mouseY):
    pass


def main():
    runApp(800, 800)


main()
