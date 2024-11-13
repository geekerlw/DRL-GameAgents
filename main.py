from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from env import RBREnv

def evaluate():
    env = RBREnv(shakedown=False)
    model = PPO.load("pretrained/ppo-rbragent", env=env)
    mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
    print(f"final evaluate result: {mean_reward}, {std_reward}")

if __name__ == '__main__':
    evaluate()