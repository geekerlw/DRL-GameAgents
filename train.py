import gymnasium as gym
from stable_baselines3 import PPO
from env import RBREnv
import time

def train():
    env = RBREnv()
    print("start training after 30s, start game please.")
    time.sleep(30)
    env.prepare()

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10)
    print("finish training!!!")

if __name__ == '__main__':
    train()