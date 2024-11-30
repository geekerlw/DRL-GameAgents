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
        time.sleep(0.2) # need some delay to wait game state update
        reward, done, truncated = self.evaluate()
        if done or truncated:
            self.monitor.stop()
            self.monitor.join()
            self.monitor = None
        self.total_rewards += reward
        print(f"take action: {action}, got reward: {reward}, total: {self.total_rewards}")
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
        reward -= 2 # step base reward, more step means more time and less reward.
        if self.game.drive_distance() - self.game.last_distance > 3: # back way detected
            reward += 2
  
        if self.game.race_wrongway(): # wrong way.
            reward -= 2

        # if self.game.car_rpm() > 4000 or self.game.car_rpm() < 6500:
        #     reward += 2

        # if self.game.last_gear != self.game.car_gear():
        #     reward -= 2

        # gear = self.game.car_gear()
        speed = self.game.car_speed()
        # if gear < 2 or speed < 20 * gear: # R/N gear is bad.
        #     reward -= 5

        distance = np.linalg.norm(np.array(self.game.car_pos()) - np.array(self.game.last_pos))
        if self.game.startcount() < -10.0 and distance < 1e-3:
            print("saddly, car maybe stoped after game start ten seconds.")
            truncated |= True
        else:
            reward += int(distance / 3)

        angel = self.driveline.offset(self.game.drive_distance(), self.game.last_pos, self.game.car_pos())
        if angel > 45:
            print(f"saddly, car is driving to a wrong direction {angel}.")
            truncated |= True
        elif 24 <= angel and speed > 40:
            reward += 1
        elif angel < 24 and speed > 20:
            reward += 8 - int(angel / 3)

        outline = self.driveline.outline(self.game.drive_distance(), self.game.car_pos())
        if outline > 5:
            print("saddly, car is out of the driveline.")
            truncated |= True
        elif speed > 20:
            reward += 10 - int(outline) * 2

        if done:
            reward += int(self.game.travel_distance() * 50)
        if truncated:
            reward -= 1000
        return reward, done, truncated