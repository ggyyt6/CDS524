import sys
from qlearning_agent import QLearningAgent
from sarsa_agent import SarsaAgent
from utils import StatsLogger, ModelCheckpoint
from game_ui import MazeGameUI
from config import Config

def train_q():
    agent = QLearningAgent()
    logger = StatsLogger()
    ckpt = ModelCheckpoint()
    for episode in range(Config.EPISODES):
        state = agent.env.reset()
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            action = agent.choose_action(state)
            next_state, reward, done = agent.env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            if done:
                break
        agent.epsilon = max(agent.min_epsilon, agent.epsilon * agent.epsilon_decay)
        logger.log_episode(episode, total_reward)
    logger.save_log("qlearning_log.json")
    logger.plot_rewards("qlearning_rewards.png")
    ckpt.save_q_table(agent.q_table, "qlearning_q_table.json")

def train_s():
    agent = SarsaAgent()
    logger = StatsLogger()
    ckpt = ModelCheckpoint()
    for episode in range(Config.EPISODES):
        state = agent.env.reset()
        action = agent.choose_action(state)
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            next_state, reward, done = agent.env.step(action)
            if done:
                agent.learn(state, action, reward, None, None)
                total_reward += reward
                break
            next_action = agent.choose_action(next_state)
            agent.learn(state, action, reward, next_state, next_action)
            state = next_state
            action = next_action
            total_reward += reward
        agent.epsilon = max(agent.min_epsilon, agent.epsilon * agent.epsilon_decay)
        logger.log_episode(episode, total_reward)
    logger.save_log("sarsa_log.json")
    logger.plot_rewards("sarsa_rewards.png")
    ckpt.save_q_table(agent.q_table, "sarsa_q_table.json")

def test_q(episodes=10):
    agent = QLearningAgent()
    ckpt = ModelCheckpoint()
    agent.q_table = ckpt.load_q_table("qlearning_q_table.json")
    scores = []
    for _ in range(episodes):
        s = agent.env.reset()
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            a = agent.best_action(s)
            s_next, r, done = agent.env.step(a)
            total_reward += r
            s = s_next
            if done:
                break
        scores.append(total_reward)
    return sum(scores) / len(scores)

def test_s(episodes=10):
    agent = SarsaAgent()
    ckpt = ModelCheckpoint()
    agent.q_table = ckpt.load_q_table("sarsa_q_table.json")
    scores = []
    for _ in range(episodes):
        s = agent.env.reset()
        a = agent.best_action(s)
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            s_next, r, done = agent.env.step(a)
            total_reward += r
            if done:
                break
            a_next = agent.best_action(s_next)
            s = s_next
            a = a_next
        scores.append(total_reward)
    return sum(scores) / len(scores)

def run_ui():
    ui = MazeGameUI()
    ui.run()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [train_q|train_s|test_q|test_s|ui]")
        sys.exit()
    cmd = sys.argv[1]
    if cmd == "train_q":
        train_q()
    elif cmd == "train_s":
        train_s()
    elif cmd == "test_q":
        score = test_q()
        print("Q-Learning average score:", score)
    elif cmd == "test_s":
        score = test_s()
        print("Sarsa average score:", score)
    elif cmd == "ui":
        run_ui()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
