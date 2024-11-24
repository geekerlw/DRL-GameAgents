import os
from stable_baselines3 import PPO, DQN
from env import RBREnv

MODEL_DIR = "model"
PPO_HALF_MODEL = "ppo-rbragent-half"
PPO_FINAL_MODEL = "ppo-rbragent"
DQN_HALF_MODEL = "dqn-rbragent-half"
DQN_FINAL_MODEL = "dqn-rbragent"

def train_ppo():
    os.makedirs(MODEL_DIR, exist_ok=True)
    try:
        env = RBREnv(continous=True, shakedown=True, spacetype=4)
        if os.path.exists(os.path.join(MODEL_DIR, PPO_HALF_MODEL) + ".zip"):
            model = PPO.load(os.path.join(MODEL_DIR, PPO_HALF_MODEL), env=env)
        else:
            model = PPO("MultiInputPolicy", env, verbose=1)
        model.n_steps = 128
        model.batch_size = 16
        model.learn(total_timesteps=30000)
    except Exception as e:
        print(f"training abort: {e}, save half trained model.")
        model.save(os.path.join(MODEL_DIR, PPO_HALF_MODEL))
        return

    print("training finished, save final model.")
    model.save(os.path.join(MODEL_DIR, PPO_FINAL_MODEL))

def train_dqn():
    os.makedirs(MODEL_DIR, exist_ok=True)
    try:
        env = RBREnv(continous=False, shakedown=True, spacetype=1)
        if os.path.exists(os.path.join(MODEL_DIR, DQN_HALF_MODEL) + ".zip"):
            model = DQN.load(os.path.join(MODEL_DIR, DQN_HALF_MODEL), env=env)
        else:
            model = DQN("MlpPolicy", env, verbose=1)
        model.learn(total_timesteps=1e5)
    except Exception as e:
        print(f"training abort: {e}, save half trained model.")
        model.save(os.path.join(MODEL_DIR, DQN_HALF_MODEL))
        return

    print("training finished, save final model.")
    model.save(os.path.join(MODEL_DIR, DQN_FINAL_MODEL))


if __name__ == '__main__':
    train_ppo()
    # train_dqn()