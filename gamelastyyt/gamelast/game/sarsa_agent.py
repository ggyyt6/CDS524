import random
from environment import MazeEnvironment
from config import Config

class SarsaAgent:
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

    def learn(self, s, a, r, s_next, a_next):
        old_q = self.get_q(s, a)
        if s_next is None or a_next is None:
            target = r
        else:
            target = r + self.gamma * self.get_q(s_next, a_next)
        self.q_table[(s, a)] = old_q + self.alpha * (target - old_q)

    def train(self):
        for _ in range(Config.EPISODES):
            state = self.env.reset()
            action = self.choose_action(state)
            for _ in range(Config.MAX_STEPS):
                next_state, reward, done = self.env.step(action)
                if done:
                    self.learn(state, action, reward, None, None)
                    break
                next_action = self.choose_action(next_state)
                self.learn(state, action, reward, next_state, next_action)
                state = next_state
                action = next_action
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def run_episode(self):
        s = self.env.reset()
        a = self.choose_action(s)
        total_reward = 0
        for _ in range(Config.MAX_STEPS):
            s_next, r, done = self.env.step(a)
            total_reward += r
            if done:
                break
            a_next = self.choose_action(s_next)
            s = s_next
            a = a_next
        return total_reward
