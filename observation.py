import numpy as np
class Numeric:
    def __init__(self, game):
        self.game = game

    def dementions(self):
        return 8

    def take(self) -> list[float]:
        states = []
        states.extend(self.carstate())
        states.extend(self.racestate())
        print(f"observation state: {states}")
        assert(self.dementions() == len(states))
        if np.isnan(states).all():
            print(f"observations contain Nan: {states}")
        return states
    
    # 6 dementions
    def carstate(self) -> list[float]:
        state = []
        state.append(self.game.car_speed())
        state.append(self.game.car_rpm())
        state.extend(self.game.car_look())
        if np.isnan(state).all():
            print(f"observations carstate contain Nan: {state}")
        return state

    # 2 dementions
    def racestate(self) -> list[float]:
        state = []
        state.extend(self.game.pacenote())
        if np.isnan(state).all():
            print(f"observations racestate contain Nan: {state}")
        return state