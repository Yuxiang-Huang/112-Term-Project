from cmu_graphics import *


class RailSwitchButton:
    def __init__(self, worldPos, size, type, angle, index):
        self.worldPos = worldPos
        self.size = size
        self.type = type
        self.angle = angle
        self.size = size
        self.index = index

    def display(self, app):
        xCoord = self.worldPos[0]
        yCoord = self.worldPos[1]
        drawOval(
            xCoord,
            yCoord,
            self.size,
            self.size,
            fill="red",
        )
        drawImage(
            app.imageDict[self.type],
            xCoord,
            yCoord,
            width=self.size,
            height=self.size,
            align="center",
            rotateAngle=self.angle,
        )

    def pressed(self, mouseX, mouseY):
        return (
            self.worldPos[0] - self.size / 2
            <= mouseX
            <= self.worldPos[0] + self.size / 2
            and self.worldPos[1] - self.size / 2
            <= mouseY
            <= self.worldPos[1] + self.size / 2
        )
