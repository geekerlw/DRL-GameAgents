from game import RBRGame

class Observation:
    def __init__(self):
        self.game = RBRGame()

    def dementions(self):
        state = self.take()
        return len(state)

    def take(self) -> list[float]:
        states = []
        states.extend(self.carstate())
        states.extend(self.racestate())
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
        state.append(self.game.drive_distance())
        return state
    
if __name__ == '__main__':
    print("test observation")
    observation = Observation()
    print(observation.dementions())
    print(observation.take())