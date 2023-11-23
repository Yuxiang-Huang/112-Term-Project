from cmu_graphics import *
import imageManager
from map import *


def onAppStart(app):
    imageManager.loadImages(app)

    # setting
    app.directionSort = True
    mapSize = 15

    app.map = Map()
    app.map.createMap(app, mapSize)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    app.map.display(app)


def onMousePress(app, mouseX, mouseY):
    app.map.findRail(app, mouseX, mouseY).onPress()


def main():
    runApp(750, 750)


main()
