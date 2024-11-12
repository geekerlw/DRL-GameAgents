import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from observation import Numeric
from action import Action
from game import RBRGame

class RBREnv(gym.Env):
    def __init__(self, shakedown=False):
        super(RBREnv, self).__init__()
        self.shakedown = shakedown
        self.game = RBRGame()
        self.numeric = Numeric(self.game)
        self.action = Action()
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.numeric.dementions(),), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(self.action.dimentions(),), dtype=np.float32)

    def restart_game(self):
        while not self.game.attach():
            print("can't attach game process, please start game.")
            time.sleep(3)

        if self.game.is_stage_started():
            print("restart game.")
            self.game.restart()

        while not self.game.is_stage_loaded():
            print("stage is not loaded, select a stage to start.")
            time.sleep(2)

        self.game.start()
        while not self.game.is_stage_started():      
            time.sleep(0.2)

    def reset(self, seed=None):
        self.action.reset()
        self.restart_game()
        return self.numeric.take(), {}

    def step(self, action):
        print("take action: " + action)
        self.action.execute(action)
        time.sleep(0.1) # need some delay to wait game state update
        return self.numeric.take(), self.reward(), self.done(), self.truncated(), {}
    
    def done(self):
        if self.shakedown:
            if self.game.oversplitone():
                print("well done, shakedown over.")
                return True
        else:
            if self.game.overfinish():
                print("well done, race over.")
                return True
        return False
    
    def truncated(self):
        if self.game.startcount() > 5: # make sure racing over 5 seconds.
            return False

        if self.game.race_failstart():
            print("saddly, race start failed.")
            return True

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
        if self.game.car_rpm() < 1500 or self.game.car_rpm() > 6500:
            reward -= 1
        reward += (self.game.car_speed() / 20.0) * 0.1

        return reward