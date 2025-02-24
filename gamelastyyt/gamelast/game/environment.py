import random
from config import Config

class MazeEnvironment:
    def __init__(self):
        self.width = Config.MAZE_WIDTH
        self.height = Config.MAZE_HEIGHT
        self.coin_reward = Config.COIN_REWARD
        self.trap_penalty = Config.TRAP_PENALTY
        self.goal_reward = Config.GOAL_REWARD
        self.step_cost = Config.STEP_COST
        self.actions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.reset()

    def _place_random_objects(self, target_set, count, used):
        placed = 0
        while placed < count:
            r = random.randint(0, self.height - 1)
            c = random.randint(0, self.width - 1)
            if (r, c) not in used:
                target_set.add((r, c))
                used.add((r, c))
                placed += 1

    def reset(self):
        self.done = False
        self.player_row = 0
        self.player_col = 0
        self.goal_row = self.height - 1
        self.goal_col = self.width - 1
        self.coins = set()
        self.traps = set()
        used_positions = {
            (self.player_row, self.player_col),
            (self.goal_row, self.goal_col)
        }
        coin_count = (self.width * self.height) // 10
        trap_count = (self.width * self.height) // 10
        self._place_random_objects(self.coins, coin_count, used_positions)
        self._place_random_objects(self.traps, trap_count, used_positions)
        return (self.player_row, self.player_col)

    def step(self, action):
        if self.done:
            return (self.player_row, self.player_col), 0, True
        dr, dc = self.actions[action]
        nr = self.player_row + dr
        nc = self.player_col + dc
        reward = self.step_cost
        if nr < 0 or nr >= self.height or nc < 0 or nc >= self.width:
            nr, nc = self.player_row, self.player_col
        if (nr, nc) in self.coins:
            reward += self.coin_reward
            self.coins.remove((nr, nc))
        if (nr, nc) in self.traps:
            reward += self.trap_penalty
            self.traps.remove((nr, nc))
        self.player_row, self.player_col = nr, nc
        if (nr, nc) == (self.goal_row, self.goal_col):
            reward += self.goal_reward
            self.done = True
        return (self.player_row, self.player_col), reward, self.done

    def get_state(self):
        return (self.player_row, self.player_col)

    def get_actions(self):
        return list(range(len(self.actions)))
