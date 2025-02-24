import os
import json
import matplotlib.pyplot as plt

class StatsLogger:
    def __init__(self, log_dir="data/logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_data = []

    def log_episode(self, episode, reward):
        self.log_data.append((episode, reward))

    def save_log(self, filename="training_log.json"):
        path = os.path.join(self.log_dir, filename)
        with open(path, "w") as f:
            json.dump(self.log_data, f)

    def load_log(self, filename="training_log.json"):
        path = os.path.join(self.log_dir, filename)
        if os.path.isfile(path):
            with open(path, "r") as f:
                self.log_data = json.load(f)
        else:
            self.log_data = []

    def plot_rewards(self, filename="training_rewards.png"):
        if not self.log_data:
            return
        episodes, rewards = zip(*self.log_data)
        plt.figure(figsize=(8, 5))
        plt.plot(episodes, rewards, label="Episode Reward")
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.title("Training Progress")
        plt.legend()
        plt.savefig(os.path.join(self.log_dir, filename))
        plt.close()

class ModelCheckpoint:
    def __init__(self, checkpoint_dir="data/checkpoint"):
        self.checkpoint_dir = checkpoint_dir
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)

    def save_q_table(self, q_table, filename="q_table.json"):
        path = os.path.join(self.checkpoint_dir, filename)
        data = {}
        for k, v in q_table.items():
            data[str(k)] = v
        with open(path, "w") as f:
            json.dump(data, f)

    def load_q_table(self, filename="q_table.json"):
        path = os.path.join(self.checkpoint_dir, filename)
        q_table = {}
        if os.path.isfile(path):
            with open(path, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    q_table[eval(k)] = v
        return q_table
