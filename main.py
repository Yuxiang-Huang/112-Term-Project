from cmu_graphics import *
import imageManager
from map import *
from spawnManager import *


def onAppStart(app):
    imageManager.loadImages(app)

    # setting
    app.stepsPerSecond = 30
    app.speedFactor = 5

    app.directionSort = True
    mapSize = 15
    app.spawnTime = 5
    app.destinationRatio = 3
    app.typeChoices = [
        "purple",
        "blue",
        "green",
    ]  # "purple", "blue", "green", "yellow", "orange", "red"
    app.switchVisualizer = False

    app.points = 0
    app.paused = False
    app.selectedRail = None

    # create map
    app.map = Map(app.typeChoices)
    app.map.createMap(app, mapSize)
    app.spawnManager = SpawnManager(app.map.spawnableRails)


def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill="lightblue")
    displayTopBar(app)
    app.map.display(app)


def displayTopBar(app):
    topBarHeight = app.height - app.width
    drawRect(0, 0, app.width, topBarHeight, fill="darkgreen")
    # points
    drawLabel(
        f"Points: {app.points}",
        app.width / 8,
        topBarHeight / 2,
        size=24,
        fill="white",
    )

    # spawn timer
    drawLabel(
        "Spawn Timer",
        app.width * 3 / 5 - app.width / 50,
        topBarHeight / 2,
        size=24,
        fill="white",
        align="right",
    )
    CDBarlength = app.width * 1.5 / 5
    drawRect(
        app.width * 3 / 5 - app.width / 100,
        topBarHeight / 2,
        CDBarlength,
        topBarHeight * 3 / 5,
        align="left",
    )
    ratio = app.spawnManager.count / app.spawnManager.curTotalSpawnTime
    if ratio > 0:
        drawRect(
            app.width * 3 / 5 - app.width / 100,
            topBarHeight / 2,
            CDBarlength * ratio,
            topBarHeight * 3 / 5,
            fill="green",
            align="left",
        )


def onMousePress(app, mouseX, mouseY, button):
    # change rail or select rail conditions
    if app.selectedRail == None or button != 0:
        app.map.findRail(app, mouseX, mouseY).onPress(app, button)
    else:
        app.selectedRail.checkSwitchButtonPress(app, mouseX, mouseY)


def onKeyPress(app, key):
    if key == "p":
        app.paused = not app.paused
    elif key == "v":
        app.switchVisualizer = not app.switchVisualizer


def onStep(app):
    if app.paused:
        return

    app.spawnManager.takeStep(app)
    app.map.update(app)


def main():
    runApp(700, 750)


main()
