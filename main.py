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
    app.spawnTime = 5
    app.speedFactor = 5
    app.destinationRatio = 3

    app.points = 0

    app.map = Map(["blue", "green", "yellow"])
    app.map.createMap(app, mapSize)
    app.spawnManager = SpawnManager(app.map.spawnableRails)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")

    # top bar display
    topBarHeight = app.height - app.width
    drawRect(0, 0, app.width, topBarHeight)
    drawLabel(
        f"Points: {app.points}", app.width / 2, topBarHeight / 2, size=24, fill="white"
    )

    app.map.display(app)


def onMousePress(app, mouseX, mouseY, button):
    app.map.findRail(app, mouseX, mouseY).onPress(button)


def onStep(app):
    if app.paused:
        return

    app.spawnManager.takeStep(app)
    app.map.update(app)


def main():
    runApp(700, 750)


main()
