from stable_baselines3 import PPO
from env import RBREnv

def train():
    env = RBREnv(shakedown=True)
    model = PPO("MultiInputPolicy", env, verbose=1, n_steps=64, batch_size=16)
    model.learn(total_timesteps=10_000)
    model.save("model/ppo-rbragent-test")

if __name__ == '__main__':
    train()