from cmu_graphics import *
import map as mapFile


class Destination:
    def __init__(self, indices, unitSize, type, relativePos):
        self.indices = indices
        self.size = unitSize / 2
        self.type = type
        self.relativePos = relativePos

    def display(self, app):
        pos = mapFile.Map.toWorldPos(self.indices, app)
        posDif = self.getPosDif()
        drawRect(
            pos[0] + posDif[0],
            pos[1] + posDif[1],
            self.size,
            self.size,
            align="center",
            fill=self.type,
        )

    def getPosDif(self):
        unitDif = self.size
        if self.relativePos == "top":
            return [0, -unitDif]
        elif self.relativePos == "bottom":
            return [0, unitDif]
        elif self.relativePos == "left":
            return [-unitDif, 0]
        elif self.relativePos == "right":
            return [unitDif, 0]
