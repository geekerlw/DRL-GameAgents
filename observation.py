from driveline import DriveLine
from game import RBRGame
import mss
import numpy
import cv2
import time

class Numeric:
    def __init__(self, game: RBRGame, driveline: DriveLine):
        self.game = game
        self.driveline = driveline

    def reset(self):
        pass

    def dementions(self):
        return 13 + 8

    def take(self) -> list[float]:
        states = []
        states.extend(self.carstate())
        states.extend(self.racestate())
        # print(f"observation state: {states}")
        assert(self.dementions() == len(states))
        return states
    
    def carstate(self) -> list[float]:
        state = []
        state.append(self.game.car_speed())
        state.append(self.game.car_gear())
        state.append(self.game.car_rpm())
        state.extend(self.game.car_look())
        state.extend(self.game.car_spin())
        state.extend(self.game.car_acc())
        return state

    def racestate(self) -> list[float]:
        state = []
        state.extend(self.game.pacenote())
        state.extend(self.game.car_pos())
        _, next = self.driveline.locate_point(self.game.drive_distance())
        state.extend(next[:3])
        return state
    

class Image:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = {"top": 0, "left": 0, "width": 640, "height": 480}
        self.width = 256
        self.height = 256

    def reset(self):
        pass

    def dementions(self):
        return 4
    
    def take(self):
        state = []
        for i in range(self.dementions()):
            img = self.sct.grab(self.monitor)
            frame = numpy.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
            state.append(frame)
            time.sleep(0.02)
        return state