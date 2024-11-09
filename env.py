import gymnasium as gym
from gymnasium import spaces
import numpy as np
from observation import Observation
from action import Action

class RBREnv(gym.Env):
    def __init__(self):
        super(RBREnv, self).__init__()
        self.observation = Observation()
        self.action = Action()

        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.observation.dementions(),), dtype=np.float32)
        self.action_space = spaces.Discrete(self.action.dimentions())
        self.state = np.zeros(self.observation.dementions())

    def reset(self):
        self.state = np.random.rand(6)
        return self.state

    def step(self, action):
        self.state = np.clip(self.state + action[:6], -10, 10)  # 更新状态，限制范围

        reward = -np.sum(np.abs(self.state))  # 奖励为状态绝对值之和的负数

        # 检查是否完成
        done = np.random.rand() < 0.1  # 10% 的概率结束

        truncated = False

        return self.state, reward, done, truncated, {}