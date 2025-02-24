import sys
import random
import pygame
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO

from environment import MazeEnvironment
from config import Config
from qlearning_agent import QLearningAgent
from sarsa_agent import SarsaAgent

pygame.init()
pygame.font.init()

# 固定窗口大小
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900
INFO_PANEL_WIDTH = 400

# 计算迷宫显示区域
MAZE_DISPLAY_WIDTH = SCREEN_WIDTH - INFO_PANEL_WIDTH
MAZE_DISPLAY_HEIGHT = SCREEN_HEIGHT

# 根据环境大小，自动计算 tile_size
maze_width = Config.MAZE_WIDTH
maze_height = Config.MAZE_HEIGHT
tile_size = min(MAZE_DISPLAY_WIDTH // maze_width, MAZE_DISPLAY_HEIGHT // maze_height)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze RL Demo")

font_small = pygame.font.SysFont("Arial", 18)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 32)

def load_and_scale(img_path, new_w, new_h):
    img = pygame.image.load(img_path).convert_alpha()
    return pygame.transform.scale(img, (new_w, new_h))

# 自动根据 tile_size 对贴图进行缩放
floor_img = load_and_scale("floor.png", tile_size, tile_size)
player_img = load_and_scale("player.png", tile_size, tile_size)
coin_img = load_and_scale("coin.png", tile_size, tile_size)
trap_img = load_and_scale("trap.png", tile_size, tile_size)
goal_img = load_and_scale("exit.png", tile_size, tile_size)

class Button:
    def __init__(self, x, y, w, h, text, font, color_bg, color_fg):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color_bg = color_bg
        self.color_fg = color_fg

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_bg, self.rect)
        label = self.font.render(self.text, True, self.color_fg)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class MazeGameUI:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.env = MazeEnvironment()
        self.score = 0
        self.done = False
        self.state = "MENU"
        self.agent = None
        self.agent_type = ""
        self.episode_rewards = []
        self.chart_surface = None

        # 这里设置训练回合数 1500
        self.total_training_episodes = 500

        # 训练演示时，每帧执行多少步
        self.training_speed = 20

        # Training Demo 用
        self.max_demo_episodes = 500
        self.training_speed = 20
        self.episode_count = 0
        self.in_episode = False
        self.current_episode_reward = 0
        self.current_step_count = 0

        self.create_buttons()

    def create_buttons(self):
        self.menu_buttons = []
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 150
        gap = 50

        labels = [
            ("Manual Play", "MANUAL"),
            ("Train Q-Learning", "TRAIN_Q"),
            ("Train Sarsa", "TRAIN_S"),
            ("AI Demo", "AI_DEMO"),
            ("Training Demo", "TRAINING_DEMO"),
            ("Quit", "EXIT")
        ]

        for i, (txt, st) in enumerate(labels):
            bx = center_x - 100
            by = start_y + i * gap
            btn = Button(bx, by, 200, 40, txt, font_medium, (100, 100, 200), (255, 255, 255))
            btn.state_target = st
            self.menu_buttons.append(btn)

    def reset_env(self):
        self.env.reset()
        self.score = 0
        self.done = False

    def run(self):
        while True:
            if self.state == "MENU":
                self.run_menu()
            elif self.state == "MANUAL":
                self.run_manual()
            elif self.state == "TRAIN_Q":
                self.run_train(agent_name="Q")
            elif self.state == "TRAIN_S":
                self.run_train(agent_name="S")
            elif self.state == "AI_DEMO":
                self.run_ai_demo()
            elif self.state == "TRAINING_DEMO":
                self.run_training_demo()
            else:
                pygame.quit()
                sys.exit()

    def run_menu(self):
        while self.state == "MENU":
            self.clock.tick(60)
            screen.fill((30, 30, 30))
            title_label = font_large.render("Maze RL Demo", True, (255, 255, 255))
            screen.blit(title_label, (SCREEN_WIDTH // 2 - title_label.get_width() // 2, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "EXIT"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.menu_buttons:
                        if btn.is_clicked(event):
                            self.state = btn.state_target

            for btn in self.menu_buttons:
                btn.draw(screen)

            pygame.display.flip()

    def run_manual(self):
        self.reset_env()
        while self.state == "MANUAL":
            self.clock.tick(60)
            self.draw_environment()
            self.draw_info_panel("Manual Play")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "EXIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    if event.key == pygame.K_r:
                        self.reset_env()
                    if not self.done:
                        if event.key == pygame.K_LEFT:
                            _, r, d = self.env.step(0)
                            self.score += r
                            self.done = d
                        elif event.key == pygame.K_DOWN:
                            _, r, d = self.env.step(1)
                            self.score += r
                            self.done = d
                        elif event.key == pygame.K_RIGHT:
                            _, r, d = self.env.step(2)
                            self.score += r
                            self.done = d
                        elif event.key == pygame.K_UP:
                            _, r, d = self.env.step(3)
                            self.score += r
                            self.done = d
            if self.done:
                self.draw_goal_message("Goal reached! Press R to reset or ESC for Menu")
                pygame.display.flip()

    def run_train(self, agent_name="Q"):
        # 纯快速训练，不逐帧显示环境，只显示训练进度
        self.episode_rewards = []
        # 训练回合 1500
        total_episodes = self.total_training_episodes

        if agent_name == "Q":
            self.agent = QLearningAgent()
            self.agent_type = "Q-Learning"
        else:
            self.agent = SarsaAgent()
            self.agent_type = "Sarsa"

        for e in range(total_episodes):
            s = self.agent.env.reset()
            ep_reward = 0
            for _ in range(Config.MAX_STEPS):
                if agent_name == "Q":
                    a = self.agent.choose_action(s)
                    ns, r, done = self.agent.env.step(a)
                    self.agent.learn(s, a, r, ns)
                    s = ns
                else:
                    # 正确调用Sarsa，包含a_next
                    a = self.agent.choose_action(s)
                    ns, r, done = self.agent.env.step(a)
                    if done:
                        self.agent.learn(s, a, r, None, None)
                    else:
                        a_next = self.agent.choose_action(ns)
                        self.agent.learn(s, a, r, ns, a_next)
                        s = ns
                        a = a_next
                ep_reward += r
                if done:
                    break
            self.agent.epsilon = max(self.agent.min_epsilon, self.agent.epsilon * self.agent.epsilon_decay)
            self.episode_rewards.append(ep_reward)
            self.draw_training_screen(e + 1, total_episodes)

        self.state = "MENU"

    def run_ai_demo(self):
        # 使用当前agent进行演示
        if not self.agent:
            self.state = "MENU"
            return
        self.reset_env()
        while self.state == "AI_DEMO":
            self.clock.tick(60)
            self.draw_environment()
            self.draw_info_panel(f"AI Demo ({self.agent_type})")
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "EXIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    elif event.key == pygame.K_r:
                        self.reset_env()

            if not self.done:
                s = self.env.get_state()
                # AI自动动作
                a = self.agent.best_action(s)
                _, r, d = self.env.step(a)
                self.score += r
                self.done = d

    def run_training_demo(self):
        # 边训练边展示环境，每帧执行多个step加速
        if not self.agent:
            # 若还没Agent，则默认Q-Learning
            self.agent = QLearningAgent()
            self.agent_type = "Q-Learning"

        self.episode_rewards = []
        self.episode_count = 0
        self.in_episode = False
        self.reset_env()
        self.current_episode_reward = 0
        self.current_step_count = 0

        while self.state == "TRAINING_DEMO":
            self.clock.tick(60)
            self.handle_events_training_demo()

            # 每帧执行多个环境步
            for _ in range(self.training_speed):
                if not self.in_episode:
                    self.start_new_episode()
                self.training_demo_step()

            self.draw_environment()
            self.draw_info_panel(f"Training Demo ({self.agent_type})", training_demo=True)
            pygame.display.flip()

            if self.episode_count >= self.max_demo_episodes:
                self.state = "MENU"

    def handle_events_training_demo(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "EXIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

    def start_new_episode(self):
        self.env.reset()
        self.done = False
        self.current_episode_reward = 0
        self.current_step_count = 0
        self.in_episode = True

    def training_demo_step(self):
        if self.done:
            self.in_episode = False
            self.episode_rewards.append(self.current_episode_reward)
            self.episode_count += 1
            return

        s = self.env.get_state()
        # 这里假设使用 self.agent 的 Q-Learning 训练，
        # 如果你想要Sarsa演示，可做相应判断
        a = self.agent.choose_action(s)
        ns, r, d = self.env.step(a)
        self.agent.learn(s, a, r, ns)
        self.current_episode_reward += r
        self.done = d
        self.current_step_count += 1
        if self.current_step_count >= Config.MAX_STEPS:
            self.done = True
        if self.done:
            self.agent.epsilon = max(self.agent.min_epsilon, self.agent.epsilon * self.agent.epsilon_decay)

    def draw_environment(self):
        # 绘制迷宫到左侧
        for row in range(self.env.height):
            for col in range(self.env.width):
                screen.blit(floor_img, (col * tile_size, row * tile_size))
        for (r, c) in self.env.coins:
            screen.blit(coin_img, (c * tile_size, r * tile_size))
        for (r, c) in self.env.traps:
            screen.blit(trap_img, (c * tile_size, r * tile_size))
        screen.blit(goal_img, (self.env.goal_col * tile_size, self.env.goal_row * tile_size))
        screen.blit(player_img, (self.env.player_col * tile_size, self.env.player_row * tile_size))

    def draw_info_panel(self, title="", training_demo=False):
        panel_x = MAZE_DISPLAY_WIDTH
        panel_w = INFO_PANEL_WIDTH
        pygame.draw.rect(screen, (60, 60, 60), (panel_x, 0, panel_w, SCREEN_HEIGHT))

        title_surf = font_medium.render(title, True, (255, 255, 255))
        screen.blit(title_surf, (panel_x + 10, 10))

        if not training_demo:
            score_label = font_small.render(f"Score: {int(self.score)}", True, (255, 255, 255))
            screen.blit(score_label, (panel_x + 10, 50))
            hint_label = font_small.render("ESC=Menu | R=Reset", True, (200, 200, 200))
            screen.blit(hint_label, (panel_x + 10, 80))
        else:
            ep_label = font_small.render(f"Episode: {self.episode_count}/{self.max_demo_episodes}", True, (255, 255, 255))
            screen.blit(ep_label, (panel_x + 10, 50))
            if self.episode_rewards:
                last_reward = round(self.episode_rewards[-1], 2)
                lr_label = font_small.render(f"Last Reward: {last_reward}", True, (255, 255, 255))
                screen.blit(lr_label, (panel_x + 10, 80))
                chart = self.generate_reward_chart()
                if chart:
                    chart_rect = chart.get_rect(center=(panel_x + panel_w // 2, SCREEN_HEIGHT // 2 + 50))
                    screen.blit(chart, chart_rect)

    def draw_goal_message(self, text):
        overlay = pygame.Surface((MAZE_DISPLAY_WIDTH, 40))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, SCREEN_HEIGHT - 40))
        msg = font_small.render(text, True, (255, 0, 0))
        screen.blit(msg, (10, SCREEN_HEIGHT - 35))

    def draw_training_screen(self, current_ep, total_ep):
        # 用于纯粹训练时显示进度
        self.clock.tick(60)
        screen.fill((0, 0, 0))
        label = font_large.render(f"Training {self.agent_type}", True, (255, 255, 255))
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 60))

        info_label = font_medium.render(f"Episode: {current_ep}/{total_ep}", True, (200, 200, 200))
        screen.blit(info_label, (SCREEN_WIDTH // 2 - info_label.get_width() // 2, 120))

        if self.episode_rewards:
            last_reward = round(self.episode_rewards[-1], 2)
            r_label = font_medium.render(f"Last Reward: {last_reward}", True, (200, 200, 200))
            screen.blit(r_label, (SCREEN_WIDTH // 2 - r_label.get_width() // 2, 160))
            chart = self.generate_reward_chart()
            if chart:
                chart_rect = chart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                screen.blit(chart, chart_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "EXIT"
                return

    def generate_reward_chart(self):
        if not self.episode_rewards:
            return None
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(self.episode_rewards, color="blue")
        ax.set_xlabel("Episode")
        ax.set_ylabel("Reward")
        ax.set_title("Training Progress")
        fig.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="PNG")
        plt.close(fig)
        buf.seek(0)
        return pygame.image.load(buf, "PNG")

def main():
    app = MazeGameUI()
    app.run()

if __name__ == "__main__":
    main()
