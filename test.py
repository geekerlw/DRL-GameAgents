from stable_baselines3 import PPO, DQN
from env import RBREnv

def train():
    env = RBREnv(continous=True, shakedown=True, spacetype=4)
    model = PPO("MultiInputPolicy", env, verbose=1, n_steps=128, batch_size=16)
    model.learn(total_timesteps=10_000)
    model.save("model/rbragent-test")

if __name__ == '__main__':
    train()