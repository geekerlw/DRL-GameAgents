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
            self.action.start()

        while not self.game.is_stage_loaded():
            print("stage is not loaded, select a stage to start.")
            time.sleep(2)

        self.game.load_pacenotes()
        while not self.game.is_stage_started():
            time.sleep(0.2)

    def reset(self, seed=None):
        self.game.reset()
        self.action.reset()
        self.restart_game()
        return self.numeric.take(), {}

    def step(self, action):
        reward = self.action.execute(action)
        time.sleep(0.2) # need some delay to wait game state update
        reward += self.reward()
        print(f"take action: {action}, got reward: {reward}")
        self.game.step()
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
        if self.game.startcount() > -5.0: # make sure racing over 5 seconds.
            return False

        if self.game.race_failstart():
            print("saddly, race start failed.")
            return True

        if self.game.race_wrongway():
            print("saddly, car turn into a wrong way.")
            return True

        if self.game.is_stage_started() and self.game.car_speed() == 0.0:
            print("saddly, car maybe stoped.")
            return True

        if self.game.car_temp() >= 130:
            print("saddly, car temp is too high, maybe damaged.")
            return True
    
        return False
    
    def reward(self):
        reward = 0
        reward -= 1 # step base reward, more step means more time and less reward.
        print(f"last {self.game.last_distance}, cur: {self.game.travel_distance()}")
        if self.game.last_distance < self.game.travel_distance():
            reward += 5

        if self.game.car_rpm() < 4000 or self.game.car_rpm() > 7000: # too low or high rpm, bad gear keep.
            reward -= 1
        throttle, brake, handbrake, _= self.game.car_control()
        if throttle >= 0.9 and brake < 0.1 and handbrake == 0: # full throttle
            reward += 1
        if brake > 0.8 or handbrake < 0.8: # too high brake and bad handbrake operation
            reward -= 1
        if brake > 0.7 and throttle > 0.2: # brake with throttle, bad operation
            reward -= 1
        if throttle > 0.7 and (brake > 0.2 or handbrake > 0.2): # throttle with brake, bad operaton
            reward -= 1
        if handbrake > 0.8 and throttle > 0.6: # throttle when handbrake on, bad operation
            reward -= 1

        speed = self.game.car_speed()
        if speed < 0:
            reward -= 3
        elif speed > 0 and speed < 60:
            reward -= 2
        elif speed >= 60 and speed < 100:
            reward -= 1
        elif speed > 100:
            reward += 1

        gear = self.game.car_gear()
        if gear < 2: # R/N bad operation
            reward -= 1
        elif gear > 4: # highway gears
            reward += 1

        return reward