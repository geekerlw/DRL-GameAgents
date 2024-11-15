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
        self.total_rewards = 0
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
            self.action.start()

        while not self.game.is_stage_loaded():
            print("stage is not loaded, select a stage to start.")
            time.sleep(2)

        self.game.load_pacenotes()
        while not self.game.is_stage_started():
            time.sleep(0.2)

    def reset(self, seed=None):
        self.total_rewards = 0
        self.game.reset()
        self.action.reset()
        self.restart_game()
        return self.numeric.take(), {}

    def step(self, action):
        self.game.step()
        self.action.execute(action)
        time.sleep(0.2) # need some delay to wait game state update
        reward = self.reward()
        self.total_rewards += reward
        print(f"take action: {action}, got reward: {reward}, total: {self.total_rewards}")
        return self.numeric.take(), reward, self.done(), self.truncated(), {}
    
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
        if self.game.car_temp() >= 130:
            print("saddly, car temp is too high, maybe damaged.")
            return True
        
        if self.total_rewards < -1000:
            print("saddly, too many mistakes, need to restart.")
            return True
    
        return False
    
    def reward(self):
        reward = 0
        reward -= 1 # step base reward, more step means more time and less reward.
        if self.game.last_distance > self.game.travel_distance(): # back way detected
            reward -= 1

        if self.game.race_wrongway(): # wrong way.
            reward -= 1

        if self.game.is_stage_started() and self.game.car_speed() == 0.0: # car stoped.
            reward -= 1

        throttle, brake, handbrake, _= self.game.car_control()
        reward -= (1.0 - throttle) / 1.0 # more throttle more score.
        reward -= 1.0 - (brake - 1.0) / 1.0 # more brake less score.
        if handbrake < 0.9:
            reward -= 1

        reward -= (10000.0 - self.game.car_rpm()) / 10000.0 # high rpm more score.
        reward -= (220.0 - self.game.car_speed()) / 220.0 # high speed more score.
        reward -= (7.0 - self.game.car_gear()) / 7.0 # high gear more score.

        return reward