import pygame
import random
import math

from entities.player import Player
from entities.button import MobileButtons
from entities.enemy import Enemy
from entities.bullet import Bullet
from db import save_score


class GameManager:

    def __init__(self, screen, screen_width, screen_height):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont(
            "consolas", 46, bold=True
        )

        self.space_font = pygame.font.SysFont(
            "consolas", 44, bold=True
        )

        self.btn_font = pygame.font.SysFont(
            "consolas", 18, bold=True
        )

        self.help_font = pygame.font.SysFont(
            "consolas", 13, bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial", 36
        )

        self.PINK = (255, 45, 180)
        self.LIGHT = (255, 130, 225)
        self.BRIGHT = (255, 215, 250)
        self.WHITE = (255, 245, 255)

        self.BG = (7, 2, 14)
        self.GRID = (75, 12, 70)

        self.player_name = ""
        self.current_player_id = None

        self.mobile_controls_enabled = True

        self.game_state = "playing"

        self.setup_game_over_buttons()
        self.reset_game_vars()

    def setup_game_over_buttons(self):

        cx = self.screen_width // 2

        width = 300
        height = 50
        x = cx - width // 2

        self.play_again_rect = pygame.Rect(
            x,
            self.screen_height // 2 + 5,
            width,
            height
        )

        self.back_menu_rect = pygame.Rect(
            x,
            self.screen_height // 2 + 75,
            width,
            height
        )

    def reset_game_vars(self):

        self.player = Player(
            self.screen_width,
            self.screen_height
        )

        self.buttons = MobileButtons()
        self.bullet = None

        self.score = 0
        self.spawn_number = 5
        self.score_saved = False

        self.player_history = []

        self.timer = 0
        self.state_timer = 0

        self.spawn_enemies()

    def start_game(self):

        self.reset_game_vars()
        self.game_state = "playing"

    def spawn_enemies(self):

        self.enemies = [
            Enemy(
                i,
                self.spawn_number,
                self.screen_width
            )
            for i in range(self.spawn_number)
        ]

        self.timer = 0

    def finalize_score(self):

        if self.score_saved:
            return

        if self.current_player_id is None:
            return

        save_score(
            self.current_player_id,
            self.score
        )

        self.score_saved = True

    def draw_neon(
        self,
        rect,
        color=None,
        width=2
    ):

        color = color or self.PINK

        pygame.draw.rect(
            self.screen,
            (45, 7, 42),
            rect.inflate(10, 10),
            1,
            border_radius=5
        )

        pygame.draw.rect(
            self.screen,
            (90, 12, 80),
            rect.inflate(5, 5),
            1,
            border_radius=5
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            width,
            border_radius=5
        )

    def draw_background(self):

        self.screen.fill(self.BG)

        pygame.draw.rect(
            self.screen,
            (12, 2, 18),
            (
                18,
                18,
                self.screen_width - 36,
                self.screen_height - 36
            )
        )

        stars = [
            (55, 85),
            (115, 145),
            (180, 72),
            (245, 125),
            (315, 90),
            (390, 145),
            (470, 78),
            (550, 125),
            (640, 82),
            (720, 145),
            (810, 85),
            (900, 130),
            (960, 185),
            (75, 300),
            (930, 315)
        ]

        for x, y in stars:

            if (
                x < self.screen_width
                and y < self.screen_height
            ):

                pygame.draw.circle(
                    self.screen,
                    self.LIGHT,
                    (x, y),
                    1
                )

        horizon = int(
            self.screen_height * 0.77
        )

        for row in range(12):

            y = horizon + row * 18

            pygame.draw.line(
                self.screen,
                self.GRID,
                (0, y),
                (self.screen_width, y),
                1
            )

        center = self.screen_width // 2

        for x in range(
            -self.screen_width,
            self.screen_width * 2,
            38
        ):

            top_x = center + (
                x - center
            ) * 0.15

            pygame.draw.line(
                self.screen,
                self.GRID,
                (int(top_x), horizon),
                (x, self.screen_height),
                1
            )

        planet_y = self.screen_height + 90
        radius = 150

        for r in range(radius, 0, -5):

            ratio = r / radius

            pygame.draw.circle(
                self.screen,
                (
                    int(45 * ratio),
                    3,
                    int(40 * ratio)
                ),
                (center, planet_y),
                r
            )

        pygame.draw.arc(
            self.screen,
            self.LIGHT,
            (
                center - radius,
                planet_y - radius,
                radius * 2,
                radius * 2
            ),
            math.pi,
            math.pi * 2,
            2
        )

        self.draw_neon(
            pygame.Rect(
                12,
                12,
                self.screen_width - 24,
                self.screen_height - 24
            )
        )

    def update(self, events):

        if self.game_state in (
            "playing",
            "blinking"
        ):

            self.update_gameplay(events)
            self.draw()

        elif self.game_state == "game_over":

            result = self.update_game_over(events)

            if result == "back_home":
                return "back_home"

            self.draw_game_over()

        return None

    def update_gameplay(self, events):

        self.player_history.append(
            (
                self.player.x,
                self.player.y
            )
        )

        if len(self.player_history) > 60:
            self.player_history.pop(0)

        if self.game_state == "playing":

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.player.move_left()

            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            screen_fired = False

            if self.mobile_controls_enabled:
                screen_fired = self.buttons.handle_mouse(
                    self.player,
                    events
                )

            key_fired = any(
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                for event in events
            )

            if (
                screen_fired or key_fired
            ) and not self.bullet:

                self.bullet = Bullet(
                    self.player.x
                    + self.player.width // 2
                    - 16,
                    self.player.y
                )

            self.player.keep_inside_screen()

            if self.bullet:

                self.bullet.update()

                if not self.bullet.is_active:
                    self.bullet = None

            self.timer += 1

            if self.timer >= 180:

                waiting = [
                    enemy
                    for enemy in self.enemies
                    if enemy.state == "waiting"
                ]

                if waiting and self.player_history:

                    random.choice(
                        waiting
                    ).start_drop(
                        *self.player_history[0]
                    )

                self.timer = 0

            all_offscreen = True

            for enemy in self.enemies:

                enemy.update()

                if enemy.state != "offscreen":
                    all_offscreen = False

            if all_offscreen:

                self.spawn_number += 1
                self.spawn_enemies()

            self.check_collisions()

        else:

            self.player.update_blink()
            self.state_timer += 1

            for enemy in self.enemies:
                enemy.update()

            if self.state_timer >= 180:

                self.finalize_score()

                self.game_state = "game_over"
                self.player.is_blinking = False

    def update_game_over(self, events):

        self.finalize_score()

        for event in events:

            if (
                event.type != pygame.MOUSEBUTTONDOWN
                or event.button != 1
            ):
                continue

            if self.play_again_rect.collidepoint(
                event.pos
            ):

                self.start_game()
                return "playing"

            if self.back_menu_rect.collidepoint(
                event.pos
            ):

                self.game_state = "back_home"
                return "back_home"

        return None

    def draw(self):

        if self.game_state in (
            "playing",
            "blinking"
        ):

            self.draw_synthwave_background()

            self.player.draw(self.screen)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            if self.bullet:
                self.bullet.draw(self.screen)

            if self.mobile_controls_enabled:
                self.buttons.draw(self.screen)

            score_text = self.font.render(
                f"Score: {self.score}",
                True,
                self.WHITE
            )

            self.screen.blit(
                score_text,
                (20, 20)
            )

        elif self.game_state == "game_over":

            self.draw_game_over()

    def draw_synthwave_background(self):

        self.draw_background()

    def draw_game_over(self):

        self.draw_background()

        cx = self.screen_width // 2

        game_over = self.space_font.render(
            "GAME OVER",
            True,
            self.BRIGHT
        )

        self.screen.blit(
            game_over,
            (
                cx - game_over.get_width() // 2,
                75
            )
        )

        score_label = self.help_font.render(
            "FINAL SCORE",
            True,
            self.LIGHT
        )

        self.screen.blit(
            score_label,
            (
                cx - score_label.get_width() // 2,
                185
            )
        )

        score_value = self.title_font.render(
            str(self.score),
            True,
            self.BRIGHT
        )

        self.screen.blit(
            score_value,
            (
                cx - score_value.get_width() // 2,
                208
            )
        )

        mouse_pos = pygame.mouse.get_pos()

        buttons = (
            (self.play_again_rect, "PLAY AGAIN"),
            (self.back_menu_rect, "BACK MENU")
        )

        for rect, text in buttons:

            hovered = rect.collidepoint(mouse_pos)

            if hovered:

                fill_color = self.PINK
                border_color = self.BRIGHT
                text_color = self.BG

            else:

                fill_color = (35, 5, 35)
                border_color = self.PINK
                text_color = self.WHITE

            pygame.draw.rect(
                self.screen,
                fill_color,
                rect,
                border_radius=5
            )

            self.draw_neon(
                rect,
                border_color
            )

            text_surface = self.btn_font.render(
                text,
                True,
                text_color
            )

            self.screen.blit(
                text_surface,
                (
                    rect.centerx -
                    text_surface.get_width() // 2,
                    rect.centery -
                    text_surface.get_height() // 2
                )
            )

    def check_collisions(self):

        player_rect = self.player.get_rect()

        for enemy in self.enemies:

            if enemy.state == "offscreen":
                continue

            enemy_rect = enemy.get_rect()

            if player_rect.colliderect(enemy_rect):

                self.game_state = "blinking"
                self.player.is_blinking = True
                self.state_timer = 0

                return

            if (
                self.bullet
                and self.bullet.get_rect().colliderect(
                    enemy_rect
                )
            ):

                enemy.state = "offscreen"
                self.bullet = None
                self.score += 1

                break