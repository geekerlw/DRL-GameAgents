from stable_baselines3 import PPO
from env import RBREnv

def train():
    try:
        env = RBREnv(shakedown=True)
        model = PPO("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=10_000)
    except Exception as e:
        print("training abort: {e}")
        model.save("part_model")

    model.save("final_model")

if __name__ == '__main__':
    train()