from car import *
import random


class SpawnManager:
    def __init__(self, spawnableRails):
        self.count = 100  # 0
        self.spawnableRails = spawnableRails

    def takeStep(self, app):
        self.count += 1
        # spawn every how many second?
        if self.count >= app.stepsPerSecond:
            self.count = 0
            self.spawn(app)

    def spawn(self, app):
        spawnRail = random.choice(self.spawnableRails)
        spawnType = random.choice(app.map.allTypes)
        spawnCar = Car(app, spawnType, spawnRail)
        spawnRail.car = spawnCar
        app.map.allCars.append(spawnCar)
