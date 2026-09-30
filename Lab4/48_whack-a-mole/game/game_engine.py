import pygame
import random
from .hole import Hole

# Game Engine

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.holes = []
        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)
        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        self.difficulty = "Medium"
        self.set_difficulty(self.difficulty)

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.score = 0
        self.misses = 0
        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 52, bold=True)
        self.hit_sound = self._create_sound(700, 100)
        self.miss_sound = self._create_sound(200, 120)
        self.game_over_sound = self._create_sound(120, 400)
        self.game_over = False
        self.show_menu = False
        self.game_over_sound_played = False

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

        if difficulty == "Easy":
            self.spawn_chance = 0.015
            self.mole_up_frames = 60
        elif difficulty == "Hard":
            self.spawn_chance = 0.03
            self.mole_up_frames = 30
        else:
            self.spawn_chance = 0.02
            self.mole_up_frames = 45

    def handle_event(self, event):
        if self.show_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.reset("Easy")
                elif event.key == pygame.K_2:
                    self.reset("Medium")
                elif event.key == pygame.K_3:
                    self.reset("Hard")
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.show_menu = True
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        for hole in self.holes:
            if hole.rect().collidepoint(pos):
                if hole.whack():
                    self.score += 1
                    self.hit_sound.play()
                    return

        self.misses += 1
        self.miss_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def reset(self, difficulty):
        self.set_difficulty(difficulty)

        self.time_left_frames = self.round_seconds * 60
        self.score = 0
        self.misses = 0
        self.game_over = False
        self.show_menu = False
        self._game_over_logged = False
        self.game_over_sound_played = False

        for hole in self.holes:
            hole.active = False
            hole.timer = 0

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.game_over = True

            if not self.game_over_sound_played:
                self.game_over_sound.play()
                self.game_over_sound_played = True

            return

        for hole in self.holes:
            hole.update()
            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def _create_sound(self, frequency, duration_ms):
        sample_rate = 44100
        samples = int(sample_rate * duration_ms / 1000)

        sound_buffer = bytearray()

        for i in range(samples):
            value = int(
                32767
                * 0.3
                * ((i * frequency // sample_rate) % 2 * 2 - 1)
            )
            sound_buffer.extend(value.to_bytes(2, byteorder="little", signed=True))

        return pygame.mixer.Sound(buffer=bytes(sound_buffer))

    def render(self, screen):
        for hole in self.holes:
            pygame.draw.circle(screen, DARK_BROWN, (hole.center_x, hole.center_y), 40)
            if hole.active:
                pygame.draw.circle(screen, MOLE_BROWN, (hole.center_x, hole.center_y), 32)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)
        timer_text = self.font.render(f"Time: {seconds_left}s", True, BLACK)
        screen.blit(timer_text, (self.width - 140, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            game_over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
            score_text = self.font.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )
            instruction_text = self.font.render(
                "Press any key or click to continue", True, (255, 255, 255)
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 70)),
            )
            screen.blit(
                score_text,
                score_text.get_rect(center=(self.width // 2, self.height // 2)),
            )
            screen.blit(
                instruction_text,
                instruction_text.get_rect(center=(self.width // 2, self.height // 2 + 60)),
            )
        if self.show_menu:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            menu_title = self.game_over_font.render(
                "PLAY AGAIN?", True, (255, 255, 255)
            )

            easy_text = self.font.render(
                "1 - Easy", True, (255, 255, 255)
            )
            medium_text = self.font.render(
                "2 - Medium", True, (255, 255, 255)
            )
            hard_text = self.font.render(
                "3 - Hard", True, (255, 255, 255)
            )
            exit_text = self.font.render(
                "ESC - Exit", True, (255, 255, 255)
            )

            screen.blit(
                menu_title,
                menu_title.get_rect(
                    center=(self.width // 2, self.height // 2 - 120)
                ),
            )

            screen.blit(
                easy_text,
                easy_text.get_rect(
                    center=(self.width // 2, self.height // 2 - 50)
                ),
            )

            screen.blit(
                medium_text,
                medium_text.get_rect(
                    center=(self.width // 2, self.height // 2)
                ),
            )

            screen.blit(
                hard_text,
                hard_text.get_rect(
                    center=(self.width // 2, self.height // 2 + 50)
                ),
            )

            screen.blit(
                exit_text,
                exit_text.get_rect(
                    center=(self.width // 2, self.height // 2 + 100)
                ),
            )