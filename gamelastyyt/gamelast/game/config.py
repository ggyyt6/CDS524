class Config:
    ALPHA = 0.1
    GAMMA = 0.95
    EPSILON = 1.0
    EPSILON_DECAY = 0.995
    MIN_EPSILON = 0.01
    EPISODES = 500
    MAX_STEPS = 200
    COIN_REWARD = 10
    TRAP_PENALTY = -10
    GOAL_REWARD = 50
    STEP_COST = -0.1
    MAZE_WIDTH = 10
    MAZE_HEIGHT = 10
