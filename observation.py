from driveline import DriveLine
from game import RBRGame

class Numeric:
    def __init__(self, game: RBRGame, driveline: DriveLine):
        self.game = game
        self.driveline = driveline

    def reset(self):
        pass

    def dementions(self):
        return 8 + 8

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
        state.append(self.game.car_rpm())
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