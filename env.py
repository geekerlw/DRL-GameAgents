import gymnasium as gym
from gymnasium import spaces
import numpy as np
from observation import Numeric
from action import Action
from game import RBRGame

class RBREnv(gym.Env):
    def __init__(self):
        super(RBREnv, self).__init__()
        self.game = RBRGame()
        self.numeric = Numeric(self.game)
        self.action = Action()
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.numeric.dementions(),), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(self.action.dimentions(),), dtype=np.float32)

    def reset(self):
        return self.numeric.take(), {}

    def step(self, action):
        self.action.execute(action)
        # FIXME: maybe need some delay to wait game state update
        return self.numeric.take(), self.reward(), self.done(), self.truncated(), {}
    
    def done(self):
        if self.game.overfinish:
            print("well done, normal finished game.")
            return True
        return False
    
    def truncated(self):
        if self.game.race_failstart():
            print("saddly, race start failed.")

        if self.game.race_wrongway():
            print("saddly, car turn into a wrong way.")
            return True

        if self.game.is_stage_started() and self.game.car_speed() <= 2:
            print("saddly, car maybe stoped.")
            return True

        if self.game.car_temp() >= 130:
            print("saddly, car temp is too high, maybe damaged.")
            return True
    
        return False
    
    def reward(self):
        reward = 1 # step base reward.
        reward -= (self.game.race_time() / 10.0) * 0.1

        return reward