import time
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from observation import Numeric, Image
from action import Action
from game import RBRGame
from driveline import DriveLine

class RBREnv(gym.Env):
    def __init__(self, shakedown=False):
        super(RBREnv, self).__init__()
        self.shakedown = shakedown
        self.total_rewards = 0
        self.game = RBRGame()
        self.driveline = DriveLine()
        self.numeric = Numeric(self.game, self.driveline)
        self.image = Image()
        self.action = Action()
        numeric_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.numeric.dementions(),), dtype=np.float32)
        image_space = spaces.Box(low=0, high=255, shape=(self.image.dementions(), self.image.width, self.image.height, 3), dtype=np.uint8)
        self.observation_space = spaces.Tuple((numeric_space, image_space))
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

        self.driveline.load(self.game.stageid())
        self.game.load_pacenotes()
        while not self.game.is_stage_started():
            time.sleep(0.2)

    def reset(self, seed=None):
        self.total_rewards = 0
        self.game.reset()
        self.numeric.reset()
        self.image.reset()
        self.action.reset()
        self.restart_game()
        return (self.numeric.take(), self.image.take()), {}

    def step(self, action):
        self.game.step()
        self.action.execute(action)
        time.sleep(0.2) # need some delay to wait game state update
        reward, done, truncated = self.evaluate()
        self.total_rewards += reward
        print(f"take action: {action}, got reward: {reward}, total: {self.total_rewards}")
        return (self.numeric.take(), self.image.take()), reward, done, truncated, {}
    
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
        
        if self.total_rewards < -1e3 or self.total_rewards > 1e4:
            print(f"saddly, too many mistakes or infinate loop, rewards: {self.total_rewards}.")
            return True

        return False
    
    def evaluate(self):
        reward = 0
        done = self.done()
        truncated = self.truncated()
        reward -= 3 # step base reward, more step means more time and less reward.
        # if self.game.drive_distance() - self.game.last_distance < 0: # back way detected
        #     reward -= 2
        # else:
        #     reward += 1

        # if self.game.car_rpm() < 4000 or self.game.car_rpm() > 7000:
        #     reward -= 2
        # else:
        #     reward += 1

        # if self.game.last_gear != self.game.car_gear():
        #     reward -= 2
        # else:
        #     reward += 1

        # if self.game.car_gear() < 2: # R/N gear is bad.
        #     reward -= 2
        # else:
        #     reward += 1

        # speed = self.game.car_speed()
        # if speed < 0:
        #     reward -= 2
        # else:
        #     reward += 1

        distance = np.linalg.norm(np.array(self.game.car_pos()) - np.array(self.game.last_pos))
        if self.game.startcount() < -10.0 and distance < 1e-3:
            print("saddly, car maybe stoped after game start ten seconds.")
            truncated |= True
        else:
            reward += int(distance)

        angel = self.driveline.offset(self.game.drive_distance(), self.game.last_pos, self.game.car_pos())
        if 10 < angel and angel < 20:
            reward -= int(angel - 10)
        elif 0 <= angel and angel <= 10:
            reward += int(10 - (angel))
        else:
            print(f"saddly, car is driving to a wrong direction {angel}.")
            truncated |= True

        outline = self.driveline.outline(self.game.drive_distance(), self.game.car_pos())
        if outline > 4:
            print("saddly, car is out of the driveline.")
            truncated |= True
        else:
            reward -= int(outline)

        if done:
            reward += 100
        if truncated:
            reward -= 100
        return reward, done, truncated