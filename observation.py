class Numeric:
    def __init__(self, game):
        self.game = game

    def dementions(self):
        return 21

    def take(self) -> list[float]:
        states = []
        states.extend(self.carstate())
        states.extend(self.racestate())
        assert(self.dementions() == len(states))
        return states
    
    # 18 dementions
    def carstate(self) -> list[float]:
        state = []
        state.append(self.game.car_speed())
        state.append(self.game.car_rpm())
        state.append(self.game.car_temp())
        state.append(self.game.car_turbo())
        state.extend(self.game.car_look())
        state.extend(self.game.car_pos())
        state.extend(self.game.car_spin())
        state.extend(self.game.car_acc())
        return state

    # 3 dementions
    def racestate(self) -> list[float]:
        state = []
        state.append(self.game.startcount())
        state.extend(self.game.pacenote())
        return state