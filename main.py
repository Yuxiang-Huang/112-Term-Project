from cmu_graphics import *
import imageManager
from map import *
from spawnManager import *


def onAppStart(app):
    imageManager.loadImages(app)

    # setting
    app.paused = False
    app.directionSort = True
    mapSize = 15
    app.spawnTime = 100

    app.map = Map(Map.allTypes)
    spawnableRails = app.map.createMap(app, mapSize)
    app.spawnManager = SpawnManager(spawnableRails)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    app.map.display(app)


def onMousePress(app, mouseX, mouseY):
    app.map.findRail(app, mouseX, mouseY).onPress()


def onStep(app):
    if app.paused:
        return

    app.spawnManager.takeStep(app)


def main():
    runApp(750, 750)


main()
