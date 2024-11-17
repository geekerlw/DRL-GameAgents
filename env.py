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
        if self.game.car_temp() >= 130 and self.game.car_speed() == 0.0:
            print("saddly, car temp is too high, maybe damaged.")
            return True

        if self.game.car_speed() < -10:
            print("saddly, car is reversing.")
            return True
        
        if self.game.race_wrongway(): # wrong way.
            print("saddly, car is driving to wrong way.")
            return True
        
        if self.total_rewards < -1000:
            print("saddly, too many mistakes.")
            return True
        
        distance = np.linalg.norm(np.array(self.game.car_pos()[:3]) - np.array(self.game.last_pos[:3]))
        if self.game.startcount() < -10.0 and distance < 1e-3:
            print("saddly, car maybe stoped after game start ten seconds.")
            return True

        return False
    
    def reward(self):
        reward = 0
        reward -= 1 # step base reward, more step means more time and less reward.
        if self.game.last_distance > self.game.travel_distance(): # back way detected
            reward -= 2
        else:
            reward += 2

        if self.game.car_rpm() < 4000 or self.game.car_rpm() > 6500:
            reward -= 2
        else:
            reward += 1

        speed = self.game.car_speed()
        if speed < -10:
            reward -= 100
        elif -10 <= speed and speed < 10:
            reward -= 2
        else:
            reward -= int(self.game.car_speed() / 10)

        if self.game.car_temp() >= 130 and self.game.car_speed() == 0.0:
            reward -= 100
        
        if self.game.race_wrongway():
            reward -= 100

        distance = np.linalg.norm(np.array(self.game.car_pos()[:3]) - np.array(self.game.last_pos[:3]))
        print(f"last distance diff: {distance}")
        if distance < 1e-3:
            reward -= 100

        # throttle, brake, handbrake, _= self.game.car_control()
        # reward -= (1.0 - throttle) / 1.0 # more throttle more score.
        # reward -= 1.0 - (brake - 1.0) / 1.0 # more brake less score.
        # if handbrake < 0.9:
        #     reward -= 1

        return reward