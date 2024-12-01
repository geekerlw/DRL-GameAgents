import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from observation import Numeric, Image
from action import Action
from game import RBRGame
from driveline import DriveLine
from track import TrackMonitor

class RBREnv(gym.Env):
    def __init__(self, continous=True, shakedown=False, spacetype=1):
        super(RBREnv, self).__init__()
        self.timetick = time.time()
        self.spacetype = spacetype
        self.shakedown = shakedown
        self.total_rewards = 0
        self.game = RBRGame()
        self.driveline = DriveLine()
        self.monitor = None
        self.numeric = Numeric(self.game, self.driveline)
        self.image = Image()
        self.action = Action(continous)
        numeric_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.numeric.dementions(),), dtype=np.float32)
        image_space = spaces.Box(low=0, high=255, shape=(self.image.width, self.image.height, 3), dtype=np.uint8)
        conbined_space = spaces.Dict({
            'numeric': numeric_space,
            'image': image_space
            })
        if spacetype == 1:
            self.observation_space = numeric_space
        elif spacetype == 2:
            self.observation_space = image_space
        elif spacetype == 4:
            self.observation_space = conbined_space

        if continous:
            self.action_space = spaces.Box(low=-1, high=1, shape=(self.action.dimentions(),), dtype=np.float32)
        else:
            self.action_space = spaces.Discrete(self.action.dimentions())

    def observation(self):
        if self.spacetype == 1:
            return self.numeric.take()
        elif self.spacetype == 2:
            return self.image.take()
        elif self.spacetype == 4:
            return {'numeric': self.numeric.take(), 'image': self.image.take()}

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

        self.driveline.load(self.game.stageid())
        self.game.load_pacenotes()

        if self.monitor == None:
            self.monitor = TrackMonitor(self.game, self.driveline)

        while not self.game.is_stage_started():
            time.sleep(0.2)

    def reset(self, seed=None):
        self.total_rewards = 0
        self.game.reset()
        self.numeric.reset()
        self.image.reset()
        self.action.reset()
        self.restart_game()
        return self.observation(), {}

    def step(self, action):
        self.game.step()
        self.action.execute(action)
        time.sleep(0.02) # need some delay to wait game state update
        reward, done, truncated = self.evaluate()
        if done or truncated:
            self.monitor.stop()
            self.monitor.join()
            self.monitor = None
        self.total_rewards += reward
        curtime = time.time()
        if curtime - self.timetick > 2 or done or truncated:
            print(f"take action: {action}, got reward: {reward}, total: {self.total_rewards}")
            self.timetick = curtime
        return self.observation(), reward, done, truncated, {}
    
    def done(self):
        if self.shakedown:
            if self.game.travel_distance() > 60:
                return True
            
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
        
        if self.total_rewards < -1e3 or self.total_rewards > 1e4:
            print(f"saddly, too many mistakes or infinate loop, rewards: {self.total_rewards}.")
            return True

        return False
    
    def evaluate(self):
        reward = 0
        done = self.done()
        truncated = self.truncated()
        reward -= 0.1 # step base reward, more step means more time and less reward.

        if self.game.car_speed() < 0:
            reward -= 1

        outline = self.driveline.outline(self.game.drive_distance(), self.game.car_pos())
        if outline > 5:
            print("saddly, car is out of the driveline.")
            truncated |= True

        if done:
            reward += int(self.game.travel_distance())
        if truncated:
            reward -= 100
        return reward, done, truncated