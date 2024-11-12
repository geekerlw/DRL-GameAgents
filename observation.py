class Numeric:
    def __init__(self, game):
        self.game = game

    def dementions(self):
        return 20

    def take(self) -> list[float]:
        states = []
        states.extend(self.carstate())
        states.extend(self.racestate())
        assert(self.dementions() == len(states))
        return states
    
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

    def racestate(self) -> list[float]:
        state = []
        state.append(self.game.startcount())
        state.append(self.game.drive_distance())
        # state.extend(self.game.pacenote())
        return state