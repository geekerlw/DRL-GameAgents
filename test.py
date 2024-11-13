from stable_baselines3 import PPO
from env import RBREnv

def train():
    env = RBREnv(shakedown=True)
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)

if __name__ == '__main__':
    train()