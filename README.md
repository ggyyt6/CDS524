# Reinforcement Learning Maze Navigation

This repository contains a **Reinforcement Learning** (RL) project that demonstrates maze navigation using **Q-Learning** and **SARSA** algorithms. The environment is a grid-based maze in which an agent must collect coins, avoid traps, and ultimately reach a goal. A **Pygame**-based user interface allows for both **manual play** and **automated agent demonstrations**. Comprehensive **training** modes (with or without real-time visualization) enable users to observe how agents learn over multiple episodes.

------

## Table of Contents

1. [Features](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#features)
2. [Project Structure](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#project-structure)
3. [Installation](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#installation)
4. [Usage](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#usage)
5. [Reinforcement Learning Overview](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#reinforcement-learning-overview)
6. [Algorithms](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#algorithms)
7. [Configuration](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#configuration)
8. [Future Improvements](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#future-improvements)
9. [License](https://chatgpt.com/c/67ba1522-d1f8-800a-bdd8-bde881e36342#license)

------

## Features

- **Grid-Based Maze Environment**
  - Each cell can be a floor, coin, trap, or a goal.
  - The agent starts at the top-left corner and aims to reach the bottom-right cell.
  - Random placement of coins and traps each episode (with customizable rewards/penalties).
- **Two RL Agents**
  - **Q-Learning (off-policy)**
  - **SARSA (on-policy)**
- **Multiple Training/Testing Modes**
  - **Manual Play**: Control the player with arrow keys.
  - **Train Q-Learning**: Train for a specified number of episodes, display training progress.
  - **Train Sarsa**: Same interface but uses SARSA.
  - **AI Demo**: Watch a trained agent traverse the maze automatically.
  - **Training Demo**: Real-time visualization of the maze while the agent learns.
- **Graphical Interface (Pygame)**
  - Renders the maze, agent, coins, traps, and goal.
  - Shows an info panel with current score, training statistics, and a live reward curve (via matplotlib).
- **Configurable Hyperparameters**
  - Learning rate (α\alpha), discount factor (γ\gamma), exploration rate (ϵ\epsilon), maximum episodes, reward values, etc.

------

## Project Structure

A typical directory layout is as follows:

```
.
├── game/
│   ├── __init__.py
│   ├── environment.py        # Defines the MazeEnvironment
│   ├── qlearning_agent.py    # Q-Learning agent implementation
│   ├── sarsa_agent.py        # SARSA agent implementation
│   ├── config.py             # Stores hyperparameters
│   ├── game_ui.py            # Pygame GUI for training, testing, demonstration
│   └── main.py               # Entry point
├── data/
│   ├── checkpoint/           # Saved Q-tables or model checkpoints
│   └── logs/                 # Training logs, e.g. JSON or CSV
├── docs/
│   └── report.pdf            # Project report or documentation
├── demo/
│   ├── screenshots/          # Images for demonstration
│   └── demo_video.mp4        # Optional, a recorded video of gameplay
├── requirements.txt
├── README.md
└── .gitignore
```

> **Note**: Some file paths may vary. Adjust accordingly based on your actual setup.

------

## Installation

1. **Clone this repository**:

   ```bash
   git clone https://github.com/YourUsername/your-project.git
   cd your-project
   ```

2. **Set up a virtual environment (recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The requirements typically include:

   - `pygame`
   - `matplotlib`
   - `numpy`
   - `python 3.7+` (or higher version)

4. **Place the required images** (`floor.png`, `player.png`, `coin.png`, `trap.png`, `exit.png`) in the same folder as `game_ui.py`, or update the file paths inside the code to match your structure.

------

## Usage

The primary entry point is `main.py`. You can run it directly with specific command-line arguments, or you can rely on the **GUI menu** integrated within the code.

### Command-Line Approach

```bash
cd game
python main.py [command]
```

**Available commands**:

- `train_q`: Train a Q-Learning agent.
- `train_s`: Train a SARSA agent.
- `test_q`: Test the Q-Learning agent after loading `q_table.json`.
- `test_s`: Test the SARSA agent after loading `sarsa_q_table.json`.
- `ui`: Launch the Pygame graphical interface with menu options.

For example:

```bash
python main.py train_q
```

will run the Q-Learning training for the specified number of episodes (configured in `config.py`).

### Graphical Interface

If you prefer the **GUI**, run:

```bash
python main.py ui
```

Inside the **GUI menu**, you will see buttons for:

- **Manual Play** (move with arrow keys, `R` to reset, `ESC` to quit)
- **Train Q-Learning / Train Sarsa** (observe real-time plots of the agent’s training progress)
- **AI Demo** (agent navigates automatically using its learned Q-values)
- **Training Demo** (the agent learns while showing the maze on-screen, every few frames)

------

## Reinforcement Learning Overview

The project implements two popular temporal-difference (TD) control algorithms:

1. **Q-Learning**: Off-policy method that learns the optimal QQ by maximizing over possible future actions (max⁡a′Q(s′,a′)\max_{a'}Q(s',a')).
2. **SARSA**: On-policy method that updates QQ using the next action a′a' actually taken under the current policy.

Both methods rely on an ϵ\epsilon-greedy strategy for exploration:

action={random actionwith probability ϵarg⁡max⁡a′Q(s,a′)with probability (1−ϵ).\text{action} =  \begin{cases} \text{random action} & \text{with probability } \epsilon \\ \arg\max_{a'} Q(s,a') & \text{with probability } (1-\epsilon). \end{cases}

### Q-Learning Update Rule

$$
Q(s,a)←Q(s,a)+α[r+γmax⁡a′Q(s′,a′)−Q(s,a)]Q(s, a) 
$$



### SARSA Update Rule

$$
Q(s,a)←Q(s,a)+α[r+γQ(s′,a′)−Q(s,a)]Q(s, a) 
$$

where α is the learning rate, γ is the discount factor, and r is the immediate reward.

------

## Algorithms

1. **QLearningAgent**
   - Maintains a dictionary-based Q-table:
     (state,action)→float(\text{state}, \text{action}) \to \text{float}.
   - Chooses actions according to ϵ\epsilon-greedy.
   - Uses Q-Learning formula for updates.
2. **SarsaAgent**
   - Similar dictionary-based Q-table.
   - On-policy updates; next state-action pair is sampled from the current ϵ\epsilon-greedy policy.

**Key Hyperparameters**:

- **Alpha (α\alpha)**: Learning rate (0.1–0.3 commonly tested).
- **Gamma (γ\gamma)**: Discount factor for future rewards (typical values 0.9–0.99).
- **Epsilon (ϵ\epsilon)**: Exploration rate (decays over time, e.g., from 1.0 to 0.01).
- **Episodes**: Number of training episodes (e.g., 500–1500+).

------

## Configuration

All critical hyperparameters and environment constants are defined in `config.py`:

```python
class Config:
    ALPHA = 0.1
    GAMMA = 0.95
    EPSILON = 1.0
    EPSILON_DECAY = 0.995
    MIN_EPSILON = 0.01
    EPISODES = 1500
    MAX_STEPS = 200
    COIN_REWARD = 10
    TRAP_PENALTY = -10
    GOAL_REWARD = 50
    STEP_COST = -0.1
    MAZE_WIDTH = 10
    MAZE_HEIGHT = 10
```

Feel free to tune these values for different experiment setups.

------

## Future Improvements

1. **Function Approximation**: Replace the Q-table with a **neural network** (e.g., Deep Q-Network, DQN) for larger or more complex mazes.
2. **Dynamic Environments**: Introduce moving traps or multiple floors to create more challenging scenarios.
3. **Reward Shaping**: Provide additional intermediate rewards for partial goals or sub-tasks, accelerating convergence.
4. **Multi-Agent**: Explore cooperative or competitive tasks with multiple agents in the same maze.
5. **Improved Graphics & Animations**: Enhance the user experience with more visually appealing tiles, transitions, and animations.

------

## License

Feel free to fork, modify, and use this codebase for academic or personal projects, attributing the original source where appropriate.

------

**Thank you for exploring this Reinforcement Learning Maze project!** If you have any questions or suggestions, please open an issue or submit a pull request.
