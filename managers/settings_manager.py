import pygame


class SettingsUI:

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

        self.grid_color = (75, 12, 70)
        self.deep_pink = (100, 15, 90)

        cx = screen_width // 2

        self.controls_rect = pygame.Rect(
            cx - 190,
            270,
            380,
            60
        )

        self.back_rect = pygame.Rect(
            cx - 100,
            screen_height - 70,
            200,
            45
        )

        self.controls_on = True

    def draw_neon_rect(self, screen, rect, color, width=2):

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

        stars = [
            (50, 70),
            (110, 110),
            (180, 65),
            (250, 95),
            (330, 60),
            (420, 105),
            (500, 70),
            (590, 115),
            (670, 65),
            (740, 100)
        ]

        for x, y in stars:
            pygame.draw.circle(
                screen,
                self.light_pink,
                (x, y),
                1
            )

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

    def draw_toggle(
        self,
        screen,
        rect,
        label,
        enabled
    ):

        pygame.draw.rect(
            screen,
            (50, 6, 45),
            rect,
            border_radius=5
        )

        self.draw_neon_rect(
            screen,
            rect,
            self.pink,
            2
        )

        text = self.button_font.render(
            label,
            True,
            self.white
        )

        screen.blit(
            text,
            (
                rect.left + 25,
                rect.centery -
                text.get_height() // 2
            )
        )

        toggle_width = 85
        toggle_height = 30

        toggle = pygame.Rect(
            rect.right - toggle_width - 15,
            rect.centery - toggle_height // 2,
            toggle_width,
            toggle_height
        )

        if enabled:
            toggle_color = self.light_pink
            status = "ON"
            knob_x = toggle.right - 16
        else:
            toggle_color = (120, 70, 110)
            status = "OFF"
            knob_x = toggle.left + 16

        pygame.draw.rect(
            screen,
            (20, 3, 20),
            toggle,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            toggle_color,
            toggle,
            2,
            border_radius=15
        )

        pygame.draw.circle(
            screen,
            toggle_color,
            (
                knob_x,
                toggle.centery
            ),
            10
        )

        status_text = self.small_font.render(
            status,
            True,
            toggle_color
        )

        screen.blit(
            status_text,
            (
                toggle.centerx -
                status_text.get_width() // 2,
                toggle.centery -
                status_text.get_height() // 2
            )
        )

    def draw_button(self, screen, rect, text):

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

        text_surface = self.button_font.render(
            text,
            True,
            self.white
        )

        screen.blit(
            text_surface,
            (
                rect.centerx -
                text_surface.get_width() // 2,
                rect.centery -
                text_surface.get_height() // 2
            )
        )

    def draw(self, screen):

        self.draw_background(screen)

        cx = self.screen_width // 2

        title = self.title_font.render(
            "SETTINGS",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                cx -
                title.get_width() // 2,
                105
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 220, 165),
            (cx + 220, 165),
            1
        )

        subtitle = self.small_font.render(
            "MOBILE CONTROLS",
            True,
            self.light_pink
        )

        screen.blit(
            subtitle,
            (
                cx -
                subtitle.get_width() // 2,
                200
            )
        )

        self.draw_toggle(
            screen,
            self.controls_rect,
            "MOBILE CONTROLS",
            self.controls_on
        )

        self.draw_button(
            screen,
            self.back_rect,
            "BACK"
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "back"

        if (
            event.type != pygame.MOUSEBUTTONDOWN
            or event.button != 1
        ):
            return None

        if self.controls_rect.collidepoint(event.pos):

            self.controls_on = not self.controls_on

            return "controls_toggle"

        if self.back_rect.collidepoint(event.pos):

            return "back"

        return None