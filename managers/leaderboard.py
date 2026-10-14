import pygame
import math
import random

from db import load_leaderboard


class LeaderboardUI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont(
            "consolas",
            42,
            bold=True
        )

        self.section_font = pygame.font.SysFont(
            "consolas",
            22,
            bold=True
        )

        self.button_font = pygame.font.SysFont(
            "consolas",
            17,
            bold=True
        )

        self.rank_font = pygame.font.SysFont(
            "consolas",
            18,
            bold=True
        )

        self.player_font = pygame.font.SysFont(
            "consolas",
            16,
            bold=True
        )

        self.score_font = pygame.font.SysFont(
            "consolas",
            16,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "consolas",
            12,
            bold=True
        )

        self.bg = (7, 2, 14)
        self.panel = (19, 5, 25)

        self.pink = (255, 45, 180)
        self.light_pink = (255, 130, 225)
        self.bright_pink = (255, 215, 250)

        self.white = (255, 245, 255)
        self.gray = (180, 155, 180)

        self.grid_color = (75, 12, 70)
        self.deep_pink = (100, 15, 90)

        cx = screen_width // 2

        self.back_rect = pygame.Rect(
            30,
            screen_height - 60,
            150,
            40
        )

        self.refresh_rect = pygame.Rect(
            screen_width - 180,
            screen_height - 60,
            150,
            40
        )

        self.help_rect = pygame.Rect(
            cx - 110,
            screen_height - 32,
            220,
            20
        )

        self.scroll_y = 0
        self.max_scroll = 0

        self.players = []

        random.seed(22)

        self.stars = [
            (
                random.randint(20, screen_width - 20),
                random.randint(45, screen_height - 90),
                random.choice([1, 1, 1, 2])
            )
            for _ in range(70)
        ]

        self.load_data()

    def load_data(self):
        data = load_leaderboard()

        if data is None:
            data = []

        self.players = data

        row_height = 48

        visible_height = 330

        content_height = len(self.players) * row_height

        self.max_scroll = max(
            0,
            content_height - visible_height
        )

        self.scroll_y = min(
            self.scroll_y,
            self.max_scroll
        )

    def reset_scroll(self):
        self.scroll_y = 0

    def draw_neon_rect(
        self,
        screen,
        rect,
        color,
        width=2,
        radius=6
    ):
        pygame.draw.rect(
            screen,
            (55, 7, 48),
            rect.inflate(10, 10),
            1,
            border_radius=radius + 2
        )

        pygame.draw.rect(
            screen,
            (100, 12, 82),
            rect.inflate(6, 6),
            1,
            border_radius=radius + 1
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            width,
            border_radius=radius
        )

    def draw_stars(self, screen):
        for x, y, size in self.stars:
            pygame.draw.circle(
                screen,
                self.light_pink,
                (x, y),
                size
            )

    def draw_planet(self, screen):
        cx = self.screen_width // 2
        cy = self.screen_height + 75
        radius = 145

        for r in range(radius, 0, -5):
            ratio = r / radius

            color = (
                int(55 * ratio + 20),
                int(7 * ratio),
                int(50 * ratio + 15)
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

    def draw_wireframe_floor(self, screen):
        horizon = int(self.screen_height * 0.80)

        for row in range(9):
            y = horizon + row * 18

            pygame.draw.line(
                screen,
                self.grid_color,
                (0, y),
                (self.screen_width, y),
                1
            )

        center_x = self.screen_width // 2

        for x in range(
            -self.screen_width,
            self.screen_width * 2,
            40
        ):
            pygame.draw.line(
                screen,
                self.grid_color,
                (center_x, horizon),
                (x, self.screen_height),
                1
            )

    def draw_spaceship(
        self,
        screen,
        x,
        y,
        scale=1.0,
        bright=True
    ):
        color = (
            self.bright_pink
            if bright
            else self.light_pink
        )

        outer = [
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
            outer
        )

        pygame.draw.lines(
            screen,
            color,
            True,
            outer,
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

    def draw_asteroid(
        self,
        screen,
        x,
        y,
        radius
    ):
        points = []

        for i in range(9):
            angle = math.pi * 2 * i / 9
            variation = 0.75 + ((i * 13) % 6) / 10

            px = x + math.cos(angle) * radius * variation
            py = y + math.sin(angle) * radius * variation

            points.append(
                (int(px), int(py))
            )

        pygame.draw.polygon(
            screen,
            (18, 3, 22),
            points
        )

        pygame.draw.lines(
            screen,
            self.deep_pink,
            True,
            points,
            1
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

        self.draw_asteroid(
            screen,
            65,
            250,
            30
        )

        self.draw_asteroid(
            screen,
            self.screen_width - 60,
            315,
            22
        )

        self.draw_side_ship(
            screen,
            50,
            355,
            0.65,
            1
        )

        self.draw_side_ship(
            screen,
            self.screen_width - 50,
            220,
            0.65,
            -1
        )

        self.draw_planet(screen)

        self.draw_wireframe_floor(screen)

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

        text = self.small_font.render(
            "RANKING SYSTEM",
            True,
            self.light_pink
        )

        screen.blit(
            text,
            (154, 35)
        )

    def draw_header(self, screen):
        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            88,
            0.55
        )

        title = self.title_font.render(
            "LEADERBOARD",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                cx -
                title.get_width() // 2,
                120
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 220, 174),
            (cx + 220, 174),
            1
        )

        subtitle = self.small_font.render(
            "TOP SPACESHIP INVADERS",
            True,
            self.light_pink
        )

        screen.blit(
            subtitle,
            (
                cx -
                subtitle.get_width() // 2,
                184
            )
        )

    def draw_table_header(self, screen):
        table_x = 115
        table_y = 210
        table_w = 570

        rect = pygame.Rect(
            table_x,
            table_y,
            table_w,
            38
        )

        self.draw_neon_rect(
            screen,
            rect,
            self.deep_pink,
            1
        )

        rank = self.small_font.render(
            "RANK",
            True,
            self.light_pink
        )

        player = self.small_font.render(
            "PLAYER",
            True,
            self.light_pink
        )

        score = self.small_font.render(
            "SCORE",
            True,
            self.light_pink
        )

        screen.blit(
            rank,
            (table_x + 20, table_y + 12)
        )

        screen.blit(
            player,
            (table_x + 115, table_y + 12)
        )

        screen.blit(
            score,
            (table_x + 475, table_y + 12)
        )

    def draw_player_row(
        self,
        screen,
        index,
        player,
        y
    ):
        table_x = 115
        table_w = 570
        row_h = 42

        rect = pygame.Rect(
            table_x,
            y,
            table_w,
            row_h
        )

        if index == 0:
            border_color = self.bright_pink
        elif index == 1:
            border_color = self.light_pink
        elif index == 2:
            border_color = self.pink
        else:
            border_color = self.deep_pink

        pygame.draw.rect(
            screen,
            (19, 5, 25),
            rect,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            border_color,
            rect,
            1,
            border_radius=5
        )

        rank_text = self.rank_font.render(
            str(index + 1),
            True,
            self.bright_pink
        )

        username = str(
            player.get("username", "UNKNOWN")
        )

        score_value = player.get(
            "score",
            0
        )

        try:
            score_value = int(score_value)
        except:
            score_value = 0

        player_text = self.player_font.render(
            username[:24],
            True,
            self.white
        )

        score_text = self.score_font.render(
            str(score_value),
            True,
            self.light_pink
        )

        screen.blit(
            rank_text,
            (
                table_x + 30,
                y + 10
            )
        )

        screen.blit(
            player_text,
            (
                table_x + 115,
                y + 11
            )
        )

        screen.blit(
            score_text,
            (
                table_x + 480,
                y + 11
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (
                table_x + 70,
                y + 9
            ),
            (
                table_x + 70,
                y + row_h - 9
            ),
            1
        )

    def draw_empty(self, screen):
        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            320,
            0.7
        )

        text = self.section_font.render(
            "NO SCORES YET",
            True,
            self.light_pink
        )

        screen.blit(
            text,
            (
                cx -
                text.get_width() // 2,
                355
            )
        )

        small = self.small_font.render(
            "PLAY THE GAME TO ENTER THE RANKING",
            True,
            self.gray
        )

        screen.blit(
            small,
            (
                cx -
                small.get_width() // 2,
                390
            )
        )

    def draw_button(
        self,
        screen,
        rect,
        text,
        ship=False
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
            (55, 6, 48),
            rect,
            border_radius=4
        )

        self.draw_neon_rect(
            screen,
            rect,
            color,
            2
        )

        text_surface = self.button_font.render(
            text,
            True,
            self.white
        )

        offset = 0

        if ship:
            self.draw_spaceship(
                screen,
                rect.x + 25,
                rect.centery,
                0.24
            )

            offset = 8

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

    def draw_footer(self, screen):
        self.draw_button(
            screen,
            self.back_rect,
            "BACK",
            True
        )

        self.draw_button(
            screen,
            self.refresh_rect,
            "REFRESH",
            False
        )

        cx = self.screen_width // 2

        pygame.draw.line(
            screen,
            self.deep_pink,
            (
                cx - 180,
                self.screen_height - 43
            ),
            (
                cx + 180,
                self.screen_height - 43
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
                self.screen_height - 25
            )
        )

    def draw(self, screen):
        self.draw_background(screen)
        self.draw_hud(screen)
        self.draw_header(screen)
        self.draw_table_header(screen)

        table_top = 255
        row_height = 48

        clip_rect = pygame.Rect(
            115,
            250,
            570,
            275
        )

        old_clip = screen.get_clip()

        screen.set_clip(clip_rect)

        if not self.players:
            screen.set_clip(old_clip)
            self.draw_empty(screen)
        else:
            start_y = table_top - self.scroll_y

            for index, player in enumerate(self.players):
                row_y = start_y + index * row_height

                if (
                    row_y + row_height >= clip_rect.top
                    and row_y <= clip_rect.bottom
                ):
                    self.draw_player_row(
                        screen,
                        index,
                        player,
                        row_y
                    )

            screen.set_clip(old_clip)

        self.draw_footer(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.back_rect.collidepoint(event.pos):
                    return "back"

                if self.refresh_rect.collidepoint(event.pos):
                    self.load_data()
                    return None

            if event.button == 4:
                self.scroll_y -= 35
                self.scroll_y = max(
                    0,
                    self.scroll_y
                )

            elif event.button == 5:
                self.scroll_y += 35
                self.scroll_y = min(
                    self.max_scroll,
                    self.scroll_y
                )

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"

            if event.key == pygame.K_UP:
                self.scroll_y -= 35
                self.scroll_y = max(
                    0,
                    self.scroll_y
                )

            elif event.key == pygame.K_DOWN:
                self.scroll_y += 35
                self.scroll_y = min(
                    self.max_scroll,
                    self.scroll_y
                )

        return None