from car import *
import random


class SpawnManager:
    def __init__(self, spawnableRails):
        self.count = 10000  # 0
        self.spawnableRails = spawnableRails

    def takeStep(self, app):
        # spawn every spawn time
        self.count += 1
        if self.count >= app.stepsPerSecond * app.spawnTime:
            self.spawn(app)
            self.count = 0

    def spawn(self, app):
        # randomly choose spawnable rail and car to spawn on
        spawnRail = random.choice(self.spawnableRails)
        spawnType = random.choice(app.map.allTypes)
        # create car and add to the list of all cars
        spawnCar = Car(app, spawnType, spawnRail)
        app.map.allCars.append(spawnCar)
