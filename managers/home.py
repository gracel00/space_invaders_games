import pygame
import math
import random


class HomeUI:

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont(
            "consolas", 42, bold=True
        )

        self.button_font = pygame.font.SysFont(
            "consolas", 18, bold=True
        )

        self.small_font = pygame.font.SysFont(
            "consolas", 12, bold=True
        )

        self.bg = (7, 2, 14)
        self.pink = (255, 45, 180)
        self.light_pink = (255, 130, 225)
        self.bright_pink = (255, 215, 250)
        self.white = (255, 245, 255)
        self.gray = (180, 155, 180)
        self.grid_color = (75, 12, 70)
        self.deep_pink = (100, 15, 90)

        cx = screen_width // 2

        button_width = 300
        button_height = 55

        self.start_game_rect = pygame.Rect(
            cx - button_width // 2,
            int(screen_height * 0.40),
            button_width,
            button_height
        )

        self.leaderboard_rect = pygame.Rect(
            cx - button_width // 2,
            int(screen_height * 0.50),
            button_width,
            button_height
        )

        self.profile_rect = pygame.Rect(
            cx - button_width // 2,
            int(screen_height * 0.60),
            button_width,
            button_height
        )

        self.settings_rect = pygame.Rect(
            cx - button_width // 2,
            int(screen_height * 0.70),
            button_width,
            button_height
        )

        self.logout_rect = pygame.Rect(
            30,
            screen_height - 65,
            150,
            40
        )

        self.help_center_rect = pygame.Rect(
            cx - 110,
            screen_height - 35,
            220,
            22
        )

        random.seed(10)

        self.stars = [
            (
                random.randint(20, screen_width - 20),
                random.randint(55, screen_height - 100),
                random.choice([1, 1, 1, 2])
            )
            for _ in range(65)
        ]

    def draw_neon_rect(
        self,
        screen,
        rect,
        color,
        width=2
    ):

        pygame.draw.rect(
            screen,
            (55, 7, 48),
            rect.inflate(10, 10),
            1,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (100, 12, 82),
            rect.inflate(6, 6),
            1,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            width,
            border_radius=5
        )

    def draw_stars(self, screen):

        for x, y, size in self.stars:

            pygame.draw.circle(
                screen,
                self.light_pink,
                (x, y),
                size
            )

    def draw_spaceship(
        self,
        screen,
        x,
        y,
        scale=1.0
    ):

        points = [
            (x, y - int(24 * scale)),
            (x - int(10 * scale), y - int(5 * scale)),
            (x - int(29 * scale), y + int(11 * scale)),
            (x - int(13 * scale), y + int(10 * scale)),
            (x - int(7 * scale), y + int(24 * scale)),
            (x, y + int(17 * scale)),
            (x + int(7 * scale), y + int(24 * scale)),
            (x + int(13 * scale), y + int(10 * scale)),
            (x + int(29 * scale), y + int(11 * scale)),
            (x + int(10 * scale), y - int(5 * scale))
        ]

        pygame.draw.polygon(
            screen,
            (30, 3, 30),
            points
        )

        pygame.draw.lines(
            screen,
            self.light_pink,
            True,
            points,
            2
        )

        cockpit = [
            (x, y - int(15 * scale)),
            (x - int(6 * scale), y + int(6 * scale)),
            (x + int(6 * scale), y + int(6 * scale))
        ]

        pygame.draw.polygon(
            screen,
            self.pink,
            cockpit
        )

        flame = [
            (x - int(6 * scale), y + int(19 * scale)),
            (x, y + int(37 * scale)),
            (x + int(6 * scale), y + int(19 * scale))
        ]

        pygame.draw.polygon(
            screen,
            self.bright_pink,
            flame
        )

    def draw_side_ship(
        self,
        screen,
        x,
        y,
        scale=1.0,
        direction=1
    ):

        points = [
            (x, y),
            (
                x + int(35 * scale) * direction,
                y - int(12 * scale)
            ),
            (
                x + int(58 * scale) * direction,
                y
            ),
            (
                x + int(35 * scale) * direction,
                y + int(12 * scale)
            )
        ]

        pygame.draw.polygon(
            screen,
            (25, 3, 28),
            points
        )

        pygame.draw.lines(
            screen,
            self.pink,
            True,
            points,
            2
        )

        pygame.draw.line(
            screen,
            self.light_pink,
            (
                x + int(58 * scale) * direction,
                y
            ),
            (
                x + int(80 * scale) * direction,
                y
            ),
            2
        )

    def draw_planet(self, screen):

        cx = self.screen_width // 2
        cy = self.screen_height + 80
        radius = 150

        for r in range(radius, 0, -5):

            ratio = r / radius

            color = (
                int(55 * ratio),
                int(6 * ratio),
                int(48 * ratio)
            )

            pygame.draw.circle(
                screen,
                color,
                (cx, cy),
                r
            )

        pygame.draw.arc(
            screen,
            self.light_pink,
            (
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2
            ),
            math.pi,
            math.pi * 2,
            2
        )

    def draw_grid(self, screen):

        horizon = int(
            self.screen_height * 0.74
        )

        for row in range(12):

            y = horizon + row * 18

            pygame.draw.line(
                screen,
                self.grid_color,
                (0, y),
                (self.screen_width, y),
                1
            )

        center = self.screen_width // 2

        for x in range(
            -self.screen_width,
            self.screen_width * 2,
            40
        ):

            top_x = center + (
                x - center
            ) * 0.15

            pygame.draw.line(
                screen,
                self.grid_color,
                (int(top_x), horizon),
                (x, self.screen_height),
                1
            )

    def draw_hud(self, screen):

        for i in range(3):

            x = 35 + i * 34
            y = 32

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x, y + 3, 7, 7)
            )

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x + 8, y + 3, 7, 7)
            )

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x + 4, y + 10, 8, 7)
            )

        unlimited = self.small_font.render(
            "UNLIMITED",
            True,
            self.light_pink
        )

        screen.blit(
            unlimited,
            (154, 35)
        )

        bx = self.screen_width - 72
        by = 32

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx, by, 39, 17),
            2
        )

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx + 39, by + 5, 4, 7)
        )

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx + 5, by + 4, 12, 9)
        )

    def draw_background(self, screen):

        screen.fill(self.bg)

        inner = pygame.Rect(
            17,
            17,
            self.screen_width - 34,
            self.screen_height - 34
        )

        pygame.draw.rect(
            screen,
            (11, 2, 17),
            inner
        )

        self.draw_stars(screen)
        self.draw_grid(screen)
        self.draw_planet(screen)

        self.draw_side_ship(
            screen,
            50,
            270,
            0.65,
            1
        )

        self.draw_side_ship(
            screen,
            self.screen_width - 50,
            310,
            0.65,
            -1
        )

        border = pygame.Rect(
            12,
            12,
            self.screen_width - 24,
            self.screen_height - 24
        )

        self.draw_neon_rect(
            screen,
            border,
            self.pink,
            2
        )

    def draw_button(
        self,
        screen,
        rect,
        text,
        ship=True
    ):

        hover = rect.collidepoint(
            pygame.mouse.get_pos()
        )

        color = (
            self.bright_pink
            if hover
            else self.pink
        )

        pygame.draw.rect(
            screen,
            (50, 6, 45),
            rect,
            border_radius=5
        )

        self.draw_neon_rect(
            screen,
            rect,
            color,
            2
        )

        if ship:

            self.draw_spaceship(
                screen,
                rect.x + 35,
                rect.centery,
                0.32
            )

        text_surface = self.button_font.render(
            text,
            True,
            self.white
        )

        offset = 12 if ship else 0

        screen.blit(
            text_surface,
            (
                rect.centerx -
                text_surface.get_width() // 2 +
                offset,
                rect.centery -
                text_surface.get_height() // 2
            )
        )

    def draw(self, screen, username=None):

        self.draw_background(screen)
        self.draw_hud(screen)

        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            92,
            0.65
        )

        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                cx -
                title.get_width() // 2,
                130
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 220, 180),
            (cx + 220, 180),
            1
        )

        username = username or "Player"

        welcome = self.small_font.render(
            f"WELCOME, {username}",
            True,
            self.light_pink
        )

        screen.blit(
            welcome,
            (
                cx -
                welcome.get_width() // 2,
                195
            )
        )

        self.draw_button(
            screen,
            self.start_game_rect,
            "START GAME"
        )

        self.draw_button(
            screen,
            self.leaderboard_rect,
            "LEADERBOARD"
        )

        self.draw_button(
            screen,
            self.profile_rect,
            "USER PROFILE"
        )

        self.draw_button(
            screen,
            self.settings_rect,
            "SETTINGS"
        )

        self.draw_button(
            screen,
            self.logout_rect,
            "LOG OUT",
            False
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (
                cx - 180,
                self.screen_height - 82
            ),
            (
                cx + 180,
                self.screen_height - 82
            ),
            1
        )

        help_text = self.small_font.render(
            "HELP CENTER",
            True,
            self.white
        )

        screen.blit(
            help_text,
            (
                cx -
                help_text.get_width() // 2,
                self.screen_height - 58
            )
        )

    def handle_event(self, event):

        if (
            event.type != pygame.MOUSEBUTTONDOWN
            or event.button != 1
        ):
            return None

        pos = event.pos

        if self.start_game_rect.collidepoint(pos):
            return "start_game"

        if self.leaderboard_rect.collidepoint(pos):
            return "leaderboard"

        if self.profile_rect.collidepoint(pos):
            return "profile"

        if self.settings_rect.collidepoint(pos):
            return "settings"

        if self.logout_rect.collidepoint(pos):
            return "logout"

        if self.help_center_rect.collidepoint(pos):
            return "help_center"

        return None