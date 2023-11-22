import rail as railFile


class Map:
    probOfStraight = 0.25
    probOfConnect = 0  # 0.05

    # def __init__(self):
    #     pass

    def createMap(self, app, mapSize):
        # initlizations
        self.rails = [[None] * mapSize for _ in range(mapSize)]
        app.unitX = app.width / mapSize
        app.unitY = app.height / mapSize

        # start with the  most middle left rail
        self.rails[mapSize // 2][0] = railFile.Rail(app, (mapSize // 2, 0), set())

        # make sure this starting rail will have a left direction
        self.rails[mapSize // 2][0].directions.add("left")

        # flood fill to create map
        self.rails[mapSize // 2][0].floodFill(app, "right")

        # optimization process
        for rowList in self.rails:
            for rail in rowList:
                rail.optimize(app)
