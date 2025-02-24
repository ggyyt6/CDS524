import pygame
import sys
import json

pygame.init()
pygame.font.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Adventure")
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, w, h, text, font, bg_color, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt_surface, (self.rect.x+5, self.rect.y+5))

class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 40)
        self.start_button = Button(screen_width//2 - 100, screen_height//2 - 50, 200, 50, "Start Game", self.font, (100, 180, 100), (255, 255, 255))
        self.instr_button = Button(screen_width//2 - 100, screen_height//2 + 10, 200, 50, "Instructions", self.font, (100, 180, 100), (255, 255, 255))
        self.score_button = Button(screen_width//2 - 100, screen_height//2 + 70, 200, 50, "Scoreboard", self.font, (100, 180, 100), (255, 255, 255))
        self.quit_button = Button(screen_width//2 - 100, screen_height//2 + 130, 200, 50, "Quit", self.font, (100, 180, 100), (255, 255, 255))
        self.bg_image = pygame.image.load("menu_bg.png").convert()
    def run(self):
        while True:
            screen.blit(self.bg_image, (0, 0))
            self.start_button.draw(screen)
            self.instr_button.draw(screen)
            self.score_button.draw(screen)
            self.quit_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.start_button.is_clicked(event):
                    return "PLAY"
                if self.instr_button.is_clicked(event):
                    return "INSTRUCTIONS"
                if self.score_button.is_clicked(event):
                    return "SCOREBOARD"
                if self.quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()

class Instructions:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 30)
        self.back_button = Button(screen_width//2 - 60, screen_height - 80, 120, 50, "Back", self.font, (80, 80, 200), (255, 255, 255))
        self.bg_image = pygame.image.load("instructions_bg.png").convert()
    def run(self):
        while True:
            screen.blit(self.bg_image, (0, 0))
            lines = ["Use arrow keys to move.", "Collect coins for rewards.", "Avoid traps or lose points.", "Reach the goal to finish."]
            y_offset = 100
            for line in lines:
                label = self.font.render(line, True, (255, 255, 255))
                screen.blit(label, (screen_width//2 - label.get_width()//2, y_offset))
                y_offset += 50
            self.back_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"
                if self.back_button.is_clicked(event):
                    return "MENU"

class Scoreboard:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 30)
        self.back_button = Button(screen_width//2 - 60, screen_height - 80, 120, 50, "Back", self.font, (200, 150, 100), (255, 255, 255))
        self.bg_image = pygame.image.load("scoreboard_bg.png").convert()
        self.scores = []
        self.load_scores()
    def load_scores(self):
        try:
            with open("scoreboard.json", "r") as f:
                self.scores = json.load(f)
        except:
            self.scores = []
    def save_scores(self):
        with open("scoreboard.json", "w") as f:
            json.dump(self.scores, f)
    def add_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:10]
        self.save_scores()
    def run(self):
        while True:
            screen.blit(self.bg_image, (0, 0))
            y_offset = 100
            title = self.font.render("Top Scores", True, (255, 255, 255))
            screen.blit(title, (screen_width//2 - title.get_width()//2, 40))
            for entry in self.scores:
                label = self.font.render(entry["name"] + ": " + str(entry["score"]), True, (255, 255, 255))
                screen.blit(label, (screen_width//2 - label.get_width()//2, y_offset))
                y_offset += 40
                if y_offset > 400:
                    break
            self.back_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"
                if self.back_button.is_clicked(event):
                    return "MENU"

class GameOver:
    def __init__(self, final_score):
        self.font = pygame.font.SysFont("Arial", 30)
        self.final_score = final_score
        self.bg_image = pygame.image.load("gameover_bg.png").convert()
        self.input_box = InputBox(screen_width//2 - 150, 320, 300, 40, self.font)
        self.submit_button = Button(screen_width//2 - 50, 380, 100, 50, "Submit", self.font, (250, 100, 100), (255, 255, 255))
        self.scoreboard = Scoreboard()
    def run(self):
        name_text = ""
        while True:
            screen.blit(self.bg_image, (0, 0))
            label = self.font.render("Game Over!", True, (255, 255, 255))
            screen.blit(label, (screen_width//2 - label.get_width()//2, 200))
            score_label = self.font.render("Your Score: " + str(self.final_score), True, (255, 255, 255))
            screen.blit(score_label, (screen_width//2 - score_label.get_width()//2, 250))
            self.input_box.draw(screen)
            self.submit_button.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"
                result = self.input_box.handle_event(event)
                if result is not None:
                    name_text = result
                if self.submit_button.is_clicked(event):
                    if name_text.strip():
                        self.scoreboard.add_score(name_text, self.final_score)
                        return "MENU"

class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 24)
        self.bg_image = pygame.image.load("game_bg.png").convert()
        self.score = 0
        self.player_x = 50
        self.player_y = 50
        self.speed = 5
        self.player_image = pygame.image.load("player.png").convert_alpha()
        self.running = True
    def run(self):
        while self.running:
            screen.blit(self.bg_image, (0, 0))
            screen.blit(self.player_image, (self.player_x, self.player_y))
            score_label = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
            screen.blit(score_label, (20, 20))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.player_x += self.speed
            if keys[pygame.K_UP]:
                self.player_y -= self.speed
            if keys[pygame.K_DOWN]:
                self.player_y += self.speed
            if self.player_x < 0:
                self.player_x = 0
            if self.player_x > screen_width - 32:
                self.player_x = screen_width - 32
            if self.player_y < 0:
                self.player_y = 0
            if self.player_y > screen_height - 32:
                self.player_y = screen_height - 32
            self.score += 1
            if self.score >= 400:
                return "GAMEOVER"

def run_init():
    menu = Menu()
    instructions = Instructions()
    scoreboard = Scoreboard()
    state = "MENU"
    while True:
        if state == "MENU":
            s = menu.run()
            state = s
        elif state == "INSTRUCTIONS":
            s = instructions.run()
            if s == "MENU":
                state = "MENU"
            else:
                state = "EXIT"
        elif state == "SCOREBOARD":
            s = scoreboard.run()
            if s == "MENU":
                state = "MENU"
            else:
                state = "EXIT"
        elif state == "PLAY":
            g = Game()
            s = g.run()
            if s == "GAMEOVER":
                go = GameOver(g.score)
                state = go.run()
            elif s == "EXIT":
                state = "EXIT"
        elif state == "EXIT":
            pygame.quit()
            sys.exit()
