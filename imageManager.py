from cmu_graphics import *
from PIL import Image

# Image Source: https://www.vectorstock.com/royalty-free-vector/railway-structural-elements-top-view-railroad-vector-16043195


def loadImages(app):
    # Load the PIL image
    app.imageDict = {
        "Straight": "Images/StraightRail.png",
        "Turn": "Images/TurnRail.png",
    }

    for imgName in app.imageDict:
        fileName = app.imageDict[imgName]
        app.imageDict[imgName] = CMUImage(Image.open(fileName))
