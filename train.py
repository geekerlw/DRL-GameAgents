import os
from stable_baselines3 import PPO
from env import RBREnv

MODEL_DIR = "model"
HALF_MODEL = "ppo-rbragent-half"
FINAL_MODEL = "ppo-rbragent"

def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    try:
        env = RBREnv(shakedown=True)
        if os.path.exists(os.path.join(MODEL_DIR, HALF_MODEL) + ".zip"):
            model = PPO.load(os.path.join(MODEL_DIR, HALF_MODEL), env=env)
        else:
            model = PPO("MultiInputPolicy", env, verbose=1)
        model.n_steps = 64
        model.batch_size = 16
        model.learn(total_timesteps=100_000)
    except Exception as e:
        print(f"training abort: {e}, save half trained model.")
        model.save(os.path.join(MODEL_DIR, HALF_MODEL))
        return

    print("training finished, save final model.")
    model.save(os.path.join(MODEL_DIR, FINAL_MODEL))

if __name__ == '__main__':
    train()