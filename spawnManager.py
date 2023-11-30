from car import *
import random


class SpawnManager:
    def __init__(self, spawnableRails):
        self.count = 10000  # 0
        self.spawnableRails = spawnableRails

    def takeStep(self, app):
        # spawn every spawn time
        self.count += 1
        # immediately spawn a car if there is no car
        if len(app.map.allCars) == 0:
            app.spawnManager.spawn(app)
            self.count = 0

        elif self.calculateSpawnTimeLeft() < 0:
            self.spawn(app)
            self.count = 0

    def spawn(self, app):
        # randomly choose spawnable rail and car to spawn on
        spawnRail = random.choice(self.spawnableRails)
        spawnType = random.choice(app.map.allTypes)
        # create car and add to the list of all cars
        spawnCar = Car(app, spawnType, spawnRail)
        app.map.allCars.append(spawnCar)

    def calculateSpawnTimeLeft(self):
        # current spawn time will decrease as points increase with a minimum
        return (
            app.stepsPerSecond
            * max(app.spawnTime / 5, app.spawnTime - app.points / 500)
            - self.count
        )
