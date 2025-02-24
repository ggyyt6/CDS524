import random
from environment import MazeEnvironment
from config import Config

class QLearningAgent:
    def __init__(self):
        self.env = MazeEnvironment()
        self.alpha = Config.ALPHA
        self.gamma = Config.GAMMA
        self.epsilon = Config.EPSILON
        self.epsilon_decay = Config.EPSILON_DECAY
        self.min_epsilon = Config.MIN_EPSILON
        self.q_table = {}

    def get_q(self, state, action):
        if (state, action) not in self.q_table:
            self.q_table[(state, action)] = 0.0
        return self.q_table[(state, action)]

    def best_action(self, state):
        actions = self.env.get_actions()
        values = [self.get_q(state, a) for a in actions]
        return actions[values.index(max(values))]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.env.get_actions())
        else:
            return self.best_action(state)

    def learn(self, s, a, r, s_next):
        old_q = self.get_q(s, a)
        max_q_next = max([self.get_q(s_next, act) for act in self.env.get_actions()])
        self.q_table[(s, a)] = old_q + self.alpha * (r + self.gamma * max_q_next - old_q)

    def train(self):
        for _ in range(Config.EPISODES):
            state = self.env.reset()
            for _ in range(Config.MAX_STEPS):
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.learn(state, action, reward, next_state)
                state = next_state
                if done:
                    break
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_episode(self):
        s = self.env.reset()
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            a = self.best_action(s)
            s_next, r, done = self.env.step(a)
            total_reward += r
            s = s_next
            if done:
                break
        return total_reward
